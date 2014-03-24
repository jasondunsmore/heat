#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from contextlib import contextmanager
from functools import wraps
import json
import os
import paramiko
import tempfile
import time


def get_proxy(dest_host, jump_user, jump_key, jump_port, jump_host,
              dest_port='22'):
    proxy_cmd = (
        'ssh -l {jump_user} -i {jump_key} -W {dest_host}:{dest_port} '
        '-p {jump_port} -o UserKnownHostsFile=/dev/null '
        '-o StrictHostKeyChecking=no {jump_host}').format(
            jump_user=jump_user,
            jump_key=jump_key,
            dest_host=dest_host,
            dest_port=dest_port,
            jump_port=jump_port,
            jump_host=jump_host)
    print('ProxyCommand string: %s' % proxy_cmd)
    return paramiko.proxy.ProxyCommand(proxy_cmd)


class RemoteUtilsException(Exception):

    def __str__(self):
        return unicode(self.message).encode('UTF-8')

    def __unicode__(self):
        return unicode(self.message)

    def __deepcopy__(self, memo):
        return self.__class__(**self.kwargs)


class RemoteCommandException(RemoteUtilsException):
    def __init__(self, **kwargs):
        self.message = ("Host: %(host)s\n"
                        "Output:\n%(output)s\n"
                        "Command: %(command)s\n"
                        "Exit Code: %(exit_code)s\n"
                        "Remote Log: %(remote_log)s" % kwargs)


class SFTPException(RemoteUtilsException):
    def __init__(self, **kwargs):
        self.message = ("Host: %(host)s\n"
                        "Username: %(username)s\n"
                        "Private key: %(private_key)s" % kwargs)


class SFTPRetriesExhausted(RemoteUtilsException):
    def __init__(self, **kwargs):
        self.message = ("SFTP failure after %(retries)s retries" % kwargs)


class RemoteCommands(object):
    """Must call connection_info(username, host, private_key)."""

    def __init__(self, username, host, private_key, jump_enabled, jump_user,
                 jump_key, jump_port, jump_host, sftp_retries):
        self.private_key = private_key
        self.username = username
        self.host = host
        self._sftp_connection = None
        self.jump_enabled = jump_enabled
        self.jump_user = jump_user
        self.jump_key = jump_key
        self.jump_port = jump_port
        self.jump_host = jump_host
        self.sftp_retries = sftp_retries

    @contextmanager
    def sftp_connection(self):
        with tempfile.NamedTemporaryFile() as private_key_file:
            private_key_file.write(self.private_key)
            private_key_file.seek(0)
            pkey = paramiko.RSAKey.from_private_key_file(
                private_key_file.name)

            transport = None
            sftp = None
            if self.jump_enabled:
                print('SSH jump enabled, calling get_proxy()...')
                sock = get_proxy(self.host, self.jump_user, self.jump_key,
                                 self.jump_port, self.jump_host)
            else:
                print('SSH jump NOT enabled')
                sock = (self.host, 22)

            try:
                transport = paramiko.Transport(sock)
                transport.connect(hostkey=None, username=self.username,
                                  pkey=pkey)
                sftp = paramiko.SFTPClient.from_transport(transport)
            finally:
                if sftp:
                    yield sftp
                    sftp.close()
                    transport.close()
                else:
                    if transport:
                        transport.close()
                    raise SFTPException(host=self.host,
                                        username=self.username,
                                        private_key=self.private_key)

    def create_remote_folder(self, path, name=None):
        if name:
            folder = os.path.join(path, name)
        else:
            folder = path

        for x in xrange(self.sftp_retries):
            print("create_remote_folder(): Opening SFTP connection, "
                  "attempt %s..." % x)
            try:
                with self.sftp_connection() as sftp:
                    sftp.mkdir(folder)
            except (EOFError, paramiko.SSHException, SFTPException) as exc:
                print("Encountered exception: %s.  Retrying..." % exc)
                time.sleep(5)
                continue
            except IOError as ioe:
                if ioe.errno == 13:
                    print("Permission denied to create %(folder)s on "
                          "%(remote)s" % dict(folder=folder, remote=self.host))
                    raise ioe
                print("There was an error creating the remote folder "
                      "%(folder)s. The remote folder already exists."
                      % dict(folder=folder))
            return folder
        raise SFTPRetriesExhausted(retries=self.sftp_retries)

    def read_remote_file(self, path):
        for x in xrange(self.sftp_retries):
            print("read_remote_file(): Opening SFTP connection, attempt "
                  "%s..." % x)
            try:
                with self.sftp_connection() as sftp:
                    with sftp.open(path, 'r') as remote_file:
                        return [x for x in remote_file]
            except (EOFError, paramiko.SSHException, SFTPException) as exc:
                print("Encountered exception: %s.  Retrying..." % exc)
                time.sleep(5)
                continue
        raise SFTPRetriesExhausted(retries=self.sftp_retries)

    def write_remote_file(self, path, name, data, mode=None):
        remote_file = os.path.join(path, name)
        sftp_file = None
        for x in xrange(self.sftp_retries):
            print("write_remote_file(): Opening SFTP connection, attempt "
                  "%s..." % x)
            try:
                with self.sftp_connection() as sftp:
                    sftp_file = sftp.open(remote_file, 'w')
                    sftp_file.write(data)
                    if mode is not None:
                        sftp.chmod(remote_file, mode)
            except (EOFError, paramiko.SSHException, SFTPException) as exc:
                print("Encountered exception: %s.  Retrying..." % exc)
                time.sleep(5)
                continue
            finally:
                if sftp_file is not None:
                    sftp_file.close()
            return remote_file
        raise SFTPRetriesExhausted(retries=self.sftp_retries)

    def write_remote_json(self, path, name, data):
        return self.write_remote_file(path, name, json.dumps(data))

    def execute_remote_command(self, name, script, save=True, logfile=None,
                               exec_path='/tmp'):
        print("Executing remote script %(name)s." % {'name': name})
        wrap = ("#!/bin/bash -x\n"
                "cd %(path)s\n"
                "%(script)s"
                % dict(path=exec_path,
                       script=script))

        if save:
            if logfile is None:
                logfile = os.path.join(exec_path, name + ".log")

            script_path = self.write_remote_file(exec_path, name, wrap,
                                                 mode=700)
            command = "%s > %s 2>&1" % (script_path, logfile)
            return self._execute_remote_command(command, logfile=logfile)
        else:
            return self._execute_remote_command(wrap)

    def _execute_remote_command(self, command, logfile=None):
        """Executes a remote command over ssh without blocking."""
        with tempfile.NamedTemporaryFile() as private_key_file:
            private_key_file.write(self.private_key)
            private_key_file.seek(0)
            try:
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(
                    paramiko.MissingHostKeyPolicy())

                if self.jump_enabled:
                    print('SSH jump enabled, calling get_proxy()...')
                    sock = get_proxy(self.host, self.jump_user, self.jump_key,
                                     self.jump_port, self.jump_host)
                else:
                    print('SSH jump NOT enabled')
                    sock = None
                ssh.connect(self.host,
                            username=self.username,
                            key_filename=private_key_file.name,
                            sock=sock)

                print("Executing command: %s" % command)
                x, stdout_buf, stderr_buf = ssh.exec_command(command)

                exit_code = stdout_buf.channel.recv_exit_status()
                stdout, stderr = (stdout_buf.read(), stderr_buf.read())
                if exit_code != 0:
                    if logfile is not None:
                        print("Reading remote log: %s" % logfile)
                        output = self.read_remote_file(logfile)
                    else:
                        output = stderr
                    raise RemoteCommandException(command=command,
                                                 exit_code=exit_code,
                                                 remote_log=logfile,
                                                 output=output,
                                                 host=self.host)
                else:
                    return(stdout, stderr)
            finally:
                if ssh:
                    ssh.close()


def remote_execute(function):
    """
    kwargs (The decorated function should accept):
        :kwarg exec_path: The path to execute the remote command in. defaults
               to /tmp
        :kwarg logfile: The file contents to return in the event of an error.

        ex: function(self, logfile=None, exec_path=None)

    returns (The function should return):
        :returns dict:
            :key script: The commands to execute.
            :key save: True if the script should be saved on the
                remote server.
            :key post_run: A function to call after the script is executed.

        ex: return dict(script="ls -al", save=True)
    """
    @wraps(function)
    def wrapper(remote, *args, **kwargs):
        assert isinstance(remote, RemoteCommands)
        # Get function kwargs
        logfile = kwargs.get('logfile', None)
        exec_path = kwargs.get('exec_path', '/tmp')

        results = function(remote, *args, **kwargs)

        # Get function return values
        save = results.get('save', True)
        script = results['script']
        post_run = results.get('post_run', lambda: None)

        name = function.__name__
        try:
            return remote.execute_remote_command(name, script, save=save,
                                                 logfile=logfile,
                                                 exec_path=exec_path)
        except Exception:
            raise
        else:
            post_run()
    return wrapper
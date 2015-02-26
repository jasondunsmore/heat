import argparse
import ast
import os
import paramiko
import socket
import sys
import time

import remote_utils


SCRIPT_ERROR_MSG = ("The %(path)s script exited with a non-zero exit "
                    "status.  To see the error message, log into the "
                    "server at %(ip)s and view %(log)s")


def run_ssh_command(command):
    """Run a shell command on the Cloud Server via SSH."""
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
    if ast.literal_eval(args.jump_enabled):
        print 'SSH jump enabled, calling get_proxy()...'
        sock = remote_utils.get_proxy(args.ip, args.jump_user, args.jump_key,
                                      args.jump_port, args.jump_host)
    else:
        print 'SSH jump NOT enabled'
        sock = None
    ssh.connect(args.ip, username="root", key_filename=args.key_file, sock=sock)
    os.remove(args.key_file)  # Earliest this sensitive file can be deleted
    chan = ssh.get_transport().open_session()
    chan.settimeout(args.timeout)
    chan.exec_command(command)
    try:
        # The channel timeout only works for read/write operations
        chan.recv(1024)
    except socket.timeout:
        sys.exit("SSH command timed out after %s seconds")
    else:
        return chan.recv_exit_status()
    finally:
        ssh.close()
        chan.close()


def sftp_files(files):
    """Transfer files to the Cloud Server via SFTP."""

    def get_transport():
        if ast.literal_eval(args.jump_enabled):
            print 'SSH jump enabled, calling get_proxy()...'
            sock = remote_utils.get_proxy(args.ip, args.jump_user,
                                          args.jump_key, args.jump_port,
                                          args.jump_host)
        else:
            print 'SSH jump NOT enabled'
            sock = (args.ip, 22)
        return paramiko.Transport(sock)

    def get_connected_transport():
        pkey = paramiko.RSAKey.from_private_key_file(args.key_file)
        for x in xrange(args.sftp_retries):
            try:
                transport = get_transport()
                transport.connect(hostkey=None, username="root", pkey=pkey)
            except Exception as e:
                print e
                print 'Failed to get & connect to transport, sleeping 5 sec'
                time.sleep(5)
                continue
            else:
                return transport
        sys.exit("Failed to connect to SSH transport after %s tries" %
                 args.sftp_retries)

    transport = get_connected_transport()
    sftp = paramiko.SFTPClient.from_transport(transport)
    try:
        for remote_file in files:
            sftp_file = sftp.open(remote_file['path'], 'w')
            sftp_file.write(remote_file['data'])
            sftp_file.close()
    except:
        sys.exit('Failed to write "%s" on remote host' % remote_file)
    finally:
        sftp.close()
        transport.close()


def run_userdata():

    with open(args.userdata_file, 'rb') as f:
        userdata = f.read()
    os.remove(args.userdata_file)
    with open(args.script_file, 'r') as f:
        script = f.read()
    os.remove(args.script_file)

    print 'Creating heat-script and userdata files on server'
    files = [{'path': "/tmp/userdata", 'data': userdata},
             {'path': "/root/heat-script.sh", 'data': script}]
    sftp_files(files)

    print 'Connecting via SSH to run script'
    command = "bash -ex /root/heat-script.sh > /root/heat-script.log 2>&1"
    exit_code = run_ssh_command(command)
    if exit_code == 42:
        sys.exit(SCRIPT_ERROR_MSG %
                 {'path': "cfn-userdata",
                  'ip': args.ip,
                  'log': "/root/cfn-userdata.log"})
    elif exit_code != 0:
        sys.exit(SCRIPT_ERROR_MSG %
                 {'path': "heat-script.sh",
                  'ip': args.ip,
                  'log': "/root/heat-script.log"})


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--userdata-file')
    parser.add_argument('--script-file')
    parser.add_argument('--ip')
    parser.add_argument('--key-file')
    parser.add_argument('--timeout', type=int)
    parser.add_argument('--sftp-retries', type=int)
    parser.add_argument('--jump-enabled')
    parser.add_argument('--jump-host')
    parser.add_argument('--jump-port')
    parser.add_argument('--jump-user')
    parser.add_argument('--jump-key')
    args = parser.parse_args()

    try:
        run_userdata()
    finally:
        if os.path.isfile(args.key_file):
            os.remove(args.key_file)
        if os.path.isfile(args.script_file):
            os.remove(args.script_file)
        if os.path.isfile(args.userdata_file):
            os.remove(args.userdata_file)
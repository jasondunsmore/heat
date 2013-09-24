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
import tempfile
import json
import os
import uuid
import subprocess
import errno
import paramiko
from Crypto.PublicKey import RSA

from heat.db.sqlalchemy import api as db_api
from heat.engine import resource

from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)

class ChefSolo(resource.Resource):
    properties_schema = {
        #TODO(andrew-plunk): custom valiation only berks or chef not both
        'Berksfile': {'Type': 'String'},
        'Cheffile': {'Type': 'String'},
        'username': {'Type': 'String',
                            'Default': 'root',
                            'Required': True},
        'hostname': {'Type': 'String',
                            'Required': True},
        #TODO(andrew-plunk): maybe not required
        'public_key': {'Type': 'String',
                        'Required': True},
        'private_key': {'Type': 'String',
                        'Required': True},
        'data_bags': {'Type': 'Map'},
        'node_json': {'Type': 'Map'}
    }
    attributes_schema = {
        'secret_key': ('The chef secret key for encrypting databags.'),
    }

    def __init__(self, name, json_snippet, stack):
        super(ChefSolo, self).__init__(name, json_snippet, stack) 
        self._secret_key = None
        self._future_resource_id = str(uuid.uuid4())

    @property
    def secret_key(self):
        """Return the private SSH key for the resource."""
        if self._secret_key:
            return self._secret_key
        if self.id is not None:
            secret_key = db_api.resource_data_get(self, 'secret_key')
            if not secret_key:
                return None
            self._secret_key = secret_key
            return secret_key

    @secret_key.setter
    def secret_key(self, secret_key):
        """Save the resource's private SSH key to the database."""
        self._secret_key = secret_key
        if self.id is not None:
            db_api.resource_data_set(self, 'secret_key', secret_key, True)

    #TODO(andrew-plunk): define the properties schema correctly
    #TODO(andrew-plunk): custom server validation, type required
    #TODO(andrew-plunk): fix solo_config to be map turned into string,
    #or set variables for json_attribs
    def _run_ruby_command(self, path, command, params):
        """Runs a knife-like command (ex. librarian-chef).

        Since knife-ike command errors are returned to stderr, we need to capture
        stderr and check for errors.

        That needs to be run in a kitchen, so we move curdir and need to make sure
        we stay there, so I added some synchronization code while that takes place
        However, if code calls in that already has a lock, the optional lock param
        can be set to false so thise code does not lock.
        :param version_param: the parameter used to get the command's version. This
                is used to check if the program is installed.
        """
        params.insert(0, command)
        logger.debug("Running: '%s' in path '%s'", ' '.join(params), path)
        cwd = os.getcwd()
        try:
            if path:
                os.chdir(path)
            output = subprocess.check_output(params)
            if path:
                os.chdir(cwd)
            return output
        except OSError as exc:
            if exc.errno == errno.ENOENT:
                # Check if command is installed
                output = None
                try:
                    output = subprocess.check_output(['which', command])
                except subprocess.CalledProcessError:
                    pass
                if not output:
                    msg = ("'%s' is not installed or not accessible on the "
                            "server" % command)
                    #TODO(andrew-plunk) proper error
                    raise ValueError(msg)
            raise exc
        except subprocess.CalledProcessError as exc:
            msg = exc.output
            #TODO(andrew-plunk) proper error
            raise ValueError(msg)

    def _run_kitchen_command(self, kitchen_path, params):
        """Runs the 'knife xxx' command.

        This also needs to handle knife command errors, which are returned to
        stderr.

        That needs to be run in a kitchen, so we move curdir and need to make sure
        we stay there, so I added some synchronization code while that takes place
        However, if code calls in that already has a lock, the optional lock param
        can be set to false so thise code does not lock
        """
        logger.debug("Running: '%s' in path '%s'", ' '.join(params), kitchen_path)
        if '-c' not in params:
            config_file = os.path.join(kitchen_path, 'solo.rb')
            if os.path.exists(config_file):
                logger.warning("Knife command called without a '-c' flag. The '-c' "
                            "flag is a strong safeguard in case knife runs in the "
                            "wrong directory. Consider adding it and pointing to "
                            "solo.rb")
                logger.debug("Defaulting to config file '%s'", config_file)
                params.extend(['-c', config_file])
        result = self._run_ruby_command(kitchen_path, params[0], params[1:])

        # Knife succeeds even if there is an error. This code tries to parse the
        # output to return a useful error. Note that FATAL erros will be picked up
        # by _run_ruby_command
        last_error = ''
        for line in result.split('\n'):
            if 'ERROR:' in line:
                logger.error(line)
                last_error = line
        if last_error:
            if 'KnifeSolo::::' in last_error:
                # Get the string after a Knife-Solo error::
                error = last_error.split('Error:')[-1]
                if error:
                    msg = "Knife error encountered: %s" % error
                    #TODO(andrew-plunk): better error
                    raise ValueError(msg)
                # Don't raise on all errors. They don't all mean failure!
        return result

    def _install_cookbooks(self, kitchen_path):
        if self.properties.get('Berksfile'):
            #install cookbooks with berksfile
            with file(os.path.join(kitchen_path, 'Berksfile'), 'w') as berksfile:
                berksfile.write(self.properties.get('Berksfile'))
            self._run_ruby_command(kitchen_path, 'berks',
                                   ['install',
                                    '--path',
                                    os.path.join(kitchen_path, 'cookbooks')]
            )
            logger.debug("Ran 'berks install' in: %s", kitchen_path)

        elif self.properties.get('Cheffile'):
            #install cookbooks with librarian chef
            with file(os.path.join(kitchen_path, 'Cheffile'), 'w') as cheffile:
                cheffile.write(self.properties.get('Cheffile'))
            self._run_ruby_command(kitchen_path, 'librarian-chef',
                                   ['install'])
            logger.debug("Ran 'librarian-chef install' in: %s", kitchen_path)

    def write_databags(self, item_id, databags, kitchen_path, private_key_path,
                       solo_config):
        for name, bag in databags.iteritems():
            encrypted = bag['encrypted']
            data = bag['data']
            self.write_databag(name, item_id, data,
                               kitchen_path,
                               solo_config,
                               secret_file=private_key_path if encrypted
                                                            else None)

    #TODO(andrew-plunk) you changed kitchen path to kitchen name. Check
    #TODO(andrew-plunk) TEST
    #TODO(andrew-plunk) removed environment because kitchen path is fully qualified
    def write_databag(self, bagname, itemname, contents, kitchen_path,
                      solo_config, secret_file=None):
        """Updates a data_bag or encrypted_data_bag

        :param environment: the ID of the environment
        :param bagname: the name of the databag (in solo, this ends up being a
                directory)
        :param item: the name of the item (in solo this ends up being a .json file)
        :param contents: this is a dict of attributes to write in to the databag
        :param path: optional override to the default path where environments live
        :param secret_file: the path to a certificate used to encrypt a data_bag
        :param merge: if True, the data will be merged in. If not, it will be
                completely overwritten
        :param kitchen_name: Optional name of kitchen to write to.  default=kitchen
        """

        databags_root = os.path.join(kitchen_path, 'data_bags')
        if not os.path.exists(databags_root):
            msg = ("Data bags path does not exist: %s" % databags_root)
            #TODO(andrew-plunk): proper exception msg
            raise ValueError(msg)
        # Check if the bag already exists (create it if not)
        params = ['knife', 'solo', 'data', 'bag', 'list', '-F', 'json',
                  '-c', solo_config]
        #TODO(andrew-plunk) check, removed environment
        self._run_kitchen_command(kitchen_path,
                             ['knife', 'solo', 'data', 'bag', 'create',
                             bagname, '-c', solo_config])
        logger.debug("Created data bag '%s' in '%s'", bagname, databags_root)

        if contents:
            if 'id' not in contents:
                contents['id'] = itemname
            elif contents['id'] != itemname:
                message = ("The value of the 'id' field in a "
                               "databag item is reserved by Chef "
                               "and must be set to the name of the "
                               "databag item. Heat will set "
                               "this for you if it is missing, but "
                               "the data you supplied included an "
                               "ID that did not match the databag "
                               "item name. The ID was '%s' and the "
                               "databag item name was '%s'" % (contents['id'],
                                                               itemname))
                raise ValueError(message)

            if isinstance(contents, dict):
                contents_str = json.dumps(contents)
            params = ['knife', 'solo', 'data', 'bag', 'create', bagname,
                      itemname, '-d', '-c', solo_config, '--json',
                      contents_str]
            if secret_file:
                params.extend(['--secret-file', secret_file])
            result = self._run_kitchen_command(kitchen_path, params)
            logger.debug(result)
        else:
            logger.warning("write_databag was called with no contents")

    #TODO(andrew-plunk)
    def manage_role(self, name, kitchen_path, path=None, desc=None,
                    run_list=None, default_attributes=None,
                    override_attributes=None, env_run_lists=None):
        """Write/Update role."""

        role_path = os.path.join(kitchen_path, 'roles', '%s.json' % name)

        if os.path.exists(role_path):
            with file(role_path, 'r') as role_file_r:
                role = json.load(role_file_r)
            if run_list is not None:
                role['run_list'] = run_list
            if default_attributes is not None:
                role['default_attributes'] = default_attributes
            if override_attributes is not None:
                role['override_attributes'] = override_attributes
            if env_run_lists is not None:
                role['env_run_lists'] = env_run_lists
        else:
            role = {
                "name": name,
                "chef_type": "role",
                "json_class": "Chef::Role",
                "default_attributes": default_attributes or {},
                "description": desc,
                "run_list": run_list or [],
                "override_attributes": override_attributes or {},
                "env_run_lists": env_run_lists or {}
            }

        logger.debug("Writing role '%s' to %s", name, role_path)
        with file(role_path, 'w') as role_file_w:
            json.dump(role, role_file_w)

    def prepare_ssh_config(self, host, identity_file, user, kitchen_path):
        ssh_config_path = os.path.join(kitchen_path, 'ssh_config')
        with file(ssh_config_path, 'w') as ssh_config:
            ssh_config.write("Host %(host)s\n"
                             " User %(user)s\n"
                             " Hostname %(host)s\n"
                             " IdentityFile %(identity_file)s\n" % 
                                {'host': host,
                                 'identity_file': identity_file,
                                 'user': user})
        return ssh_config_path

    def write_node_json(self, kitchen_path, name, node_json):
        #TODO(andrew-plunk): this is to conform with checkmate... remove
        node_json['deployment'] = {'id': self._future_resource_id}
        node_json['run_list'].append('recipe[chef-solo-search]')
        node_json_path = os.path.join(kitchen_path, "nodes", name + ".json")
        with file(node_json_path, 'w') as json_file:
            json_file.write(json.dumps(node_json))

    def write_roles(self, kitchen_path, roles):
        for role in roles:
            role_path = os.path.join(kitchen_path, "roles", role + ".json")
            with file(role_path, 'w') as role_file:
                role_file.write(json.dumps(role))

    #TODO: we are returning relative paths here.... is that right?
    def _generate_chef_secrets_file(self, kitchen_path):
        secret_key_path = os.path.join(kitchen_path, "secrets.pem")
        key = RSA.generate(2048)
        self.secret_key = key.exportKey('PEM')
        print("Generated secrets private key")
        with file(secret_key_path, 'w') as secret_key_file_w:
            secret_key_file_w.write(self.secret_key)
        return 'certificates/secrets.pem'

    #TODO: we are returning relative paths here.... is that right?
    def _create_environment_keys(self, kitchen_path, private_key, public_key):
        """Put keys in an existing environment

        If none are provided, a new set of public/private keys are created
        """
        key_path = os.path.join(kitchen_path, 'certificates')
        if not os.path.exists(key_path):
            os.mkdir(key_path, 0o770)
        else:
            os.chmod(key_path, 0o770)
        #private key
        private_key_path = os.path.join(key_path, 'heat_rsa')
        with file(private_key_path, 'w') as pk_file:
                pk_file.write(private_key)
        print("Wrote environment private key: %s", private_key_path)

        os.chmod(private_key_path, 0o600)
        print("Private cert permissions set: chmod 0600 %s", private_key_path)

        #public_key
        public_key_path = os.path.join(key_path, 'heat_rsa.pub')
        with file(public_key_path, 'w') as public_key_file_w:
            public_key_file_w.write(public_key)
        print("Wrote environment public key: %s", public_key_path)

        #chef secrets
        secrets_file_path = self._generate_chef_secrets_file(key_path)
        
        return dict(public_key_path=public_key_path,
                    private_key_path=private_key_path,
                    secrets_file_path=secrets_file_path) 

    def _write_knife_config_file(self, kitchen_path, remote_path, secret_key_path):
        """Writes a solo.rb config file and links a knife.rb file too."""
        knife_config = """# knife -c knife.rb
    file_cache_path  "%s"
    cookbook_path    ["%s", "%s"]
    role_path  "%s"
    data_bag_path  "%s"
    log_level        :info
    log_location     "%s"
    verbose_logging  true
    ssl_verify_mode  :verify_none
    encrypted_data_bag_secret "%s"
    """ % (remote_path,
           os.path.join(remote_path, 'cookbooks'),
           os.path.join(remote_path, 'site-cookbooks'),
           os.path.join(remote_path, 'roles'),
           os.path.join(remote_path, 'data_bags'),
           os.path.join(remote_path, 'knife-solo.log'),
           secret_key_path)
        # knife kitchen creates a default solo.rb, so the file already exists
        solo_file = os.path.join(kitchen_path, 'solo.rb')
        with file(solo_file, 'w') as handle:
            handle.write(knife_config)
        logger.debug("Created solo file: %s", solo_file)
        return solo_file

    def _create_kitchen(self, environment_dir, kitchen_path, remote_path, 
                        secret_key_path=None,
                        source_repo=None):
        if not os.path.exists(kitchen_path):
            os.mkdir(kitchen_path, 0o770)
            logger.debug("Created kitchen directory: %s", kitchen_path)
        else:
            logger.debug("Kitchen directory exists: %s", kitchen_path)

        params = ['knife', 'solo', 'init', '.']
        self._run_kitchen_command(kitchen_path, params)

        #todo check this, does it have to be a fully qualified path?
        #TODO remove
        # remote_config_file = self._write_knife_config_file(kitchen_path,
        #                                           remote_path,
        #                                           os.path.join(remote_path,
        #                                             secret_key_path))
        remote_config_file = self._write_knife_config_file(kitchen_path,
                                                          kitchen_path,
                                                          os.path.join(
                                                            kitchen_path,
                                                            secret_key_path))

        # Create bootstrap.json in the kitchen
        bootstrap_path = os.path.join(kitchen_path, 'bootstrap.json')
        if not os.path.exists(bootstrap_path):
            with file(bootstrap_path, 'w') as the_file:
                json.dump({"run_list": ["recipe[build-essential]"]}, the_file)

        # Knife defaults to knife.rb, but knife-solo looks for solo.rb, so we link
        # both files so that knife and knife-solo commands will work and anyone
        # editing one will also change the other
        knife_file = os.path.join(kitchen_path, 'knife.rb')
        if os.path.exists(knife_file):
            logger.debug("Knife.rb already exists: %s", knife_file)
        else:
            os.link(remote_config_file, knife_file)
            logger.debug("Linked knife.rb: %s", knife_file)

        logger.debug("Finished creating kitchen: %s", kitchen_path)
        #todo(andrew-plunk) removed secret key path
        return {"kitchen": kitchen_path,
                "remote_solo": remote_config_file}

    #TODO(andrew-plunk): taken from cloud_servers... move into common class
    def _run_ssh_command(self, username, host, command, private_key_path=None):
        """Run a shell command on the Cloud Server via SSH."""
        if not private_key_path:
            with tempfile.NamedTemporaryFile() as private_key_file:
                private_key_file.write(self.private_key)
                private_key_file.seek(0)
            private_key_path = private_key_file.name

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        ssh.connect(host,
                    username=username,
                    key_filename=private_key_path)
        stdin, stdout, stderr = ssh.exec_command(command)
        logger.debug(stdout.read())
        logger.debug(stderr.read())

    def create_chef_environment(self, resource_id):
        environment = os.path.join(os.getcwd(), ".heat_chef")
        if not os.path.exists(environment):
            os.mkdir(environment, 0o770)

        environment_dir = os.path.join(environment, resource_id)
        os.mkdir(environment_dir, 0o770)

        kitchen_path = os.path.join(environment_dir, 'kitchen')
        os.mkdir(kitchen_path, 0o770)

        key_data = self._create_environment_keys(kitchen_path,
                                                 self.properties['private_key'],
                                                 self.properties['public_key']
                                                 )

        remote_path = os.path.join("/", self.properties['username'], 'kitchen')
        secret_key_path = key_data['secrets_file_path']
        kitchen_env = self._create_kitchen(environment_dir, kitchen_path,
                                           remote_path,
                                           secret_key_path=secret_key_path)

        ssh_config_path = self.prepare_ssh_config(self.properties['hostname'],
                                                  key_data['private_key_path'],
                                                  self.properties['username'],
                                                  environment_dir)

        self._install_cookbooks(kitchen_path)
        return {
            'environment': environment_dir,
            'kitchen': kitchen_path,
            'secret_key': key_data['secrets_file_path'],
            'ssh_config': ssh_config_path,
            'solo_config': kitchen_env['remote_solo'],
            'remote_kitchen': remote_path,
            'private_key_path': key_data['private_key_path']
        }

    #TODO(andrew-plunk): see if this can be run multiple times, may have to
    #use cook/prepare
    def bootstrap(self, solo_path, kitchen_path, username, host, ssh_config_path):
        #TODO(andrew-plunk): check knife bootstrap with erb template to create directory
        params = ['knife', 'solo', 'bootstrap', '%s@%s' % (username, host),
              '-c', solo_path, "-F", ssh_config_path]
        #TODO(andrew-plunk): params.extend(['bootstrap.json'])
        self._run_kitchen_command(kitchen_path, params)

    #TODO andrew
    def cook(self, solo_path, kitchen_path, username, host, ssh_config_path):
        #TODO(andrew-plunk): check knife solo cook for
        params = ['knife', 'solo', 'cook', '%s@%s' % (username, host),
              '-c', solo_path, "-F", ssh_config_path]
        #TODO(andrew-plunk): params.extend(['cook.json'])
        self._run_kitchen_command(kitchen_path, params)

    def handle_create(self):
        #TODO(andrew-plunk) try to setup chef env in init, this will let us
        #do it in parallel with the server creation. You may have to create
        #deferred attributes
        self.env = self.create_chef_environment(self._future_resource_id)
        if self.properties.get('data_bags'):
            self.write_databags(self._future_resource_id,
                                self.properties['data_bags'],
                                self.env['kitchen'],
                                self.env['secret_key'],
                                self.env['solo_config'])

        #todo solo_config
        if self.properties.get('node_json'):
            self.write_node_json(self.env['kitchen'],
                                 self.properties['hostname'],
                                 self.properties.get('node_json'))

        if self.properties.get('roles'):
            self.write_roles(self.properties.get('roles'))

        #create remote kitchen path
        #TODO this is crazy, creating the remote path to match the server path...
        #find a fix
        self._run_ssh_command(self.properties['username'],
                              self.properties['hostname'],
                              'mkdir -p ' + self.env['kitchen'],
                              private_key_path=self.env['private_key_path'])
        #TODO REMOVE, should be done by build-install cookbook
        self._run_ssh_command(self.properties['username'],
                              self.properties['hostname'],
                              'apt-get install make',
                              private_key_path=self.env['private_key_path'])
        self.bootstrap(self.env['solo_config'],
                       self.env['kitchen'],
                       self.properties['username'],
                       self.properties['hostname'],
                       self.env['ssh_config'])
        self.resource_id_set(self._future_resource_id)

def resource_mapping():
    return {
        'OS::Nova::ChefSolo': ChefSolo
    }


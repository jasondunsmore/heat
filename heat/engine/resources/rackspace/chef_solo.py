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
import re
import json
import os
import uuid
import subprocess
import errno
import shutil
from Crypto.PublicKey import RSA

from heat.engine import resource
from heat.common import exception

from heat.openstack.common import log as logging

logger = logging.getLogger(__name__)

class ChefSolo(resource.Resource):
    properties_schema = {
        #TODO(andrew-plunk): custom valiation only berks or chef not both
        'Berksfile': {'Type': 'String'},
        'Cheffile': {'Type': 'String'}
    }

    #TODO(andrew-plunk): define the properties schema correctly
    #TODO(andrew-plunk): custom server validation, type required
    #TODO(andrew-plunk): fix solo_config to be map turned into string,
    #or set variables for json_attribs
    def _write_knife_config_file(self, kitchen_path):
        """Writes a solo.rb config file and links a knife.rb file too."""
        secret_key_path = os.path.join(kitchen_path, 'certificates', 'chef.pem')
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
    """ % (kitchen_path,
           os.path.join(kitchen_path, 'cookbooks'),
           os.path.join(kitchen_path, 'site-cookbooks'),
           os.path.join(kitchen_path, 'roles'),
           os.path.join(kitchen_path, 'data_bags'),
           os.path.join(kitchen_path, 'knife-solo.log'),
           secret_key_path)
        # knife kitchen creates a default solo.rb, so the file already exists
        solo_file = os.path.join(kitchen_path, 'solo.rb')
        with file(solo_file, 'w') as handle:
            handle.write(knife_config)
        logger.debug("Created solo file: %s", solo_file)
        return (solo_file, secret_key_path)


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

    def _run_kitchen_command(self, kitchen_path, params, lock=True):
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

    def _create_kitchen(self, service_name, path, secret_key=None,
                        source_repo=None):
        """Creates a new knife-solo kitchen in path

        Arguments:
        - `name`: The name of the kitchen
        - `path`: Where to create the kitchen
        - `source_repo`: URL of the git-hosted blueprint
        - `secret_key`: PEM-formatted private key for data bag encryption
        """
        if not os.path.exists(path):
            #TODO: real error
            logger.error("Invalid path: %s" % path)

        kitchen_path = os.path.join(path, service_name)

        if not os.path.exists(kitchen_path):
            os.mkdir(kitchen_path, 0o770)
            logger.debug("Created kitchen directory: %s", kitchen_path)
        else:
            logger.debug("Kitchen directory exists: %s", kitchen_path)

        nodes_path = os.path.join(kitchen_path, 'nodes')
        if os.path.exists(nodes_path):
            if any((f.endswith('.json') for f in os.listdir(nodes_path))):
                msg = ("Kitchen already exists and seems to have nodes defined "
                       "in it: %s" % nodes_path)
                logger.debug(msg)
                #TODO(andrew-plunk) we probably don't want to do this
                return {"kitchen": kitchen_path}
        else:
            # we don't pass the config file here because we're creating the
            # kitchen for the first time and knife will overwrite our config file
            params = ['knife', 'solo', 'init', '.']
            self._run_kitchen_command(kitchen_path, params)

        #todo check this, does it have to be a fully qualified path?
        solo_file, secret_key_path = self._write_knife_config_file(kitchen_path)

        # Create bootstrap.json in the kitchen
        bootstrap_path = os.path.join(kitchen_path, 'bootstrap.json')
        if not os.path.exists(bootstrap_path):
            with file(bootstrap_path, 'w') as the_file:
                json.dump({"run_list": ["recipe[build-essential]"]}, the_file)

        # Create certificates folder
        certs_path = os.path.join(kitchen_path, 'certificates')
        if os.path.exists(certs_path):
            logger.debug("Certs directory exists: %s", certs_path)
        else:
            os.mkdir(certs_path, 0o770)
            logger.debug("Created certs directory: %s", certs_path)

        # Store (generate if necessary) the secrets file
        if os.path.exists(secret_key_path):
            if secret_key:
                with file(secret_key_path, 'r') as secret_key_file_r:
                    data = secret_key_file_r.read(secret_key)
                if data != secret_key:
                    msg = ("Kitchen secrets key file '%s' already exists and does "
                           "not match the provided value" % secret_key_path)
                    #TODO(andrew-plunk) proper error
                    raise ValueError(msg)
            logger.debug("Stored secrets file exists: %s", secret_key_path)
        else:
            if not secret_key:
                key = RSA.generate(2048)
                secret_key = key.exportKey('PEM')
                logger.debug("Generated secrets private key")
            with file(secret_key_path, 'w') as secret_key_file_w:
                secret_key_file_w.write(secret_key)
            logger.debug("Stored secrets file: %s", secret_key_path)

        # Knife defaults to knife.rb, but knife-solo looks for solo.rb, so we link
        # both files so that knife and knife-solo commands will work and anyone
        # editing one will also change the other
        knife_file = os.path.join(kitchen_path, 'knife.rb')
        if os.path.exists(knife_file):
            logger.debug("Knife.rb already exists: %s", knife_file)
        else:
            os.link(solo_file, knife_file)
            logger.debug("Linked knife.rb: %s", knife_file)

        # Copy blueprint files to kitchen
        #if source_repo:
        #TODO(andrew-plunk)
        #    _ensure_kitchen_blueprint(kitchen_path, source_repo)
        logger.debug("Finished creating kitchen: %s", kitchen_path)
        return {"kitchen": kitchen_path,
                "secret_key": secret_key}

    def _create_environment_keys(self, environment_path, private_key=None,
                             public_key_ssh=None):
        """Put keys in an existing environment

        If none are provided, a new set of public/private keys are created
        """
        # Create private key
        private_key_path = os.path.join(environment_path, 'private.pem')
        if os.path.exists(private_key_path):
            # Already exists.
            if private_key:
                with file(private_key_path, 'r') as pk_file:
                    data = pk_file.read()
                if data != private_key:
                    msg = ("A private key already exists in environment %s and "
                           "does not match the value provided" % environment_path)
                    #TODO(andrew-plunk) proper exception
                    raise ValueError(msg)
        else:
            if private_key:
                with file(private_key_path, 'w') as pk_file:
                    pk_file.write(private_key)
                logger.debug("Wrote environment private key: %s", private_key_path)
            else:
                params = ['openssl', 'genrsa', '-out', private_key_path, '2048']
                result = subprocess.check_output(params)
                logger.debug(result)
                logger.debug("Generated environment private key: %s",
                          private_key_path)

        # Secure private key
        os.chmod(private_key_path, 0o600)
        logger.debug("Private cert permissions set: chmod 0600 %s", private_key_path)

        # Get or Generate public key
        public_key_path = os.path.join(environment_path, 'heat.pub')
        if os.path.exists(public_key_path):
            logger.debug("Public key exists. Retrieving it from %s", public_key_path)
            with file(public_key_path, 'r') as public_key_file_r:
                public_key_ssh = public_key_file_r.read()
        else:
            if not public_key_ssh:
                params = ['ssh-keygen', '-y', '-f', private_key_path]
                public_key_ssh = subprocess.check_output(params)
                logger.debug("Generated environment public key: %s", public_key_path)
            # Write it to environment
            with file(public_key_path, 'w') as public_key_file_w:
                public_key_file_w.write(public_key_ssh)
            logger.debug("Wrote environment public key: %s", public_key_path)
        return dict(public_key_ssh=public_key_ssh, public_key_path=public_key_path,
                    private_key_path=private_key_path) 

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

    def create_chef_environment(self):
        environment = os.path.join(os.getcwd(), ".heat_chef")
        if not os.path.exists(environment):
            os.mkdir(environment, 0o770)

        #TODO(andrew-plunk) resource id
        environment_dir = os.path.join(environment, str(uuid.uuid4()))
        os.mkdir(environment_dir, 0o770)

        #TODO(andrew-plunk): use already created ssh key
        key_data = self._create_environment_keys(environment_dir)
        #TODO(andrew-plunk): environment keys
        kitchen_name = 'kitchen'
        kitchen_data = self._create_kitchen(kitchen_name, environment_dir)

        # Copy environment public key to kitchen certs folder
        kitchen_key_path = os.path.join(kitchen_data['kitchen'],
                                        'certificates',
                                        'heat-environment.pub')
        shutil.copy(key_data['public_key_path'], kitchen_key_path)
        logger.debug("Wrote environment public key to kitchen: %s", kitchen_key_path)

        self._install_cookbooks(kitchen_data['kitchen'])
        return {
            'environment': environment_dir,
            'kitchen': kitchen_data['kitchen'],
            'secret_key': key_data['private_key_path']
        }

    #TODO(andrew-plunk) you changed kitchen path to kitchen name. Check
    #TODO(andrew-plunk) TEST
    #TODO(andrew-plunk) removed environment because kitchen path is fully qualified
    def write_databag(self, bagname, itemname, contents, kitchen_path,
                      secret_file=None):
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
        config_file = os.path.join(kitchen_path, 'solo.rb')
        params = ['knife', 'solo', 'data', 'bag', 'list', '-F', 'json',
                  '-c', config_file]
        #TODO(andrew-plunk) check, removed environment
        self._run_kitchen_command(kitchen_path,
                             ['knife', 'solo', 'data', 'bag', 'create',
                             bagname, '-c', config_file])
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
                      itemname, '-d', '-c', config_file, '--json',
                      contents_str]
            if secret_file:
                params.extend(['--secret-file', secret_file])
            result = self._run_kitchen_command(kitchen_path, params)
            logger.debug(result)
        else:
            logger.warning("write_databag was called with no contents")

    #TODO(andrew-plunk)
    def manage_role(self, name, kitchen_path, resource, path=None, desc=None,
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

    def write_node_json(self, node_json_path, node_json):
        with file(node_json_path) as json_file:
            json_file.write(json.dump(node_json))

    def write_databags(self, databags, kitchen_path, private_key_path):
        for app_id, databag in databags.iteritems():
            self.write_databag(self.stack_id, app_id, databag,
                               kitchen_path,
                               secret_file=private_key_path)

    def write_roles(self, kitchen_path, roles):
        for role in roles:
            with file(os.path.join(kitchen_path, "roles", role + ".json"))\
                as role_file:
                role_file.write(json.dumps(role))

    def handle_create(self):
        env = self.create_chef_environment()
        self.write_databags(self.properties.get('databags'), env['kitchen'],
                            secret_file=env['private_key_path'])
        self.write_node_json(os.path.join(env['environment'], 'node.json'),
                             self.properties.get('node_json'))
        self.write_roles(self.properties.get('roles'))

def resource_mapping():
    return {
        'OS::Nova::ChefSolo': ChefSolo
    }


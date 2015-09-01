# vim: tabstop=4 shiftwidth=4 softtabstop=4

#
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

import copy
import os
import tempfile
import time

from oslo_log import log as logging

from oslo_config import cfg
from oslo_utils import uuidutils

from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import properties
from heat.engine.resources.openstack.nova import server

import psexec  # noqa

LOG = logging.getLogger(__name__)


class WinServer(server.Server):
    '''
    Rackspace cloud Windows server resource.
    '''

    SAVE_ADMIN_PASS = 'save_admin_pass'
    PERSONALITY = 'personality'

    attributes_schema = copy.deepcopy(server.Server.attributes_schema)
    attributes_schema.update(
        {
            'privateIPv4': attributes.Schema(
                _('The private IPv4 address of the server.')),
            'admin_pass': attributes.Schema(
                _('The administrator password for the server.'),
                cache_mode=attributes.Schema.CACHE_NONE
            )
        }
    )

    cmd = 'netsh advfirewall firewall add rule name="Port 445"' \
        ' dir=in action=allow protocol=TCP localport=445'

    files = {"C:\\cloud-automation\\bootstrap.bat": cmd,
             "C:\\cloud-automation\\bootstrap.cmd": cmd,
             "C:\\rs-automation\\bootstrap.bat": cmd,
             "C:\\rs-automation\\bootstrap.cmd": cmd}

    properties_schema = copy.deepcopy(server.Server.properties_schema)
    properties_schema.update(
        {
            SAVE_ADMIN_PASS: properties.Schema(
                properties.Schema.BOOLEAN,
                _('True if the system should remember the admin password; '
                  'False otherwise.'),
                default=False
            )
        }
    )

    def __init__(self, name, json_snippet, stack):
        super(WinServer, self).__init__(name, json_snippet, stack)
        self._public_ip = None
        self._server = None
        self._process = None
        self._last_time_stamp = None
        self._retry_count = 0
        self._max_retry_limit = 10
        self._timeout_start = None
        self._server_up = False
        self._ps_script = None
        self._tmp_batch_file = None

    @property
    def server(self):
        if not self._server:
            self._server = self.nova().servers.get(self.resource_id)
        return self._server

    def _get_ip(self, ip_type):
        if ip_type in self.server.addresses:
            for ip in self.server.addresses[ip_type]:
                if ip['version'] == 4:
                    return ip['addr']

        raise exception.Error("Could not determine the %s IP of %s." %
                              (ip_type, self.properties[self.IMAGE]))

    @property
    def public_ip(self):
        """Return the public IP of the Cloud Server."""
        if not self._public_ip:
            self._public_ip = self._get_ip('public')

        return self._public_ip

    def handle_create(self):
        '''
        Create Rackspace Cloud Windows Server Instance.
        '''

        if self.properties[self.PERSONALITY]:
            self.properties.data[self.PERSONALITY].update(self.files)
        else:
            self.properties.data[self.PERSONALITY] = self.files

        self.properties.data[self.USER_DATA_FORMAT] = 'RAW'
        # create Windows server instance
        LOG.info("Creating Windows cloud server")

        security_groups = self.properties[self.SECURITY_GROUPS]

        user_data_format = self.properties[self.USER_DATA_FORMAT]
        ud_content = self.properties[self.USER_DATA]
        if self.user_data_software_config() or self.user_data_raw():
            if uuidutils.is_uuid_like(ud_content):
                # attempt to load the userdata from software config
                ud_content = self.get_software_config(ud_content)

        metadata = self.metadata_get(True) or {}

        if self.user_data_software_config():
            self._create_transport_credentials()
            self._populate_deployments_metadata(metadata)

        userdata = self.client_plugin().build_userdata(
            metadata,
            ud_content,
            user_data_format=user_data_format)

        flavor = self.properties[self.FLAVOR]
        availability_zone = self.properties[self.AVAILABILITY_ZONE]

        image = self.properties[self.IMAGE]
        if image:
            image = self.client_plugin('glance').get_image_id(image)

        flavor_id = self.client_plugin().get_flavor_id(flavor)

        instance_meta = self.properties[self.METADATA]
        if instance_meta is not None:
            instance_meta = self.client_plugin().meta_serialize(
                instance_meta)

        scheduler_hints = self.properties[self.SCHEDULER_HINTS]
        if cfg.CONF.stack_scheduler_hints:
            if scheduler_hints is None:
                scheduler_hints = {}
            scheduler_hints['heat_root_stack_id'] = self.stack.root_stack_id()
            scheduler_hints['heat_stack_id'] = self.stack.id
            scheduler_hints['heat_stack_name'] = self.stack.name
            scheduler_hints['heat_path_in_stack'] = self.stack.path_in_stack()
            scheduler_hints['heat_resource_name'] = self.name
        nics = self._build_nics(self.properties[self.NETWORKS])
        block_device_mapping = self._build_block_device_mapping(
            self.properties[self.BLOCK_DEVICE_MAPPING])
        block_device_mapping_v2 = self._build_block_device_mapping_v2(
            self.properties[self.BLOCK_DEVICE_MAPPING_V2])
        reservation_id = self.properties[self.RESERVATION_ID]
        disk_config = self.properties[self.DISK_CONFIG]
        admin_pass = self.properties[self.ADMIN_PASS] or None
        personality_files = self.properties[self.PERSONALITY]
        key_name = self.properties[self.KEY_NAME]

        server = None
        try:
            server = self.nova().servers.create(
                name=self._server_name(),
                image=image,
                flavor=flavor_id,
                key_name=key_name,
                security_groups=security_groups,
                userdata=userdata,
                meta=instance_meta,
                scheduler_hints=scheduler_hints,
                nics=nics,
                availability_zone=availability_zone,
                block_device_mapping=block_device_mapping,
                block_device_mapping_v2=block_device_mapping_v2,
                reservation_id=reservation_id,
                config_drive=self._config_drive(),
                disk_config=disk_config,
                files=personality_files,
                admin_pass=admin_pass)
        finally:
            # Avoid a race condition where the thread could be canceled
            # before the ID is stored
            if server is not None:
                self.resource_id_set(server.id)
                #  Server will not have an adminPass attribute if Nova's
                #  "enable_instance_password" config option is turned off
                if (self.properties.get(self.SAVE_ADMIN_PASS) and
                        hasattr(server, 'adminPass') and
                        server.adminPass):

                    self.data_set("admin_pass", server.adminPass,
                                  redact=True)

        return server.id

    def check_create_complete(self, resource_id):
        '''
        Check if cloud Windows server instance creation is complete.
        '''
        instance = self.nova().servers.get(resource_id)
        if not super(WinServer, self).check_create_complete(instance):
            return False

        if not self._is_time_to_get_status():
            return False

        #if not self._is_server_active(instance):
            #return False

        # server status is ACTIVE, but server may not be ready for network
        # connection, so wait until it is reachable or until timeout happens
        if not self._is_server_reachable(instance):
            return False

        if self._process is None:
            self._start_installation_process(instance)
            return False

        self._throw_if_installation_timed_out(instance)

        if self._process.is_alive():
            return False

        # installation completed, so do cleanup
        self._cleanup_script_files(self._ps_script, self._tmp_batch_file)

        if self._process.exit_code() != 0:
            LOG.info("Installation exitcode %s" % self._process.exit_code())
            msg = "Install error:%s" % self._process.std_out()
            if cfg.CONF.debug:
                msg += "\n%s %s exitcode:%s" % (self.public_ip,
                                                instance.adminPass,
                                                self._process.exit_code())
            self._close_smb_port(instance)
            raise exception.Error(msg)

        self._close_smb_port(instance)
        LOG.info("Server %s configuration completed." % self.resource_id)
        return True

    def _close_smb_port(self, instance):
        self._process = psexec.PsexecWrapper("Administrator",
                                             instance.adminPass,
                                             self.public_ip,
                                             "C:\\Windows")
        cmd_lines = 'netsh advfirewall firewall delete rule name="Port 445"\nexit\n'
        self._process.run_cmd(cmd_lines)
        # give few seconds to execute the command 
        time.sleep(5)
        if self._is_server_reachable(instance) == True:
            time.sleep(15)
        self._process.kill()        

    def _is_server_reachable(self, instance):
        if not self._server_up:
            if not self._timeout_start:
                self._timeout_start = time.time()
            if psexec.wait_net_service(self.public_ip, 445, timeout=5):
                self._server_up = True
                return True

            time_diff = time.time() - self._timeout_start
            if not self._server_up and time_diff >= 1500:
                self._close_smb_port(instance)
                raise exception.Error("Server is not accessible... timedout!")

            return False

        return True

    def _is_server_active(self, instance):
        try:
            if instance.status != 'ACTIVE':
                instance.get()  # get updated attributes
        except Exception as ex:
            if self._retry_count < self._max_retry_limit:
                LOG.info("Exception found in get status...going to retry.")
                self._retry_count += 1
                return False
            raise ex

        if instance.status == 'ERROR':
            raise exception.Error("Cloud server creation failed.")

        if instance.status != 'ACTIVE':
            return False

        return True

    def _throw_if_installation_timed_out(self, instance):
        if time.time() - self._timeout_start > 3600:
            LOG.info("Installation timed out")
            self._process.kill()
            self._cleanup_script_files(self._ps_script, self._tmp_batch_file)
            # Close the port before throwing
            self._close_smb_port(instance)
            raise exception.Error("Resource instalation timed out")

    def _start_installation_process(self, instance):
        LOG.info("Starting installation on windows server %s" % instance.name)
        self._timeout_start = time.time()
        # create a powershellscript with given user_data
        self._ps_script = self._userdata_ps_script(
            self.properties[self.USER_DATA])

        # create a batch file that launches given powershell script
        self._tmp_batch_file = self._wrapper_batch_script(
            os.path.basename(self._ps_script))

        self._process = psexec.PsexecWrapper("Administrator",
                                             instance.adminPass,
                                             self.public_ip,
                                             "C:\\Windows")
        cmd_lines = "put %s\nput %s\n%s\nexit\n" % (
            self._ps_script,
            self._tmp_batch_file,
            os.path.basename(self._tmp_batch_file))
        self._process.run_cmd(cmd_lines)

    def _is_time_to_get_status(self):
        if self._last_time_stamp is None:
            self._last_time_stamp = time.time()
            return True

        # For now get status for every 30secs
        if time.time() - self._last_time_stamp > 30:
            self._last_time_stamp = time.time()
            return True

        return False

    def _cleanup_script_files(self, ps_script, tmp_batch_file):
        # remove the temp powershell and batch script
        try:
            os.remove(ps_script)
        except:
            pass
        try:
            os.remove(tmp_batch_file)
        except:
            pass
        # Stack creation timeout may result in stale batch files in tmp folder
        # so, remove old .bat and .ps1 files from tmp folder
        path = tempfile.gettempdir()
        time_now = time.time()
        for script in [f for f in os.listdir(path)
                       if f.endswith(".bat") and not f.endswith(".ps1")]:
            try:
                scriptf = os.path.join(path, script)
                # remove files older than 7200sec (2hours)
                if time_now - os.stat(scriptf).st_mtime > 7200:
                    os.remove(scriptf)
            except Exception:
                pass

    def _userdata_ps_script(self, user_data):
        # create powershell script with user_data
        powershell_script = tempfile.NamedTemporaryFile(suffix=".ps1",
                                                        delete=False)

        powershell_script.write(user_data)
        ps_script_full_path = powershell_script.name
        powershell_script.close()
        return ps_script_full_path

    def _wrapper_batch_script(self, command):
        batch_file_command = "powershell.exe -executionpolicy unrestricted " \
            "-command .\%s" % command
        batch_file = tempfile.NamedTemporaryFile(suffix=".bat", delete=False)
        batch_file.write(batch_file_command)
        batch_file.close()
        return batch_file.name

    def _resolve_attribute(self, name):
        if name == 'privateIPv4' and self.resource_id:
            return self.client_plugin().get_ip(self.server, 'private', 4)
        if name == 'admin_pass':
            return self.data().get('admin_pass', '')

        return super(WinServer, self)._resolve_attribute(name)


def resource_mapping():
    return {'Rackspace::Cloud::WinServer': WinServer}


try:
    import pyrax  # noqa
except ImportError:
    def available_resource_mapping():
        return {}
else:
    def available_resource_mapping():
        if hasattr(psexec, "PsexecWrapper"):
            return {'Rackspace::Cloud::WinServer': WinServer}
        else:
            LOG.warn("psexec not available.")
            return {}

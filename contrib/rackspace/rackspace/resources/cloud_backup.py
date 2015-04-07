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

import json
import requests
from oslo_log import log as logging

from heat.common import exception
from heat.common.i18n import _
from heat.common.i18n import _LI
from heat.common.i18n import _LW
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support

LOG = logging.getLogger(__name__)


class RaxBackupRestAPI(object):
    def __init__(self, base_url, tenant_id, auth_token):
        self.base_url = base_url
        self.tenant_id = tenant_id
        self.headers = {'Content-Type': 'application/json',
                        'X-Auth-Token': auth_token}

    def create_backup_config(self, backup_config):
        resp = requests.post(
            self.base_url+"/%s/backup-configuration" % self.tenant_id,
            headers=self.headers,
            data=backup_config)
        if resp.status_code != 200:
            raise Exception(resp.text)

        return resp.json()

    def get_backup_config(self, backup_config_id):
        resp = requests.get(
            self.base_url+"/%s/backup-configuration/%s" % (
                self.tenant_id, backup_config_id),
            headers=self.headers)
        if resp.status_code != 200:
            raise Exception(resp.text)

        return resp.json()

    def delete_backup_config(self, backup_config_id):
        resp = requests.delete(
            self.base_url+"/%s/backup-configuration/%s" % (
                self.tenant_id, backup_config_id),
            headers=self.headers)
        if resp.status_code != 200:
            raise Exception(resp.text)

    def update_backup_config(self, backup_config_id, updated_backup_config):
        resp = requests.put(
            self.base_url+"/%s/backup-configuration/%s" % (
                self.tenant_id, backup_config_id),
            headers=self.headers,
            data=updated_backup_config)
        if resp.status_code != 200:
            raise Exception(resp.text)

    def get_agent_list(self):
        resp = requests.get(self.base_url+"/user/agents",
                            headers=self.headers)
        return resp.json()

    def update_backup_config_status(self, backup_config_id, enabled=True):
        data = {"Enabled": enabled}
        resp = requests.post(
            self.base_url+"/%s/backup-configuration/enable/%s" % (
                self.tenant_id, backup_config_id),
            headers=self.headers,
            data=json.dumps(data))
        if resp.status_code != 200:
            raise Exception(resp.text)


class BackupConfig(resource.Resource):
    '''
    Rackspace cloud backup configuration resource.
    '''
    support_status = support.SupportStatus(version='2015.1')

    PROPERTIES = (
        HOST_IP_ADDRESS, BACKUP_CONFIGURATION_NAME,
        IS_ACTIVE, VERSION_RETENTION, FREQUENCY, START_TIME_HOUR,
        START_TIME_MIN, START_TIME_AM_PM, DAY_OF_WEEK_ID,
        HOUR_INTERVAL, TIME_ZONE_ID, NOTIFY_RECIPIENTS,
        NOTIFY_SUCCESS, NOTIFY_FAILURES, INCLUSIONS, EXCLUSIONS,
        ENABLED,
    ) = (
        'host_ip_address', 'BackupConfigurationName',
        'IsActive', 'VersionRetention', 'Frequency', 'StartTimeHour',
        'StartTimeMinute', 'StartTimeAmPm', 'DayOfWeekId',
        'HourInterval', 'TimeZoneId', 'NotifyRecipients',
        'NotifySuccess', 'NotifyFailure', 'Inclusions', 'Exclusions',
        'Enabled',
    )

    INCLUSION_EXCLUSION_KEYS = (
        FILE_PATH, FILE_ITEM_TYPE,
    ) = ('FilePath', 'FileItemType',)

    properties_schema = {
        ENABLED: properties.Schema(
            properties.Schema.BOOLEAN,
            _('Indicates backup configuration is enabled or not.'),
            default=True,
            update_allowed=True),
        HOST_IP_ADDRESS: properties.Schema(
            properties.Schema.STRING,
            _('Cloud server ip address.'),
            required=True),
        BACKUP_CONFIGURATION_NAME: properties.Schema(
            properties.Schema.STRING,
            _('Cloud backup configuration name.'),
            required=True),
        IS_ACTIVE: properties.Schema(
            properties.Schema.BOOLEAN,
            _('Indicates backup configuration is active.'),
            constraints=[
                constraints.AllowedValues([True, False]),
            ],
            default=True,
            update_allowed=True),
        VERSION_RETENTION: properties.Schema(
            properties.Schema.INTEGER,
            _('Indicates how many days backup revisions are maintained.'
              ' Valid values are 0, 30 , and 60. 0 means indefinite.'),
            constraints=[
                constraints.AllowedValues([0, 30, 60]),
            ],
            default=60,
            update_allowed=True),
        FREQUENCY: properties.Schema(
            properties.Schema.STRING,
            _('Frequency of backup schedule. Valid values are Manually, '
              'Hourly, Daily, and Weekly. '),
            constraints=[
                constraints.AllowedValues(
                    ['Manually', 'Hourly', 'Daily', 'Weekly']), ],
            default="Daily",
            update_allowed=True),
        START_TIME_HOUR: properties.Schema(
            properties.Schema.STRING,
            _('Indicates the hour when the backup runs. Valid values are 1 '
              'through 12, as well as null when the Frequency value is '
              '"Manually" or "Hourly". '),
            required=True,
            update_allowed=True),
        START_TIME_MIN: properties.Schema(
            properties.Schema.STRING,
            _('Indicates the minute when the backup runs. Valid values are 0 '
              'through 59, as well as null when the Frequency value is '
              '"Manually" or "Hourly". '),
            required=True,
            update_allowed=True),
        START_TIME_AM_PM: properties.Schema(
            properties.Schema.STRING,
            _('Indicates AM or PM. Valid values are "AM" or "PM", as well as '
              'null when the Frequency value is "Manually" or "Hourly".'),
            constraints=[
                constraints.AllowedValues(['AM', 'PM', '']),
            ],
            required=True,
            update_allowed=True),
        DAY_OF_WEEK_ID: properties.Schema(
            properties.Schema.STRING,
            _('Indicates the day of the week. Valid values are 0 through 6, '
              'with 0 representing Sunday and 6 representing Saturday. '
              'null is also a valid value when the Frequency value is '
              '"Manually" ,"Hourly", or "Daily".'),
            required=True,
            update_allowed=True),
        HOUR_INTERVAL: properties.Schema(
            properties.Schema.STRING,
            _('Indicates the hour. Valid values are 1 through 23, as well '
              'as null when the Frequency value is "Manually" ,"Daily", '
              'or "Weekly".'),
            required=True,
            update_allowed=True),
        TIME_ZONE_ID: properties.Schema(
            properties.Schema.STRING,
            _('Specifies the time zone where the backup runs, for example '
              '"Eastern Standard Time".'),
            default="Eastern Standard Time",
            required=True,
            update_allowed=True),
        NOTIFY_RECIPIENTS: properties.Schema(
            properties.Schema.STRING,
            _('Indicates the email address to notify in case of backup '
              'success or failure. '),
            required=True,
            update_allowed=True),
        NOTIFY_SUCCESS: properties.Schema(
            properties.Schema.BOOLEAN,
            _('Indicates if emails are sent after a successful backup. '
              'Valid values are true or false. '),
            default=False,
            update_allowed=True),
        NOTIFY_FAILURES: properties.Schema(
            properties.Schema.BOOLEAN,
            _('Indicates if emails are sent after a failed backup. '
              'Valid values are true or false. '),
            required=True,
            update_allowed=True),
        INCLUSIONS: properties.Schema(
            properties.Schema.LIST,
            _('Indicates the list of files and folders to back up.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    FILE_PATH: properties.Schema(
                        properties.Schema.STRING,
                        _('File  or folder path.')
                    ),
                    FILE_ITEM_TYPE: properties.Schema(
                        properties.Schema.STRING,
                        _('File item type.'),
                        constraints=[
                            constraints.AllowedValues(['Folder', 'File']),
                        ]                        
                    )
                }),
            required=True,
            update_allowed=True),
        EXCLUSIONS: properties.Schema(
            properties.Schema.LIST,
            _('Indicates the list of files and folders not to back up.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    FILE_PATH: properties.Schema(
                        properties.Schema.STRING,
                        _('File or folder path.')
                    ),
                    FILE_ITEM_TYPE: properties.Schema(
                        properties.Schema.STRING,
                        _('File item type.'),
                        constraints=[
                            constraints.AllowedValues(['Folder', 'File']),
                        ]                        
                    )
                }),
            required=False,
            update_allowed=True),
    }

    ATTRIBUTES = (
        BACKUP_AGENT_ID, BACKUP_CONFIG_DETAILS
    ) = ('backup_agent_id', 'backup_config_details', )
    attributes_schema = {
        BACKUP_AGENT_ID: attributes.Schema(
            _("Backup agent ID.")
        ),
        BACKUP_CONFIG_DETAILS: attributes.Schema(
            _("Backup config details.")
        ),
    }

    def __init__(self, name, json_snippet, stack):
        super(BackupConfig, self).__init__(name, json_snippet, stack)
        # TODO: should we get this from catalog instead of hardcoding?
        self.rax_rest_api = RaxBackupRestAPI(
            "https://backup.api.rackspacecloud.com/v1.0",
            self.context.tenant_id,
            self.context.auth_token)

    def handle_create(self):
        '''
        Create cloud  backup configuration.
        '''
        host_ip = self.properties[self.HOST_IP_ADDRESS]
        agent_list = self.rax_rest_api.get_agent_list()
        backup_agent_id = None
        for agent in agent_list:
            if agent['IPAddress'] == host_ip:
                backup_agent_id = agent['MachineAgentId']
                break

        if not backup_agent_id:
            raise Exception("Backup agent not found on %s" % host_ip)

        backup_config = {
            "MachineAgentId": backup_agent_id,
            "BackupConfigurationName": self.properties[
                self.BACKUP_CONFIGURATION_NAME],
            "IsActive": self.properties[self.IS_ACTIVE],
            "VersionRetention":  self.properties[self.VERSION_RETENTION],
            "MissedBackupActionId": 1,
            "Frequency": self.properties[self.FREQUENCY],
            "StartTimeHour": self.properties[self.START_TIME_HOUR],
            "StartTimeMinute": self.properties[self.START_TIME_MIN],
            "StartTimeAmPm": self.properties[self.START_TIME_AM_PM],
            "DayOfWeekId": self.properties[self.DAY_OF_WEEK_ID],
            "HourInterval": self.properties[self.HOUR_INTERVAL],
            "TimeZoneId": self.properties[self.TIME_ZONE_ID],
            "NotifyRecipients": self.properties[self.NOTIFY_RECIPIENTS],
            "NotifySuccess": self.properties[self.NOTIFY_SUCCESS],
            "NotifyFailure": self.properties[self.NOTIFY_FAILURES],
            "Inclusions": self.properties[self.INCLUSIONS],
            "Exclusions": self.properties[self.EXCLUSIONS]}

        backup_config = json.dumps(backup_config)
        resp = self.rax_rest_api.create_backup_config(backup_config)
        self.resource_id_set(resp['BackupConfigurationId'])
        self.data_set('backup_agent_id', backup_agent_id)
        if not self.properties[self.ENABLED]:
            self.rax_rest_api.update_backup_config_status(
                resp['BackupConfigurationId'], enabled=False)

    def handle_update(self, json_snippet, tmpl_diff, prop_diff):
        '''
        Update cloud  backup configuration.
        '''
        if self.ENABLED in prop_diff:
            self.rax_rest_api.update_backup_config_status(
                self.resource_id,
                prop_diff[self.ENABLED])

        prop_diff.pop(self.ENABLED, None)
        if not prop_diff:
            return

        properties = tmpl_diff['Properties']
        backup_config = {
            "MachineAgentId": self.data().get(self.BACKUP_AGENT_ID, ''),
            "BackupConfigurationName": properties[
                self.BACKUP_CONFIGURATION_NAME],
            "IsActive": properties[self.IS_ACTIVE],
            "VersionRetention":  properties[self.VERSION_RETENTION],
            "MissedBackupActionId": 1,
            "Frequency": properties[self.FREQUENCY],
            "StartTimeHour": properties[self.START_TIME_HOUR],
            "StartTimeMinute": properties[self.START_TIME_MIN],
            "StartTimeAmPm": properties[self.START_TIME_AM_PM],
            "DayOfWeekId": properties[self.DAY_OF_WEEK_ID],
            "HourInterval": properties[self.HOUR_INTERVAL],
            "TimeZoneId": properties[self.TIME_ZONE_ID],
            "NotifyRecipients": properties[self.NOTIFY_RECIPIENTS],
            "NotifySuccess": properties[self.NOTIFY_SUCCESS],
            "NotifyFailure": properties[self.NOTIFY_FAILURES],
            "Inclusions": properties.get(self.INCLUSIONS, None),
            "Exclusions": properties.get(self.EXCLUSIONS, None)}
        self.rax_rest_api.update_backup_config(self.resource_id,
                                               json.dumps(backup_config))

    def handle_delete(self):
        '''
        Delete cloud  backup configuration.
        '''
        if self.resource_id is None:
            return

        self.rax_rest_api.delete_backup_config(self.resource_id)

    def validate(self):
        '''
        Validate any of the provided params
        '''
        if self.properties[self.FREQUENCY] in ["Manually", "Hourly"]:
            if (self.properties[self.START_TIME_HOUR] or
                    self.properties[self.START_TIME_MIN] or
                    self.properties[self.START_TIME_AM_PM]):
                msg = (_("%s, %s, %s must be null if %s is set to 'Manually' "
                         "or 'Hourly'.") % (self.START_TIME_HOUR,
                                            self.START_TIME_MIN,
                                            self.START_TIME_AM_PM,
                                            self.FREQUENCY))
                raise exception.StackValidationFailed(message=msg)

        if self.properties[self.FREQUENCY] in ["Manually", "Daily"]:
            if (self.properties[self.DAY_OF_WEEK_ID] or
                    self.properties[self.HOUR_INTERVAL]):
                msg = (_("%s, %s must be null if %s is set to 'Manually', "
                         "'Hourly' or 'Daily'.") % (
                             self.DAY_OF_WEEK_ID, self.HOUR_INTERVAL,
                             self.FREQUENCY))
                raise exception.StackValidationFailed(message=msg)

    def _resolve_attribute(self, name):
        if name == self.BACKUP_AGENT_ID:
            return self.data().get(self.BACKUP_AGENT_ID, '')

        if name == self.BACKUP_CONFIG_DETAILS:
            return self.rax_rest_api.get_backup_config(self.resource_id)


def resource_mapping():
    return {
        'Rackspace::Cloud::BackupConfig': BackupConfig,
    }

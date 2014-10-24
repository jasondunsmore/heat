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

import abc
import copy
import six

from oslo_log import log as logging

from heat.common import exception
from heat.common.i18n import _
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.common.exception import StackValidationFailed

try:
    import pyrax  # noqa
    PYRAX_INSTALLED = True
except ImportError:
    PYRAX_INSTALLED = False

LOG = logging.getLogger(__name__)


@six.add_metaclass(abc.ABCMeta)
class CloudMonitoringResource(resource.Resource):
    """
    Common class for all Cloud Monitoring resources. It has definitions
    for shared properties, attributes, and client configuration.
    """

    default_client_name = "cloud_monitoring"

    COMMON_PROPS = (LABEL, ) = ("label", )

    common_prop_schema = {
        LABEL: properties.Schema(
            properties.Schema.STRING,
            _("A friendly label for this resource"),
            constraints=[
                constraints.Length(min=1, max=255)
            ],
            update_allowed=True)
    }

    ATTRIBUTES = (
        SHOW,
    ) = (
        "show",
    )

    attributes_schema = {
        SHOW: attributes.Schema(
            _("A dict of all entity details as returned by the API.")
        )
    }

    @abc.abstractmethod
    def _res_get(self):
        return None

    def handle_check(self):
        entity = self._res_get()
        if not entity:
            raise self.client_plugin().exception_module.NotFound()
        template = _("Value for property %s does not match; expected: %s, "
                     "actual: %s")
        for prop in self.properties:
            prop_val = self.properties.get(prop)
            if prop_val is not None:
                actual_val = getattr(entity, prop, None)
                message = template % (prop, prop_val, actual_val)
                assert prop_val == actual_val, message
                   
    def _resolve_attribute(self, name):
        if self.SHOW == name:
            phys_res = self._res_get()
            if phys_res:
                return phys_res._info


@six.add_metaclass(abc.ABCMeta)
class TypedMixIn(object):
    """
    Mix-in for resource classes for resources that have `type` and
    `details` properties. It has property schema definitions and
    a common implementation of `validate`.
    """

    _detail_schemas = {}
    _types = None
    _detail_ref = ""
    _type_constraint = ""

    TYPED_PROPERTIES = (TYPE, DETAILS) = ("type", "details")
    typed_schema = {
        TYPE: properties.Schema(
            properties.Schema.STRING,
            _("The specific type of resource"),
            required=True,
            constraints=[
                constraints.Length(min=1, max=64)
            ]
        ),
        DETAILS: properties.Schema(
            properties.Schema.MAP,
            _("A hash of type-specific details"),
            default={}
        ),
    }

    def __init__(self):
        constr = self.properties_schema[self.TYPE].constraints
        if len(constr) == 1:
            constr.append(constraints.CustomConstraint(self._type_constraint))
        if self._detail_ref:
            extra = _("A hash of type-specific details. "
                      "See %s") % self._detail_ref
            self.properties_schema[self.DETAILS].description = extra

    @abc.abstractmethod
    def _get_types(self):
        return {}

    def get_types(self):
        if not self._types:
            self._types = dict((t.id, t) for t
                               in self._get_types())
        return self._types
    
    def detail_schemas(self):
        if not self._detail_schemas:
            schemas = dict((ct.id,
                            dict((f["name"],
                                  properties.Schema(
                                      properties.Schema.STRING,
                                      f["description"],
                                      required=not f["optional"]))
                                 for f in ct.fields))
                           for ct in self.get_types().values())
            self._detail_schemas = schemas
        return self._detail_schemas

    def validate(self):
        detail_schemas = self.detail_schemas()
        try:
            det_prop_schema = detail_schemas[self.properties[self.TYPE]]
        except KeyError:
            message = _("Unknown type: %s")  % self.properties[self.TYPE]
            raise exception.StackValidationFailed(message=message)
        det_props = properties.Properties(det_prop_schema,
                                          self.properties[self.DETAILS],
                                          self.properties.resolve,
                                          self.DETAILS,
                                          self.context)
        det_props.validate()


class MetadataMixIn(object):
    """
    Mix-in for resource classes for resources with `metadata` properties
    """

    METADATA_PROPERTIES = (METADATA, ) = ("metadata",)
    metadata_schema = {
        METADATA: properties.Schema(
            properties.Schema.MAP,
            _("Arbitrary key/value pairs that are passed during the alerting"
              " phase. Both keys and values must be 255 characters or less."
              " Non-string values will be serialized to JSON (and the "
              "serialized string must be 255 characters or less)."),
            update_allowed=True
        )
    }


class AgentToken(CloudMonitoringResource):
    """
    Agent tokens are used to authenticate Monitoring agents to the Monitoring
    Service. Multiple agents can share a single token.
    """

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common

    def _res_get(self):
        if self.resource_id:
            return self.client().get_agent_token(self.resource_id)

    def handle_create(self):
        name = self.properties[self.LABEL] or self.physical_resource_name()
        token = self.client().create_agent_token(name)
        self.resource_id_set(token.id)

    def handle_update(self, json_snippet=None, tmpl_diff=None,
                      prop_diff=None):
        if self.LABEL in prop_diff:
            self.client().update_agent_token(self.resource_id,
                                             prop_diff[self.LABEL])

    def handle_delete(self):
        if self.resource_id:
            try:
                self.client().delete_agent_token(self.resource_id)
            except Exception as exc:
                self.client_plugin().ignore_not_found(exc)


class Entity(CloudMonitoringResource, MetadataMixIn):
    """
    An entity is the target of what you are monitoring. For example, you can
    create an entity to monitor your website, a particular web service, or
    your Rackspace server or server instance. Note that an entity represents
    only one item in the monitoring system. For example, if you wanted to
    monitor each server in a cluster, you would create an entity for each of
    the servers. You would not create a single entity to represent the entire
    cluster.
    
    An entity can have multiple checks associated with it. This allows you to
    check multiple services on the same host by creating multiple checks on the
    same entity, instead of multiple entities each with a single check.
    """

    PROPERTIES = (
        AGENT_ID,
        IP_ADDRESSES
    ) = (
        "agent_id",
        "ip_addresses"
    )

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common
    properties_schema.update(MetadataMixIn.metadata_schema)
    properties_schema.update({
        AGENT_ID: properties.Schema(
            properties.Schema.STRING,
            _("Agent to which this entity is bound"),
            constraints=[
                constraints.AllowedPattern("[-\.\w]+"),
                constraints.Length(min=1, max=255)
            ],
            update_allowed=True
        ),
        IP_ADDRESSES: properties.Schema(
            properties.Schema.MAP,
            _("IP addresses that can be referenced by checks on this entity."
              " Keys must be between 1 and 64 characters long. Values must be"
              " valid IPv4 or IPv6 addresses.")
        )
    })

    def _res_get(self):
        if self.resource_id:
            return self.client().get_entity(self.resource_id)

    def handle_create(self):
        entity = self.client().create_entity(
            label=self.properties[self.LABEL],
            agent=self.properties[self.AGENT_ID],
            ip_addresses=self.properties[self.IP_ADDRESSES],
            metadata=self.properties[self.METADATA]
        )
        self.resource_id_set(entity.id)

    def handle_update(self, json_snippet=None, tmpl_diff=None, prop_diff=None):
        if prop_diff is not None:
            self.client().update_entity(**prop_diff)

    def handle_delete(self):
        if self.resource_id:
            try:
                self.client().delete_entity(self.resource_id)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)


class Check(CloudMonitoringResource, TypedMixIn, MetadataMixIn):
    """
    A check is one of the foundational building blocks of the monitoring
    system. The check determines the parts or pieces of the entity that you
    want to monitor, the monitoring frequency, how many monitoring zones are
    originating the check, and so on.
    """

    _detail_ref = ("http://docs.rackspace.com/cm/api/v1.0/cm-devguide/"
                   "content/appendix-check-types.html")
    _type_constraint = "monitoring.checktype"

    PROPERTIES = (
        ENTITY,
        DISABLED,
        LABEL,
        METADATA,
        PERIOD,
        TIMEOUT,
        MONITORING_ZONES_POLL,
        TARGET_ALIAS,
        TARGET_HOSTNAME,
        TARGET_RECEIVER
        
    ) = (
        "entity",
        "disabled",
        "label",
        "metadata",
        "period",
        "timeout",
        "monitoring_zones_poll",
        "target_alias",
        "target_hostname",
        "target_receiver"
    )

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common
    properties_schema.update(copy.deepcopy(MetadataMixIn.metadata_schema))
    properties_schema.update(copy.deepcopy(TypedMixIn.typed_schema))
    properties_schema.update({
        ENTITY: properties.Schema(
            properties.Schema.STRING,
            _("The id of the entity for which to create the check. This can "
              "either be the id of a configured monitoring entity, a cloud "
              "server or a cloud database instance."),
            required=True
        ),
        DISABLED: properties.Schema(
            properties.Schema.BOOLEAN,
            _("Disables the check"),
            default=False,
            update_allowed=True
        ),
        PERIOD: properties.Schema(
            properties.Schema.INTEGER,
            _("The period in seconds for a check. The value must be greater "
              "than the minimum period set on your account."),
            constraints=[
                constraints.Range(min=30, max=1800)
            ],
            default=60,
            update_allowed=True
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.INTEGER,
            _("The timeout in seconds for a check. This has to be less than "
              "the period."),
            constraints=[
                constraints.Range(min=2, max=1800)
            ],
            default=30,
            update_allowed=True
        ),
        MONITORING_ZONES_POLL: properties.Schema(
            properties.Schema.LIST,
            _("List of monitoring zones to poll from. Note: This argument is "
              "only required for remote (non-agent) checks"),
            schema=properties.Schema(
                properties.Schema.STRING,
                constraints=[
                    constraints.CustomConstraint("monitoring.zone")
                ]
            )
        ),
        TARGET_ALIAS: properties.Schema(
            properties.Schema.STRING,
            _("A key in the entity's 'ip_addresses' hash used to resolve "
              "this check to an IP address. This parameter is mutually "
              "exclusive with target_hostname."),
            constraints=[
                constraints.Length(min=1, max=64)
            ]
        ),
        TARGET_HOSTNAME: properties.Schema(
            properties.Schema.STRING,
            _("The hostname this check should target. This parameter is "
              "mutually exclusive with target_alias. Value must be a Valid "
              "FQDN, IPv4 or IPv6 address")
        ),
        TARGET_RECEIVER: properties.Schema(
            properties.Schema.STRING,
            _("Determines how to resolve the check target."),
            constraints=[
                constraints.AllowedValues(["IPv4", "IPv6"])
            ],
            default="IPv4"
        )
    })

    def __init__(self, name, definition, stack):
        TypedMixIn.__init__(self)
        CloudMonitoringResource.__init__(self, name, definition, stack)

    def _get_types(self):
        return self.client().list_check_types()

    def _res_get(self):
        if self.resource_id:
            return self.client().get_check(self.properties[self.ENTITY],
                                           self.resource_id)

    def validate(self):
        CloudMonitoringResource.validate(self)
        TypedMixIn.validate(self)
        
        # validate period and timeout
        if self.properties[self.TIMEOUT] >= self.properties[self.PERIOD]:
            message = _("Timeout must be less than period.")
            raise exception.StackValidationFailed(message=message)
        
        check_type = self.get_types()[self.properties[self.TYPE]]
        if check_type.type == 'remote':
            # remote checks have to have monitoring zones
            if self.properties.get(self.MONITORING_ZONES_POLL) is None:
                message = (_("%s is required for remote checks.") %
                           self.MONITORING_ZONES_POLL)
                raise exception.StackValidationFailed(message=message)
            # target alias and target hostname are mutually exclusive
            if (self.properties[self.TARGET_HOSTNAME] and
                self.properties[self.TARGET_ALIAS]):
                message = (_("%s and %s are mutually exclusive.") %
                           (self.TARGET_ALIAS, self.TARGET_HOSTNAME))
                raise exception.StackValidationFailed(message=message)
            # but one is required
            if not (self.properties[self.TARGET_ALIAS] or
                    self.properties[self.TARGET_HOSTNAME]):
                message = (_("One of %s or %s is required for remote checks")
                           % (self.TARGET_ALIAS, self.TARGET_HOSTNAME))

    def _resolve_entity(self):
        try:
            return self.client().get_entity(self.properties[self.ENTITY])
        except Exception as ex:
            if self.client_plugin().is_client_exception(ex):
                # could be a server or db instance
                target = [e for e in self.client().list_entities()
                          if e.agent_id == self.properties[self.ENTITY]]
                if target:
                    return target[0]
            else:
                raise ex

    def handle_create(self):
        # we may have to wait on automatic entity
        # creation so defer to check
        return self._resolve_entity()

    def check_create_complete(self, entity):
        target = entity or self._resolve_entity()
        if target is not None:
            kwargs = dict((p, self.properties[p])
                      for p in self.properties
                      if p not in (self.ENTITY, self.TYPE))
            kwargs['check_type'] = self.properties[self.TYPE]
            self._format_zones(kwargs)
            check = self.client().create_check(target, **kwargs)
            self.resource_id_set(check.id)
            return True
        return False

    def handle_update(self, json_snippet=None, tmpl_diff=None, prop_diff=None):
        if prop_diff:
            self._format_zones(prop_diff)
            self.client().update_check(self._resolve_entity(),
                                       self.resource_id, **prop_diff)

    def _format_zones(self, params):
        if params.get(self.MONITORING_ZONES_POLL):
            zones = [z.id for z in self.client().list_monitoring_zones()
                     if (z.label in params[self.MONITORING_ZONES_POLL] or
                         z.id in params[self.MONITORING_ZONES_POLL])]
            # remove any dupes, but client has to have a list
            params[self.MONITORING_ZONES_POLL] = list(set(zones))

    def handle_delete(self):
        if self.resource_id:
            try:
                self.client().delete_check(self._resolve_entity(),
                                           self.resource_id)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)


class Notification(CloudMonitoringResource, TypedMixIn):
    """
    A notification is a destination to send an alarm, it can be a variety
    of different types, and will evolve over time.

    For instance, with a webhook type notification Rackspace Cloud Monitoring
    posts JSON formatted data to a user-specified URL on an alert condition
    (Check goes from `OK` -> `CRITICAL` and so on).
    """

    _detail_ref = ("http://docs.rackspace.com/cm/api/v1.0/cm-devguide/"
                   "content/service-notification-types-crud.html")
    _type_constraint = "monitoring.notificationtype"

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common
    properties_schema.update(copy.deepcopy(TypedMixIn.typed_schema))

    def __init__(self, name, definition, stack):
        TypedMixIn.__init__(self)
        CloudMonitoringResource.__init__(self, name, definition, stack)

    def _get_types(self):
        return self.client().list_notification_types()

    def _res_get(self):
        if self.resource_id:
            return self.client().get_notification(self.resource_id)

    def validate(self):
        CloudMonitoringResource.validate(self)
        TypedMixIn.validate(self)

    def handle_create(self):
        notification = self.client().create_notification(
            self.properties[self.TYPE],
            label=self.properties[self.LABEL],
            details=self.properties[self.DETAILS]
        )
        self.resource_id_set(notification.id)

    def handle_update(self, json_snippet=None, tmpl_diff=None, prop_diff=None):
        if prop_diff and self.DETAILS in prop_diff:
            self.client().update_notification(self.resource_id, prop_diff[self.DETAILS])

    def handle_delete(self):
        if self.resource_id:
            try:
                self.client().delete_notification(self.resource_id)
            except Exception as ex:
                self.client_plugin().ignore_not_found(ex)


class NotificationPlan(CloudMonitoringResource):
    """
    A notification plan contains a set of notification actions that Rackspace
    Cloud Monitoring executes when triggered by an alarm. Rackspace Cloud
    Monitoring currently supports webhook and email notifications.

    Each notification state can contain multiple notification actions. For
    example, you can create a notification plan that hits a webhook/email to
    notify your operations team if a warning occurs. However, if the warning
    escalates to an Error, the notification plan could be configured to hit a
    different webhook/email that triggers both email and SMS messages to the
    operations team. 
    """

    PROPERTIES = (
        CRITICAL_STATE,
        OK_STATE,
        WARNING_STATE
    ) = (
        "critical_state",
        "ok_state",
        "warning_state"
    )

    NP_SCHEMA = {
        CRITICAL_STATE: properties.Schema(
            properties.Schema.LIST,
            _("The notification list to send to when the state is CRITICAL."),
            update_allowed=True
        ),
        OK_STATE: properties.Schema(
            properties.Schema.LIST,
            _("The notification list to send to when the state is OK."),
            update_allowed=True
        ),
        WARNING_STATE: properties.Schema(
            properties.Schema.LIST,
            _("The notification list to send to when the state is WARNING."),
            update_allowed=True
        ),
    }

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common
    properties_schema.update(copy.deepcopy(NP_SCHEMA))

    def _res_get(self):
        if self.resource_id:
            return self.client().get_notification_plan(self.resource_id)

    def handle_create(self):
        kwargs = dict((p, self.properties[p]) for p in self.properties)
        plan = self.client().create_notification_plan(**kwargs)
        self.resource_id_set(plan.id)

    def handle_update(self, json_snippet=None, tmpl_diff=None, prop_diff=None):
        if prop_diff:
            kwargs = dict((p, self.properties[p]) for p in self.properties)
            self.client().update_notification_plan(self.resource_id, **kwargs)

    def handle_delete(self):
        return self.resource_id

    def check_delete_complete(self, resource_id):
        if resource_id:
            try:
                self.client().delete_notification_plan(resource_id)
            except Exception as exc:
                if self.client_plugin().is_client_exception(exc):
                    if self.client_plugin().is_not_found(exc):
                        return True
                    # will return Forbidden if we're waiting on alerts to
                    # be deleted
                    expected = ("Notification plans cannot be removed while "
                                "alarms are using it")
                    message = six.text_type(exc)
                    if expected in message:
                        return False
                raise exc
        return True


class PlanNotifications(CloudMonitoringResource):
    """
    Binds notifications to existing notification plans. This is useful
    for cases (such as using monitoring with autoscale), when you need
    a plan but must create the notifications dynamically later. Note that
    these notifications will overwrite any of the same level created
    as part of the NotificationPlan resource.
    """

    PN_PROPS = (
        PLAN
    ) = (
        "plan"
    )

    properties_schema = copy.deepcopy(NotificationPlan.NP_SCHEMA)
    properties_schema.update({
        PLAN: properties.Schema(
            properties.Schema.STRING,
            _("The notification plan to add notifications to"),
            required=True,
        )
    })

    attributes_schema = {}

    def _res_get(self):
        return None

    def validate(self):
        super(PlanNotifications, self).validate()
        if not [self.properties[p] for p in self.properties
                if p != self.PLAN]:
            raise StackValidationFailed(message="Must supply at least one"
                                        " notification")

    def handle_create(self):
        kwargs = dict((p, self.properties[p]) for p in self.properties
                      if p != self.PLAN)
        self.client().update_notification_plan(self.properties[self.PLAN],
                                               **kwargs)

    def handle_update(self, json_snippet=None, tmpl_diff=None,
                      prop_diff=None):
        if prop_diff:
            kwargs = dict((p, self.properties[p]) for p in self.properties
                      if p != self.PLAN)
            self.client().update_notification_plan(self.properties[self.PLAN],
                                                   **kwargs)


class Alarm(CloudMonitoringResource, MetadataMixIn):
    """
    Alarms bind alerting rules, entities, and notification plans into a
    logical unit. Alarms are responsible for determining a state (`OK`,
    `WARNING` or `CRITICAL`) based on the result of a Check, and executing a
    notification plan whenever that state changes. You create alerting rules
    by using the alarm DSL. For information about using the alarm language,
    refer to the `reference documentation <http://docs.rackspace.com/cm/api/
    v1.0/cm-devguide/content/alerts-language.html>`_.
    
    **Note** Criteria is optional. If you don't provide a criteria, the state
    of your alarm depends entirely on the success or failure of the check.
    This is a convenient shortcut for setting a simple alarm with a
    notification plan. For example, if you set a ping check on a server, it
    won't alert unless no pings are returned at all, whereas adding criteria
    would enable the alert to trigger if the ping round trip time went past a
    certain threshold.
    """

    PROPERTIES = (
        CHECK,
        PLAN,
        CRITERIA,
        DISABLED
    ) = (
         "check",
         "plan",
         "criteria",
         "disabled"
    )

    common = copy.deepcopy(CloudMonitoringResource.common_prop_schema)
    properties_schema = common
    properties_schema.update(copy.deepcopy(MetadataMixIn.metadata_schema))
    properties_schema.update({
        CHECK: properties.Schema(
            properties.Schema.STRING,
            _("The check to alert on"),
            required=True
        ),
        PLAN: properties.Schema(
            properties.Schema.STRING,
            _("The notification plan to execute when the state changes"),
            required=True
        ),
        CRITERIA: properties.Schema(
            properties.Schema.STRING,
            _("The alarm DSL for describing alerting conditions and their "
              "output states"),
            update_allowed=True
        ),
        DISABLED: properties.Schema(
            properties.Schema.BOOLEAN,
            _("Disable processing and alerts on this alarm"),
            default=False,
            update_allowed=True
        )
    })

    def _res_get(self):
        if self.resource_id:
            return self.client().get_alarm(self._find_entity(),
                                           self.resource_id)

    def _find_entity(self):
        if self.resource_id:
            return self.data().get("entity")
        if self.properties[self.CHECK]:
            check_id = self.properties[self.CHECK]
            # the client lib/api gives us no choice here
            for e in self.client().list_entities():
                if check_id in [c.id for c in e.list_checks()]:
                    return e.id

    def handle_create(self):
        entity_id = self._find_entity()
        if entity_id is None:
            raise Exception(_("Could not find parent entity of check %s")
                            % self.properties[self.CHECK])
        alarm = self.client().create_alarm(
                entity_id,
                self.properties[self.CHECK],
                self.properties[self.PLAN],
                criteria=self.properties[self.CRITERIA],
                disabled=self.properties[self.DISABLED],
                label=self.properties[self.LABEL],
                metadata=self.properties[self.METADATA]
        )
        self.resource_id_set(alarm.id)
        # cache entity id to save some lookups
        self.data_set("entity", entity_id)

    def handle_update(self, json_snippet=None, tmpl_diff=None,
                      prop_diff=None):
        if prop_diff:
            entity_id = self._find_entity()
            if entity_id is None:
                raise Exception(_("Could not find parent entity of check %s")
                                % self.properties[self.CHECK])
            self.client().update_alarm(
                entity_id,
                self.resource_id,
                **prop_diff
            )

    def handle_delete(self):
        if self.resource_id:
            # skip delete if the entity is already gone
            entity = self._find_entity()
            if entity:
                try:
                    self.client().delete_alarm(entity, self.resource_id)
                except Exception as exc:
                    self.client_plugin().ignore_not_found(exc)


def resource_mapping():
    if PYRAX_INSTALLED:
        return {
            "Rackspace::CloudMonitoring::AgentToken": AgentToken,
            "Rackspace::CloudMonitoring::Entity": Entity,
            "Rackspace::CloudMonitoring::Check": Check,
            "Rackspace::CloudMonitoring::Notification": Notification,
            "Rackspace::CloudMonitoring::NotificationPlan": NotificationPlan,
            "Rackspace::CloudMonitoring::PlanNotifications": PlanNotifications,
            "Rackspace::CloudMonitoring::Alarm": Alarm
        }
    return {}

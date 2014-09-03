from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine.resources import swiftsignal
from heat.openstack.common.gettextutils import _


class WaitCondition(swiftsignal.SwiftSignal):

    PROPERTIES = (HANDLE, TIMEOUT, COUNT,) = ('Handle', 'Timeout', 'Count',)

    properties_schema = {
        HANDLE: properties.Schema(
            properties.Schema.STRING,
            required=True,
            description=_('URL of TempURL where resource will signal '
                          'completion and optionally upload data.')
        ),
        TIMEOUT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The maximum number of seconds to wait for the '
                          'resource to signal completion.  Once the timeout '
                          'is reached, creation of the signal resource will '
                          'fail.'),
            required=True,
            constraints=[
                constraints.Range(1, 43200),
            ]
        ),
        COUNT: properties.Schema(
            properties.Schema.NUMBER,
            description=_('The number of success signals that must be '
                          'received before the stack creation process '
                          'continues.'),
            default=1,
            constraints=[
                constraints.Range(1, 1000),
            ]
        )
    }

    ATTRIBUTES = (DATA) = 'Data'

    attributes_schema = {
        DATA: attributes.Schema(
            _('JSON data that was uploaded via the SwiftSignalHandle.')
        )
    }


def resource_mapping():
    return {
        'AWS::CloudFormation::WaitCondition': WaitCondition,
        'AWS::CloudFormation::WaitConditionHandle':
        swiftsignal.SwiftSignalHandle
    }

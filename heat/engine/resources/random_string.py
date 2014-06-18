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

import random
import string

from six.moves import xrange

from heat.common import exception
from heat.engine import attributes
from heat.engine import constraints
from heat.engine import properties
from heat.engine import resource
from heat.engine import support
from heat.openstack.common.gettextutils import _


class RandomString(resource.Resource):
    '''
    A resource which generates a random string.

    This is useful for configuring passwords and secrets on services.
    '''
    PROPERTIES = (
        LENGTH, SEQUENCE, CHARACTER_CLASSES, CHARACTER_SEQUENCES,
        SALT,
    ) = (
        'length', 'sequence', 'character_classes', 'character_sequences',
        'salt',
    )

    _CHARACTER_CLASSES_KEYS = (
        CHARACTER_CLASSES_CLASS, CHARACTER_CLASSES_MIN, CHARACTER_CLASSES_MAX,
    ) = (
        'class', 'min', 'max',
    )

    _CHARACTER_SEQUENCES = (
        CHARACTER_SEQUENCES_SEQUENCE, CHARACTER_SEQUENCES_MIN,
        CHARACTER_SEQUENCES_MAX,
    ) = (
        'sequence', 'min', 'max',
    )

    ATTRIBUTES = (
        VALUE,
    ) = (
        'value',
    )

    properties_schema = {
        LENGTH: properties.Schema(
            properties.Schema.INTEGER,
            _('Length of the string to generate.'),
            default=32,
            constraints=[
                constraints.Range(1, 512),
            ]
        ),
        SEQUENCE: properties.Schema(
            properties.Schema.STRING,
            _('Sequence of characters to build the random string from.'),
            constraints=[
                constraints.AllowedValues(['lettersdigits', 'letters',
                                           'lowercase', 'uppercase',
                                           'digits', 'hexdigits',
                                           'octdigits']),
            ],
            support_status=support.SupportStatus(
                support.DEPRECATED,
                _('Use property %s.') % CHARACTER_CLASSES
            ),
            required=False
        ),
        CHARACTER_CLASSES: properties.Schema(
            properties.Schema.LIST,
            _('A list of character class and their constraints to generate '
              'the random string from.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    CHARACTER_CLASSES_CLASS: properties.Schema(
                        properties.Schema.STRING,
                        _('A character class and its corresponding min and max '
                          'constraints to generate the random string from.'),
                        constraints=[
                            constraints.AllowedValues(
                                ['lettersdigits', 'letters', 'lowercase',
                                 'uppercase', 'digits', 'hexdigits',
                                 'octdigits', 'punctuation']),
                        ],
                        default='lettersdigits'),
                    CHARACTER_CLASSES_MIN: properties.Schema(
                        properties.Schema.INTEGER,
                        _('The minimum number of characters from this '
                          'character class that will be in the generated '
                          'string.'),
                        default=1
                    ),
                    CHARACTER_CLASSES_MAX: properties.Schema(
                        properties.Schema.INTEGER,
                        _('The maximum number of characters from this '
                          'character class that will be in the generated '
                          'string.'),
                        required=False
                    ),
                }
            ),
            required=False
        ),
        CHARACTER_SEQUENCES: properties.Schema(
            properties.Schema.LIST,
            _('A list of character sequences and their constraints to '
              'generate the random string from.'),
            schema=properties.Schema(
                properties.Schema.MAP,
                schema={
                    CHARACTER_SEQUENCES_SEQUENCE: properties.Schema(
                        properties.Schema.STRING,
                        _('A character sequence and its corresponding min and '
                          'max constraints to generate the random string '
                          'from.'),
                        required=True),
                    CHARACTER_SEQUENCES_MIN: properties.Schema(
                        properties.Schema.INTEGER,
                        _('The minimum number of characters from this '
                          'sequence that will be in the generated '
                          'string.'),
                        required=True
                    ),
                    CHARACTER_SEQUENCES_MAX: properties.Schema(
                        properties.Schema.INTEGER,
                        _('The maximum number of characters from this '
                          'sequence that will be in the generated '
                          'string.'),
                        required=False
                    ),
                }
            )
        ),
        SALT: properties.Schema(
            properties.Schema.STRING,
            _('Value which can be set or changed on stack update to trigger '
              'the resource for replacement with a new random string . The '
              'salt value itself is ignored by the random generator.')
        ),
    }

    attributes_schema = {
        VALUE: attributes.Schema(
            _('The random string generated by this resource. This value is '
              'also available by referencing the resource.'),
            cache_mode=attributes.Schema.CACHE_NONE
        ),
    }

    _sequences = {
        'lettersdigits': string.ascii_letters + string.digits,
        'letters': string.ascii_letters,
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'hexdigits': string.digits + 'ABCDEF',
        'octdigits': string.octdigits,
        'punctuation': string.punctuation
    }

    @staticmethod
    def _generate_random_string(sequence, length):
        rand = random.SystemRandom()
        return ''.join(rand.choice(sequence) for x in xrange(length))

    @staticmethod
    def _random_string(char_sequences, char_classes, length):
        string = ""
        if char_sequences:
            for char_seq in char_sequences:
                seq = char_seq[self.CHARACTER_SEQUENCES_SEQUENCE]
                seq_min = char_seq[self.CHARACTER_SEQUENCES_MIN]
                seq_max = char_seq[self.CHARACTER_SEQUENCES_MAX]
                length = random.randrange(seq_min, seq_max + 1)
                for char in range(length):
                    

        if char_classes:
            pass

    def validate(self):
        sequence = self._sequences[self.properties.get(self.SEQUENCE)]
        char_sequences = self.properties.get(self.CHARACTER_SEQUENCES)
        char_classes = self.properties.get(self.CHARACTER_CLASSES)

        if sequence and (char_sequences or char_classes):
            msg = _("Cannot use deprecated 'sequence' property along with "
                    "'character_sequences' or 'character_classes' properties")
            raise exception.StackValidationFailed(message=msg)

    def handle_create(self):
        length = self.properties.get(self.LENGTH)
        sequence = self._sequences[self.properties.get(self.SEQUENCE)]
        char_sequences = self.properties.get(self.CHARACTER_SEQUENCES)
        char_classes = self.properties.get(self.CHARACTER_CLASSES)

        if sequence:  # Deprecated property was provided
            random_string = self._generate_random_string(sequence, length)
        elif char_sequences or char_classes:
            random_string = self._random_string(char_sequences, char_classes,
                                                length)
        else:  # Maintain old behavior
            random_string = self._generate_random_string("lettersdigits",
                                                         length)

        self.data_set('value', random_string, redact=True)
        self.resource_id_set(random_string)

    def _resolve_attribute(self, name):
        if name == self.VALUE:
            return self.data().get(self.VALUE)


def resource_mapping():
    return {
        'OS::Heat::RandomString': RandomString,
    }

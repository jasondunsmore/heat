
The ``heat.api.aws.utils`` Module
=================================

Helper utilities related to the AWS API implementations.

**heat.api.aws.utils.extract_param_list(params, prefix='')**

   Extract a list-of-dicts based on parameters containing AWS style
   list.

   MetricData.member.1.MetricName=buffers
   MetricData.member.1.Unit=Bytes MetricData.member.1.Value=231434333
   MetricData.member.2.MetricName=buffers2
   MetricData.member.2.Unit=Bytes MetricData.member.2.Value=12345

   This can be extracted by passing prefix=MetricData, resulting in a
   list containing two dicts.

**heat.api.aws.utils.extract_param_pairs(params, prefix='',
keyname='', valuename='')**

   Extract user input params from AWS style parameter-pair encoded
   list.

   In the AWS API list items appear as two key-value pairs (passed as
   query parameters)  with keys of the form below:

   Prefix.member.1.keyname=somekey Prefix.member.1.keyvalue=somevalue
   Prefix.member.2.keyname=anotherkey
   Prefix.member.2.keyvalue=somevalue

   We reformat this into a dict here to match the heat engine API
   expected format.

**heat.api.aws.utils.format_response(action, response)**

   Format response from engine into API format.

**heat.api.aws.utils.get_param_value(params, key)**

   Looks up an expected parameter in a parsed params dict.

   Helper function, looks up an expected parameter in a parsed params
   dict and returns the result.  If params does not contain the
   requested key we raise an exception of the appropriate type.

**heat.api.aws.utils.reformat_dict_keys(keymap=None, inputdict=None)**

   Utility function for mapping one dict format to another.

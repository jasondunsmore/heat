
The ``heat.api.aws.exception`` Module
*************************************

Heat API exception subclasses - maps API response errors to AWS
Errors.

**exception heat.api.aws.exception.AlreadyExistsError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Resource with the name requested already exists.

   ``code = 400``

   ``explanation = u'Resource with the name requested already
   exists'``

   ``title = 'AlreadyExists'``

**exception heat.api.aws.exception.HeatAPIException(detail=None)**

   Bases: ``webob.exc.HTTPError``

   webob HTTPError subclass that creates a serialized body.

   Subclass webob HTTPError so we can correctly serialize the wsgi
   response into the http response body, using the format specified by
   the request. Note this should not be used directly, instead use the
   subclasses defined below which map to AWS API errors.

   ``code = 400``

   ``err_type = 'Sender'``

   ``explanation = u'Generic HeatAPIException, please use specific
   subclasses!'``

   **get_unserialized_body()**

      Return a dict suitable for serialization in the wsgi controller.

      This wraps the exception details in a format which maps to the
      expected format for the AWS API.

   ``title = 'HeatAPIException'``

**exception
heat.api.aws.exception.HeatAPINotImplementedError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   API action is not yet implemented.

   ``code = 500``

   ``err_type = 'Server'``

   ``explanation = u'The requested action is not yet implemented'``

   ``title = 'APINotImplemented'``

**exception
heat.api.aws.exception.HeatAccessDeniedError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Authentication fails due to user IAM group memberships.

   This is the response given when authentication fails due to user
   IAM group memberships meaning we deny access.

   ``code = 403``

   ``explanation = u'User is not authorized to perform action'``

   ``title = 'AccessDenied'``

**exception
heat.api.aws.exception.HeatActionInProgressError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Cannot perform action on stack in its current state.

   ``code = 400``

   ``explanation = 'Cannot perform acti ... ctions are in progress'``

   ``title = 'InvalidAction'``

**exception
heat.api.aws.exception.HeatIncompleteSignatureError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The request signature does not conform to AWS standards.

   ``code = 400``

   ``explanation = u'The request signature does not conform to AWS
   standards'``

   ``title = 'IncompleteSignature'``

**exception
heat.api.aws.exception.HeatInternalFailureError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The request processing has failed due to some unknown error.

   ``code = 500``

   ``err_type = 'Server'``

   ``explanation = u'The request processing has failed due to an
   internal error'``

   ``title = 'InternalFailure'``

**exception
heat.api.aws.exception.HeatInvalidActionError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The action or operation requested is invalid.

   ``code = 400``

   ``explanation = u'The action or operation requested is invalid'``

   ``title = 'InvalidAction'``

**exception
heat.api.aws.exception.HeatInvalidClientTokenIdError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The X.509 certificate or AWS Access Key ID provided does not exist.

   ``code = 403``

   ``explanation = u'The certificate or AWS Key ID provided does not
   exist'``

   ``title = 'InvalidClientTokenId'``

**exception
heat.api.aws.exception.HeatInvalidParameterCombinationError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Parameters that must not be used together were used together.

   ``code = 400``

   ``explanation = u'Incompatible parameters were used together'``

   ``title = 'InvalidParameterCombination'``

**exception
heat.api.aws.exception.HeatInvalidParameterValueError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   A bad or out-of-range value was supplied for the input parameter.

   ``code = 400``

   ``explanation = u'A bad or out-of-range value was supplied'``

   ``title = 'InvalidParameterValue'``

**exception
heat.api.aws.exception.HeatInvalidQueryParameterError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   AWS query string is malformed, does not adhere to AWS standards.

   ``code = 400``

   ``explanation = u'AWS query string is malformed, does not adhere to
   AWS spec'``

   ``title = 'InvalidQueryParameter'``

**exception
heat.api.aws.exception.HeatMalformedQueryStringError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The query string is malformed.

   ``code = 404``

   ``explanation = u'The query string is malformed'``

   ``title = 'MalformedQueryString'``

**exception
heat.api.aws.exception.HeatMissingActionError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The request is missing an action or operation parameter.

   ``code = 400``

   ``explanation = u'The request is missing an action or operation
   parameter'``

   ``title = 'MissingAction'``

**exception
heat.api.aws.exception.HeatMissingAuthenticationTokenError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Does not contain a valid AWS Access Key or certificate.

   Request must contain either a valid (registered) AWS Access Key ID
   or X.509 certificate.

   ``code = 403``

   ``explanation = u'Does not contain a valid AWS Access Key or
   certificate'``

   ``title = 'MissingAuthenticationToken'``

**exception
heat.api.aws.exception.HeatMissingParameterError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   A mandatory input parameter is missing.

   An input parameter that is mandatory for processing the request is
   missing.

   ``code = 400``

   ``explanation = u'A mandatory input parameter is missing'``

   ``title = 'MissingParameter'``

**exception
heat.api.aws.exception.HeatOptInRequiredError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The AWS Access Key ID needs a subscription for the service.

   ``code = 403``

   ``explanation = u'The AWS Access Key ID needs a subscription for
   the service'``

   ``title = 'OptInRequired'``

**exception
heat.api.aws.exception.HeatRequestExpiredError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Request expired or more than 15 minutes in the future.

   Request is past expires date or the request date (either with 15
   minute padding), or the request date occurs more than 15 minutes in
   the future.

   ``code = 400``

   ``explanation = u'Request expired or more than 15mins in the
   future'``

   ``title = 'RequestExpired'``

**exception
heat.api.aws.exception.HeatServiceUnavailableError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   The request has failed due to a temporary failure of the server.

   ``code = 503``

   ``err_type = 'Server'``

   ``explanation = u'Service temporarily unavailable'``

   ``title = 'ServiceUnavailable'``

**exception heat.api.aws.exception.HeatSignatureError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Authentication fails due to a bad signature.

   ``code = 403``

   ``explanation = u'The request signat ... signature you provided'``

   ``title = 'SignatureDoesNotMatch'``

**exception heat.api.aws.exception.HeatThrottlingError(detail=None)**

   Bases: ``heat.api.aws.exception.HeatAPIException``

   Request was denied due to request throttling.

   ``code = 400``

   ``explanation = u'Request was denied due to request throttling'``

   ``title = 'Throttling'``

**heat.api.aws.exception.map_remote_error(ex)**

   Map rpc_common.RemoteError exceptions to HeatAPIException
   subclasses.

   Map rpc_common.RemoteError exceptions returned by the engine to
   HeatAPIException subclasses which can be used to return properly
   formatted AWS error responses.

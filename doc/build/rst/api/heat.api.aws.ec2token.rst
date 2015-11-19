
The ``heat.api.aws.ec2token`` Module
====================================

**class heat.api.aws.ec2token.EC2Token(app, conf)**

   Bases: ``heat.common.wsgi.Middleware``

   Authenticate an EC2 request with keystone and convert to token.

   ``ssl_options``

**heat.api.aws.ec2token.EC2Token_filter_factory(global_conf,
**local_conf)**

   Factory method for paste.deploy.

**heat.api.aws.ec2token.list_opts()**


The ``heat.engine.clients.progress`` Module
*******************************************

Helper classes that are simple key-value storages meant to be passed
between handle_* and check_*_complete, being mutated during subsequent
check_*_complete calls.

Some of them impose restrictions on client plugin API, thus they are
put in this client-plugin-agnostic module.

**class
heat.engine.clients.progress.PoolDeleteProgress(task_complete=False)**

   Bases: ``object``

**class heat.engine.clients.progress.ServerCreateProgress(server_id,
complete=False)**

   Bases: ``object``

**class heat.engine.clients.progress.ServerDeleteProgress(server_id,
image_id=None, image_complete=True)**

   Bases: ``object``

**class heat.engine.clients.progress.ServerUpdateProgress(server_id,
handler, complete=False, called=False, handler_extra=None,
checker_extra=None)**

   Bases: ``heat.engine.clients.progress.ServerCreateProgress``

   Keeps track on particular server update task.

   ``handler`` is a method of client plugin performing required update
   operation. Its first positional argument must be ``server_id`` and
   this method must be resilent to intermittent failures, returning
   ``True`` if API was successfully called, ``False`` otherwise.

   If result of API call is asynchronous, client plugin must have
   corresponding ``check_<handler>`` method. Its first positional
   argument must be ``server_id`` and it must return ``True`` or
   ``False`` indicating completeness of the update operation.

   For synchronous API calls, set ``complete`` attribute of this
   object to ``True``.

   ``[handler|checker]_extra`` arguments, if passed to constructor,
   should be dictionaries of

   ..

      {'args': tuple(), 'kwargs': dict()}

   structure and contain parameters with which corresponding
   ``handler`` and ``check_<handler>`` methods of client plugin must
   be called. ``args`` is automatically prepended with ``server_id``.
   Missing ``args`` or ``kwargs`` are interpreted as empty tuple/dict
   respectively. Defaults are interpreted as both ``args`` and
   ``kwargs`` being empty.

**class heat.engine.clients.progress.VolumeAttachProgress(srv_id,
vol_id, device, task_complete=False)**

   Bases: ``object``

**class
heat.engine.clients.progress.VolumeBackupRestoreProgress(vol_id,
backup_id)**

   Bases: ``object``

**class
heat.engine.clients.progress.VolumeDeleteProgress(task_complete=False)**

   Bases: ``object``

**class heat.engine.clients.progress.VolumeDetachProgress(srv_id,
vol_id, attach_id, task_complete=False)**

   Bases: ``object``

**class
heat.engine.clients.progress.VolumeResizeProgress(task_complete=False,
size=None)**

   Bases: ``object``

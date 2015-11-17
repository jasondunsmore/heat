
The ``heat.engine.plugin_manager`` Module
*****************************************

**class heat.engine.plugin_manager.PluginManager(*extra_packages)**

   Bases: ``object``

   A class for managing plugin modules.

   **map_to_modules(function)**

      Iterate over the results of calling a function on every module.

**class heat.engine.plugin_manager.PluginMapping(names, *args,
**kwargs)**

   Bases: ``object``

   A class for managing plugin mappings.

   **load_all(plugin_manager)**

      Iterate over the mappings from all modules in the plugin
      manager.

      Mappings are returned as a list of (key, value) tuples.

   **load_from_module(module)**

      Return the mapping specified in the given module.

      If no such mapping is specified, an empty dictionary is
      returned.

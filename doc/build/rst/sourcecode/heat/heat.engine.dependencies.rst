
The `heat.engine.dependencies <../../api/heat.engine.dependencies.rst#module-heat.engine.dependencies>`_ Module
===============================================================================================================

**exception
heat.engine.dependencies.CircularDependencyException(**kwargs)**

   Bases: ``heat.common.exception.HeatException``

   ``msg_fmt = u'Circular Dependency Found: %(cycle)s'``

**class heat.engine.dependencies.Dependencies(edges=None)**

   Bases: ``object``

   Helper class for calculating a dependency graph.

   **graph(reverse=False)**

      Return a copy of the underlying dependency graph.

   **leaves()**

      Return an iterator over all of the leaf nodes in the graph.

   **required_by(last)**

      List the keys that require the specified node.

   **requires(target)**

      List the keys that require the specified node.

   **roots()**

      Return an iterator over all of the root nodes in the graph.

   **translate(transform)**

      Translate all of the nodes using a transform function.

      Returns a new Dependencies object.

**class heat.engine.dependencies.Graph(*args)**

   Bases: ``collections.defaultdict``

   A mutable mapping of objects to nodes in a dependency graph.

   **copy()**

      Return a copy of the graph.

   **edges()**

      Return an iterator over all of the edges in the graph.

   **map(func)**

      Map the supplied function onto each node in the graph.

      Return a dictionary derived from mapping the supplied function
      onto each node in the graph.

   **reverse_copy()**

      Return a copy of the graph with the edges reversed.

   ``static toposort(graph)``

      Return a topologically sorted iterator over a dependency graph.

      This is a destructive operation for the graph.

**class heat.engine.dependencies.Node(requires=None,
required_by=None)**

   Bases: ``object``

   A node in a dependency graph.

   **copy()**

      Return a copy of the node.

   **disjoint()**

      Return True if this node is both a leaf and a stem.

   **required_by(source=None)**

      List the keys that require this node, and optionally add new
      one.

   **requires(target=None)**

      Add a key that this node requires, and optionally add a new one.

   **reverse_copy()**

      Return a copy of the node with the edge directions reversed.

   **stem()**

      Return True if this node is a stem (required by nothing).

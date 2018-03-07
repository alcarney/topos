VertexArrays
============

The :code:`VertexArray` family of objects are responsible for managing and
manipulating collections of vertices. Their use is identical the only
difference being which coordinate system you want to use.

.. todo::

    Link to explanations on the different systems we support and a discussion
    on which situations they are useful for.

Currently :code:`topos` comes with the following VertexArray Objects

- :code:`Cartesian`: For vertices using the :term:`cartesian coordinate` system
- :code:`Cylindrical`: For vertices using the :term:`cylindrical coordinate` system

Intialisation
-------------

The :code:`VertexArray` objects are just wrappers over a :term:`numpy array`
providing additional features that are useful when treating these arrays as a
list of vertices. So create your own vertex array simply pass a numpy array
with the right shape to one of these objects.

.. doctest:: ref-vertx-arrays

    >>> import numpy as np
    >>> from topos.vertices import Cartesian
    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> Cartesian(vs)
    Cartesian Array: 2 vertices

:code:`Cartesian` arrays are stored in the standard :math:`(x, y, z)` order.

Similarly for the :code:`Cylindrical` object

.. doctest:: ref-vertx-arrays

    >>> from topos.vertices import Cylindrical
    >>> Cylindrical(vs)
    Cylindrical Array: 2 vertices

.. note::

    For internal reasons :code:`Cylindrical` arrays are stored in
    :math:`(\theta, z, r)` format

Properties
----------

:code:`VertexArray` objects come with a number of properties which allow you to
easily retrieve information about particular arrays:

- :ref:`Cartesian - Read Only`
- :ref:`Data - Read Only`
- :ref:`Length - Read Only`
- :ref:`System - Read Only`

Cartesian - Read Only
^^^^^^^^^^^^^^^^^^^^^

Return a numpy array representing the vertices in Cartesian coordinates. If the
array is with respect to a different coordinate system the conversion will be
performed automatically.

.. doctest:: ref-vertx-arrays

    >>> vs = np.array([[1., 0., 3.], [0., 1. 4.]])
    >>> carts = Cartesian(vs)
    >>> carts.carteisan
    array([[1., 0., 3.],
           [0., 1., 4.])
    >>> cylins = Cylindrical(vs)
    >>> cylins.cartesian

Data - Read Only
^^^^^^^^^^^^^^^^

Return the raw data contained in the array

.. doctest:: ref-vertx-arrays

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.data
    array([1., 2., 3.],
          [4., 5., 6.])

Length - Read Only
^^^^^^^^^^^^^^^^^^

Return the number of vertices in an array

.. doctest:: ref-vertx-arrays

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.length
    2

System - Read Only
^^^^^^^^^^^^^^^^^^

Return a string representing the coordinate system the array is using

.. doctest:: ref-vertx-arrays

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cylindrical(vs)
    >>> verts.system
    "Cylindrical"

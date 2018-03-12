VertexArrays
============

The :code:`VertexArray` family of objects are responsible
for managing and manipulating collections of vertices. Their use is identical
the only difference being which coordinate system you want to use.

.. todo::

    Link to explanations on the different systems we support and a discussion
    on which situations they are useful for.

Currently :code:`topos` comes with the following VertexArray implementations

- :code:`Cartesian`: For vertices using the :term:`cartesian coordinate` system
- :code:`Cylindrical`: For vertices using the :term:`cylindrical coordinate`
  system

Intialisation
-------------

The :code:`VertexArray` objects are just wrappers over a :term:`numpy array`
providing additional features that are useful when treating these arrays as a
list of vertices. So create your own vertex array simply pass a numpy array
with the right shape to one of these objects.

.. doctest:: ref-vertx-array-init

    >>> import numpy as np
    >>> from topos.vertices import Cartesian
    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> Cartesian(vs)
    Cartesian Array: 2 vertices

:code:`Cartesian` arrays are stored in the standard :math:`(x, y, z)` order.

Similarly for the :code:`Cylindrical` object

.. doctest:: ref-vertx-array-init

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

.. testsetup:: ref-vertx-array-props

    import numpy as np
    from topos.vertices import Cartesian, Cylindrical

Return an array containing the vertices in Cartesian coordinates.

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[0., 2., 3.], [0., 1., 4.]])
    >>> carts = Cartesian(vs)
    >>> carts.cartesian
    array([[0., 2., 3.],
           [0., 1., 4.]])

Note that this will automatically convert vertex arrays that are not natively
using Cartesian coordinates

.. doctest:: ref-vertx-array-props

    >>> cylins = Cylindrical(vs)
    >>> cylins.cartesian
    array([[3., 0., 2.],
           [4., 0., 1.]])

Data - Read Only
^^^^^^^^^^^^^^^^

Return the raw data contained in the array

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.data
    array([[1., 2., 3.],
           [4., 5., 6.]])

X - Read Only
^^^^^^^^^^^^^

Return an array of just x coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.x
    array([1., 4.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

Y - Read Only
^^^^^^^^^^^^^

Return an array of just y coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.y
    array([2., 5.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

Z - Read Only
^^^^^^^^^^^^^

Return an array of just z coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.z
    array([3., 6.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

R - Read Only
^^^^^^^^^^^^^

Return an array of just r coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[0, 4., 2.], [0., 2., 1.]])
    >>> verts = Cylindrical(vs)
    >>> verts.r
    array([2., 1.])

Like the :code:`cylindrical` property this will automatically convert vertex
arrays that are not using Cylindrical coordinates

T - Read Only
^^^^^^^^^^^^^

Return an array of just t coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[0, 4., 2.], [0., 2., 1.]])
    >>> verts = Cylindrical(vs)
    >>> verts.t
    array([0., 0.])

Like the :code:`cylindrical` property this will automatically convert vertex
arrays that are not using Cylindrical coordinates

Length - Read Only
^^^^^^^^^^^^^^^^^^

Return the number of vertices in an array

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.length
    2

System - Read Only
^^^^^^^^^^^^^^^^^^

Return a string representing the coordinate system the array is using

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cylindrical(vs)
    >>> verts.system
    'Cylindrical'


Operations
----------

:code:`VertexArrays` support a number of arithmetic operations

Addition
^^^^^^^^

.. testsetup:: ref-vertx-array-addition

    import numpy as np
    from topos.vertices import Cartesian, Cylindrical

:code:`VertexArrays` support addition with a number of different objects, each
with their own behavior:

- :ref:`Addition with Other VertexArrays`
- :ref:`Addition with a Numpy Array`

Addition with Other VertexArrays
""""""""""""""""""""""""""""""""

.. doctest:: ref-vertx-array-addition

    >>> us = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> US = Cartesian(us)

    >>> vs = np.array([[7., 8., 9.]])
    >>> VS = Cartesian(vs)

    >>> US + VS
    Cartesian Array: 3 vertices

Where adding two arrays together creates a new array containing the vertices
from both arrays. Note that this works even if the arrays are using different
coordinate systems.

.. doctest:: ref-vertx-array-addition

    >>> us = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> US = Cartesian(us)

    >>> vs = np.array([[0., 2., 4.]])
    >>> VS = Cylindrical(vs)

    >>> AS = US + VS
    >>> AS.data
    array([[4., 0., 2.],
           [1., 2., 3.],
           [4., 5., 6.]])

When combining arrays that use different coordinate systems, the resulting
array will use the coordinate system of the first array and vertices from the
second will automatically be converted

.. doctest:: ref-vertx-array-addition

    >>> AS.system
    'Cartesian'

Addition with a Numpy Array
"""""""""""""""""""""""""""

:code:`VetexArray` objects also support addition with a numpy array. In this
case the shape of the numpy array *must* be :code:`(3,)` and the array is added
to each vertex in the array individually. This is typically useful when
translating an object in space.

.. doctest:: ref-vertx-array-addition

    >>> vs = np.array([[1., 2., 3], [4., 5., 6.]])
    >>> VS = Cartesian(vs)
    >>> US = VS + np.array([1., -2., 4.])
    >>> US.data
    array([[ 2.,  0.,  7.],
           [ 5.,  3., 10.]])

However since a numpy array does not carry coordinate system information so it
cannot be automatically converted. It is up to the user to ensure the numpy
array is using the correct coordinate system.


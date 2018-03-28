.. _use_ref_vertx_array:

VertexArrays
============

The :code:`VertexArray` family of objects are responsible
for managing and manipulating collections of vertices. Their use is identical
the only difference being which coordinate system you want to use.

.. todo::

    Link to explanations on the different systems we support and a discussion
    on which situations they are useful for.

Currently :code:`topos` comes with the following VertexArray implementations

- :code:`Cartesian`: For vertices using the :term:`cartesian coordinate`
  system
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

.. hlist::
    :columns: 3

    - :ref:`use_ref_vertx_cartesian`
    - :ref:`use_ref_vertx_data`
    - :ref:`use_ref_vertx_x`
    - :ref:`use_ref_vertx_y`
    - :ref:`use_ref_vertx_z`
    - :ref:`use_ref_vertx_r`
    - :ref:`use_ref_vertx_t`
    - :ref:`use_ref_vertx_length`
    - :ref:`use_ref_vertx_system`

.. _use_ref_vertx_cartesian:

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

.. _use_ref_vertx_data:

Data - Read Only
^^^^^^^^^^^^^^^^

Return the raw data contained in the array

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.data
    array([[1., 2., 3.],
           [4., 5., 6.]])

.. _use_ref_vertx_x:

X
^^

Return an array of just x coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.x
    array([1., 4.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

You can also use this property to set each x coordinate in the array to a new
value. For example

.. doctest:: ref-vertx-array-props

    >>> verts.x = np.array([0., 0.])
    >>> verts.data
    array([[0., 2., 3.],
           [0., 5., 6.]])

Instead of an array you can also set new values using a function. It's
arguments *must* be one or more of the coordinate variables that vertex arrays
support. The function will be called on each vertex in turn and passed that
vertex's values for each coordinate variable asked for.

For example if we wanted to set the :code:`x` coordinate of each vertex to be
the sum of the :code:`y` and :code:`z` coordinates we could do it as follows

.. doctest:: ref-vertx-array-props

    >>> verts.x = lambda y, z: y + z
    >>> verts.data
    array([[ 5.,  2.,  3.],
           [11.,  5.,  6.]])


.. note::

    This "does the right thing" for all vertex arrays, even if they are not
    using cartesian coordinates. The conversion is automatically performed for
    you behind the scenes.


.. todo::

    Link to examples demonstrating this feature in a "real world" application

.. _use_ref_vertx_y:

Y
^^

Return an array of just y coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.y
    array([2., 5.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

You can use this property to set each :code:`y` coordinate in the array to a
new value.  For example

.. doctest:: ref-vertx-array-props

    >>> verts.y = np.array([0., 0.])
    >>> verts.data
    array([[1., 0., 3.],
           [4., 0., 6.]])

Instead of an array you can also set new values using a function. It's
arguments *must* be one or more of the coordinate variables that
are supported by :code:`VertexArray`. The function will then be called on each
vertex in turn and passed that vertex's values for each coordinate variable
asked for.

For example if we wanted to set the :code:`y` coordinate to be 4 times the
:code:`x` coordinate we could do it as follows

.. doctest:: ref-vertx-array-props

    >>> verts.y = lambda x: 4*x
    >>> verts.data
    array([[ 1.,  4.,  3.],
           [ 4., 16.,  6.]])

.. note::

    This "does the right thing" for all vertex arrays, even if they are not
    natively using cartesian coordinates. The conversion will be automatically
    performed for you behind the scenes.

.. todo::

    Link to examples demonstrating this feature in a "real world" application.

.. _use_ref_vertx_z:

Z
^^

Return an array of just z coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.z
    array([3., 6.])

Like the :code:`cartesian` property this will automatically convert vertex
arrays that are not using Cartesian coordinates

You can use this property to set each :code:`z` coordinate in the array to a
new value. For example

.. doctest:: ref-vertx-array-props

    >>> verts.z = np.array([0., 0.])
    >>> verts.data
    array([[1., 2., 0.],
           [4., 5., 0.]])

Instead of an array you can also set new values using a function. It's
arguments *must* be one or more of the coordinate variables that are
supported by :code:`VertexArray`. The function will be called on each vertex in
turn and passed that vertex's value for each coordinate variable asked for.

For example if we wanted to set the :code:`z` coordinate to be the :code:`x`
coordinate less the the :code:`y` coordinate we could do it as follows

.. doctest:: ref-vertx-array-props

    >>> verts.z = lambda x, y: x - y
    >>> verts.data
    array([[ 1.,  2., -1.],
           [ 4.,  5., -1.]])

.. note::

    This "does the right thing" for all vertex arrays even if they are not
    natively using cartesian coordinates. The conversion will be performed for
    you automatically behind the scenes.

.. todo::

    Links to examples demonstrating this feature in a "real world" application

.. _use_ref_vertx_r:

R
^^

Return an array of just r coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[0, 4., 2.], [0., 2., 1.]])
    >>> verts = Cylindrical(vs)
    >>> verts.r
    array([2., 1.])

Like the :code:`cylindrical` property this will automatically convert vertex
arrays that are not using Cylindrical coordinates

You can use this property to set each :code:`r` coordinate array to a new
value. For example

.. doctest:: ref-vertx-array-props

    >>> verts.r = np.array([0., 0.])
    >>> verts.data
    array([[0., 4., 0.],
           [0., 2., 0.]])

Instead of an array you can also set new values using a function. It's
arguments *must* be one or more of the coordinate variables that are supported
for each :code:`VertexArray`. The function will then be called on each vertex
in turn and passed that vertex's values for each coordinate variable asked for.

For example if we wanted to set the :code:`r` coordinate to :math:`z^2 - z` we
could do it as follows

.. doctest:: ref-vertx-array-props

    >>> verts.r = lambda z: z*z - z
    >>> verts.data
    array([[ 0.,  4., 12.],
           [ 0.,  2.,  2.]])

.. note::

    This "does the right thing" for all vertex arrays even if they are not
    natively using cylindrical coordinates. The conversion will be
    automatically performed for you behind the scenes.


.. todo::

    Link to examples demonstrating this feature in a "real world" applicaton.

.. _use_ref_vertx_t:

T
^^

Return an array of just t coordinates

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[0, 4., 2.], [0., 2., 1.]])
    >>> verts = Cylindrical(vs)
    >>> verts.t
    array([0., 0.])

Like the :code:`cylindrical` property this will automatically convert vertex
arrays that are not using Cylindrical coordinates

You can use this property to set each :code:`t` coordinate in the array to a
new value. For example

.. doctest:: ref-vertx-array-props

    >>> verts.t = np.array([1., 1.])
    >>> verts.data
    array([[1., 4., 2.],
           [1., 2., 1.]])

Instead of an array you can also set new values using a function. It's
arguments *must* be one or more of the coordinate variables that are supported
by :code:`VertexArray`. The function will then be called on each vertex in turn
and passed that vertex's values for each coordinate variable asked for.

For example if we wanted to set the :code:`t` coordinate to be itself plus the
value of the radius then we could do it as follows

.. doctest:: ref-vertx-array-props

    >>> verts.t = lambda t, r: t + r
    >>> verts.data
    array([[3., 4., 2.],
           [2., 2., 1.]])

.. note::

    This "does the right thing" for all vertex arrays, even if they are not
    natively using cartesian coordinates. The conversion will be automatically
    performed for you behind the scenes.

.. todo::

    Link to examples demonstrating this feature in a "real world" application.

.. _use_ref_vertx_length:

Length - Read Only
^^^^^^^^^^^^^^^^^^

Return the number of vertices in an array

.. doctest:: ref-vertx-array-props

    >>> vs = np.array([[1., 2., .3], [4., 5., 6.]])
    >>> verts = Cartesian(vs)
    >>> verts.length
    2

.. _use_ref_vertx_system:

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

.. _use_ref_vertx_addition:

Addition
^^^^^^^^

.. testsetup:: ref-vertx-array-addition

    import numpy as np
    from topos.vertices import Cartesian, Cylindrical

:code:`VertexArrays` support addition with a number of different objects, each
with their own behavior:

- :ref:`use_ref_vertx_addition_arr`
- :ref:`use_ref_vertx_addition_np`

.. _use_ref_vertx_addition_arr:

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

.. _use_ref_vertx_addition_np:

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

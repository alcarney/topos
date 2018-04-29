Troubleshooting
===============


ToposError
----------

The base error type for all errors thrown by topos.

FaceDataError
-------------

A face array data error.

CylindricalVerticesError
------------------------

a cylindrical vertices error.

GeometryNameError
-----------------

A geometry name error.

MeshDataError
-------------

A mesh data error.

VertexAdditionError
-------------------

These errors are all related to the addition of 2 vertex arrays.

.. testsetup:: va-addition-errors

    import numpy as np
    from topos.core.vertices import Cartesian

.. error::

    Incompatible shape (??), array must have shape (3,)

Vertex arrays support addition with numpy arrays, which can be used to shift
a whole collection for vertices by a constant amount e.g. when moving an entire
object up by a certain amount. Since coordinates are represented by 3 numbers
the numpy array you use must only consist of these three numbers.

For example:

.. doctest:: va-addition-errors

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> vert_array = Cartesian(vs)
    >>> vert_array += np.array([1., 4., -2.])
    >>> vert_array.cartesian
    array([[2., 6., 1.],
           [5., 9., 4.]])

.. error::

    Addition is not supported with type (??)

While addition with a :code:`VertexArray` is supported with a few kinds
of object it doesn't make sense with everything. Please see the
documentation for `Addition`_ for more details

.. _Addition: http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#use-ref-vertx-addition

VertexCoordinateError
---------------------

These errors are related to extracting specific coordinate values
from a vertex array.

.. testsetup:: va-coordinate-error

    import numpy as np
    from topos.core.vertices import Cartesian

.. error::

    Coordinates must be specified using an iterable.

You can use Python's list indexing syntax (:code:`my_list[0]`) to access
a particular collection of coordinate variables from a vertex array.
However instead of using numbers a vertex array take what's called an
iterable. An iterable is any python object that can be used in a for loop
such as :code:`list`, :code:`str`, :code:`tuple` and :code`set`.

The iterable should then contain the name of any coordinate variable you
want returned. For example to get the :code:`x` and :code:`z` coordinate
of every vertex in the array both of the following are valid examples.

.. doctest:: va-coordinate-error

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> cs = Cartesian(vs)

    >>> cs['xz']
    array([[1., 3.],
           [4., 6.]])

    >>> cs['x', 'z']
    array([[1., 3.],
           [4., 6.]])

.. error::

    Unknown coordinate variable (??)

When asking for a particular collection of coordinate variables you can only
ask for the variables that are currently supported. These are:

- :code:`x`: The cartesian :math:`x`-coordinate
- :code:`y`: The cartesian :math:`y`-coordinate
- :code:`z`: The cartesian :math:`z`-coordinate
- :code:`r`: The polar :math:`r`-coordinate
- :code:`t`: The polar :math:`\theta`-coordinate


.. error::

    Coordinate values must be specified using a numpy array

    Coordinate array must have shape (??)

Using the :code:`vertex_array.x = values` syntax to assign each :code:`x`-value
in the array to a new value the array :code:`values` must be a numpy array.
Furthermore this array must have the same length as the vertex array you are
using it with for example.

.. doctest:: va-coordinate-error

    >>> vs = np.array([[0., 2., 3.], [0., 5., 6.]])
    >>> cs = Cartesian(vs)
    >>> cs.length
    2

    >>> cs.x
    array([0., 0.])

    >>> cs.x = np.array([1., 4.])
    >>> cs.data
    array([[1., 2., 3.],
           [4., 5., 6.]])

VertexDataError
---------------

These errors are all related to the creation of a vertex array.

.. error::

    Vertex array must be represented by a numpy array.

.. testsetup:: va-data-errors

    import numpy as np
    from topos.core.vertices import Cartesian, Cylindrical

You would see this message if you pass something other than a numpy
array to the constructor of a VertexArray.

Passing in your vertices as a `numpy array`_ will fix the issue

.. doctest:: va-data-errors

    >>> vs = np.array([[1., 2., 3.]])
    >>> Cartesian(vs)
    Cartesian Array: 1 vertex

.. error::

    Vertex array must have shape (n, 3)

Numpy arrays are extremely flexible and can be used to represent lots
of types of data, everything from a single point, to large matrices and
even `images`_. To be able to support this wide range of applications
every numpy array has a shape represented by a tuple of one or more numbers
that describes... well the shape of the data. Perhaps I should give a few
examples.

- A simple array of three numbers :code:`np.array([1, 2, 3])` has the shape
  :code:`(3,)`
- A :code:`3x3` matrix :code:`np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])`
  would have the shape :code:`(3, 3)`
- A :code:`512x512` pixel RGB Image would have the shape :code:`(512, 512, 3)`

You can check the shape of a numpy array by accessing the :code:`shape`
attribute

.. doctest:: va-data-errors

    >>> vs = np.array([[1, 2, 3], [4, 5, 6]])
    >>> vs.shape
    (2, 3)

Back to our situation, vertex arrays are essentially a list of points in 3D
space which means they should have a shape :code:`(n, 3)`. Where :code:`n`
refers to the number of points in the array and the :code:`3` refers to the
3 numbers required to represent a point in 3D space. This means that if you
want to create an array containing a single vertex you have to ensure that the
list of numbers is itself wrapped in a list.

.. doctest:: va-data-errors

    >>> v = np.array([ [1, 2, 3] ])
    >>> Cartesian(v)
    Cartesian Array: 1 vertex

.. _images: https://matplotlib.org/users/image_tutorial.html
.. _numpy array: https://docs.scipy.org/doc/numpy/user/basics.creation.html

WorldViewDataError
------------------

A world view data error.

WorldViewPosistionError
-----------------------

A world view position error.

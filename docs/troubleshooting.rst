Troubleshooting
===============

Here you will (hopefully) find a description of every error from within topos
and what you can do to fix it!

- :ref:`trbl_mesh_errors`: Errors relating to to :code:`Mesh` objects
- :ref:`trbl_vertx_errors`: Errors relating to Vertex Array objects
  such as :code:`Cartesian` and :code:`Cylindrical`

.. note::

    :code:`(??)` In error messages below indicates where situation specific
    information will be reported

.. _trbl_mesh_errors:

Mesh Errors (ME)
----------------

.. _trbl_me01:

ME01
^^^^

.. _trbl_vertx_errors:

Vertex Array Errors (VA)
------------------------

.. testsetup:: va-errors

    import numpy as np
    from topos.vertices import Cartesian, Cylindrical

These errors are related to any of the Vertex Array objects such as
:code:`Cartesian` and :code:`Cylindrical`

- :ref:`trbl_va01`: Initialisation errors
- :ref:`trbl_va02`: Array addition errors
- :ref:`trbl_va03`: Get item errors (:code:`array['x']`)
- :ref:`trbl_va04`: Coordinate property errors (:code:`array.z`)

.. _trbl_va01:

VA01
^^^^

This class of errors are all related to the creation of new vertex arrays

.. error::

    VA01.1: Vertex array must be represented by a numpy array

You would see this message if you pass something other than a `numpy array`_ to
the constructor of a Vertex Array.

.. doctest:: va-errors

    >>> Cartesian([1., 2., 3.])
    Traceback (most recent call last):
    ...
    TypeError: VA01.1: Vertex array must be represented by a numpy array
    More info: https://topos.readthedocs.io/en/latest/troubleshooting.html#va01

Passing in your vertices in a numpy array will fix this issue

.. doctest:: va-errors

    >>> vs = np.array([[1. , 2. , 3.]])
    >>> Cartesian(vs)
    Cartesian Array: 1 vertex

.. error::

    VA01.2: Vertex array must have shape (n, 3)

Numpy arrays are extremely flexible and can be used to represent lots of types
of data, everything from a single point, to large matrices and even `images`_.
To be able to support this wide range of applications every numpy array has a
shape which is a tuple of one or more numbers outlining... well the shape of
the data. Perhaps I should give you a couple of examples

- A simple array of three numbers :code:`np.array([1, 2, 3])` would have a
  the shape :code:`(3,)`
- A :code:`3x3` matrix :code:`np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])`
  would have a shape :code:`(3, 3)`
- A :code:`512x512` pixel RGB Image would have a shape of :code:`(512, 512, 3)`

You can check the shape of a numpy array by accessing the :code:`shape`
attribute

.. doctest:: va-errors

    >>> vs = np.array([[1, 2, 3], [4, 5, 6]])
    >>> vs.shape
    (2, 3)

In our case vertex arrays are essentially a list of points and so they have a
shape given by :code:`(n, 3)`. Where the :code:`3` refers to the three
coordinates required to specify a point in space and the :code:`n` refers to
the number of vertices in the array. So even if you want to create a vertex
array with a single vertex you have to wrap it in an extra list like so

.. doctest:: va-errors

    >>> v = np.array([ [1., 2., 3.] ])
    >>> Cartesian(v)
    Cartesian Array: 1 vertex

.. _trbl_va02:

VA02
^^^^

.. error::

    :code:`VA02.1: Incompatible shape (??), array must have shape (3,)`

Vertex arrays support addition with a few different types of object. One of
these is a numpy array which you can use to move a whole collection of vertices
by a constant amount. In order for this to work the array that you use must
have a compatible shape which is :code:`(3,)` - one value for each coordinate.

For example:

.. doctest:: va-errors
    :options: +NORMALIZE_WHITESPACE

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> vert_array = Cartesian(vs)
    >>> vert_array += np.array([1., 4., -2.])
    >>> vert_array.cartesian
    array([[2., 6., 1.],
           [5., 9., 4.]])

.. error::

    :code:`VA02.2: Addition is not supported with type (??)`

While addition on a :code:`VertexArray` is supported with a few different kinds
of object it doesn't make sense with everything. Please see the section on
:ref:`use_ref_vertx_addition` for details on which types of objects are supported.

.. _trbl_va03:

VA03
^^^^

.. error::

    :code:`VA03.1: Coordinates must be specified using an iterable`

You can use Python's list indexing syntax (:code:`my_list[0]`) to access a
particular collection of coordinate variables from the vertex array. However
instead of a number vertex arrays take what's called an iterable, an iterable
is any python object that you can use in a for loop. Examples of iterables
include :code:`list`, :code:`str`, :code:`tuple` and :code:`set`.

Inside this iterable you would then put the name of any coordinate variable you
want to have returned. For example to get the :code:`x` and :code:`z`
coordinate of every vertex in an array both of the following are valid.

.. doctest:: va-errors

    >>> vs = np.array([[1., 2., 3.], [4., 5., 6.]])
    >>> cs = Cartesian(vs)

    >>> cs['xz']
    array([[1., 3.],
           [4., 6.]])

    >>> cs[('x', 'z')]
    array([[1., 3.],
           [4., 6.]])


.. error::

    :code:`VA03.2: Unknown coordinate variable (??)`

When asking for a particular collection of coordinate variables, you can only
ask for the coordinate variables we currently support which are:

- :code:`x`: The cartesian :math:`x`-coordinate
- :code:`y`: The cartesian :math:`y`-coordinate
- :code:`z`: The cartesian :math:`z`-coordinate
- :code:`r`: The polar :math:`r`-coordinate
- :code:`t`: The polar :math:`\theta`-coordinate


.. _trbl_va04:

VA04
^^^^

.. error::

    :code:`VA04.1: Coordinate values must be specified using a numpy array`

    :code:`VA04.2: Coordinate array must have shape (??)`

When changing setting new coordinate values for each vertex in the array using
the :code:`array.x = new_values` syntax :code:`new_values` must be a numpy
array. Furthermore since you are assigning it to a single coordinate variable
this array can only have one dimension and can only be the same length as the
vertex array. For example

.. doctest:: va-errors

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

.. _images: https://matplotlib.org/users/image_tutorial.html
.. _numpy array: https://docs.scipy.org/doc/numpy/user/basics.creation.html

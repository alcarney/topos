Troubleshooting
===============

Here you will (hopefully) find a description of every error from within topos
and what you can do to fix it!

- :ref:`Mesh Errors (ME)`: Errors relating to to :code:`Mesh` objects
- :ref:`Vertex Array Errors (VA)`: Errors relating to Vertex Array objects
  such as :code:`Cartesian` and :code:`Cylindrical`

Mesh Errors (ME)
----------------

ME01
^^^^

Vertex Array Errors (VA)
------------------------

.. testsetup:: va-errors

    import numpy as np
    from topos.vertices import Cartesian, Cylindrical

These errors are related to any of the Vertex Array objects such as
:code:`Cartesian` and :code:`Cylindrical`

- :ref:`VA01`: Initialisation errors
- :ref:`VA02`: Array addition errors


VA01
^^^^

This class of errors are all related to the creation of new vertex arrays

.. warning::

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

.. warning::

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

VA02
^^^^

.. warning::

    VA02.1: Incompatible shape (??), array must have shape (3,)

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

.. _images: https://matplotlib.org/users/image_tutorial.html
.. _numpy array: https://docs.scipy.org/doc/numpy/user/basics.creation.html

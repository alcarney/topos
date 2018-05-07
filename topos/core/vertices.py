from abc import ABC, abstractmethod
import numpy as np
from magus.inspect import get_parameters


from .errors import ToposError


class VertexDataError(ToposError):
    """These errors are all related to the creation of a vertex array.

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
    """


class VertexAdditionError(ToposError):
    """These errors are all related to the addition of 2 vertex arrays.

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
    """


class VertexCoordinateError(ToposError):
    """These errors are related to extracting specific coordinate values
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
    - :code:`t`: The polar :math:`\\theta`-coordinate


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
    """


class VertexArray(ABC):

    _coords = 'xyzrt'

    def __init__(self, data):

        with VertexDataError():
            if not isinstance(data, (np.ndarray,)):
                message = "Vertex array must be represented by a numpy array"
                raise TypeError(message)

            shape = data.shape

            if len(shape) != 2 or shape[1] != 3:
                raise TypeError("Vertex array must have shape (n, 3)")

            self._data = data

    def __len__(self):
        return self.length

    def __repr__(self):
        s = self.system + " Array: "

        if self.length == 1:
            s += '{} vertex'.format(self.length)
        else:
            s += '{} vertices'.format(self.length)

        return s

    def __add__(self, other):

        system = self.system.lower()

        with VertexAdditionError():

            if isinstance(other, (VertexArray,)):

                us = self.__getattribute__(system)
                vs = other.__getattribute__(system)
                verts = np.concatenate((vs, us))

                return self.fromarray(verts)

            if isinstance(other, (np.ndarray,)):

                shape = other.shape

                if shape != (3,):
                    message = "Incompatible shape {}, array must have shape (3,)"
                    raise TypeError(message.format(shape))

                vs = self.__getattribute__(system)
                return self.fromarray(vs + other)

            message = "Addition is not supported with type {}"
            raise TypeError(message.format(type(other)))

    @classmethod
    def fromarray(cls, array):
        """Given a numpy array, construct a :py:class:`VertexArray` from it."""
        return cls(array)

    def copy(self):
        """Return a copy of the array under the same coordinate system."""
        vs = np.array(self.data)
        return self.fromarray(vs)

    @property
    def system(self):
        """Return a string representing the coorindate system the array uses."""
        return type(self).__name__

    @property
    def data(self):
        """Return the underlying numpy array representing the vertex array."""
        return self._data

    @property
    def length(self):
        """Return the length of the vertex array."""
        return self._data.shape[0]

    @property
    @abstractmethod
    def cartesian(self):
        """Return a numpy representing the vertex array
        w.r.t :term:`cartesian coordinate` s."""
        pass

    @property
    @abstractmethod
    def cylindrical(self):
        """Return a numpy array representing the vertex array
        w.r.t :term:`cylindrical coordinate` s."""
        pass

    @property
    def x(self):
        """Return a numpy array containing the :math:`x` coordinate of each vertex.
        Can also be used to modify each coordinate, see the
        `documentation <http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#x>`__
        for more details."""
        return self.cartesian[:, 0]

    @property
    def y(self):
        """Return a numpy array containing the :math:`y` coordinate of each vertex.
        Can also be used to modify each coordinate, see the
        `documentation <http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#y>`__
        for more details."""
        return self.cartesian[:, 1]

    @property
    def z(self):
        """Return a numpy array containing the :math:`z` coordinate of each vertex.
        Can also be used to modify each coordinate, see the
        `documentation <http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#z>`__
        for more details."""
        return self.cartesian[:, 2]

    @property
    def r(self):
        """Return a numpy array containing the :math:`r` coordinate of each vertex.
        Can also be used to modify each coordinate, see the
        `documentation <http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#r>`__
        for more details."""
        return self.cylindrical[:, 2]

    @property
    def t(self):
        """Return a numpy array containing the :math:`t` coordinate of each vertex.
        Can also be used to modify each coordinate, see the
        `documentation <http://topos.readthedocs.io/en/latest/use/reference/vertexarray.html#t>`__
        for more details."""
        return self.cylindrical[:, 0]

    def __getitem__(self, key):

        coords = []

        with VertexCoordinateError():

            try:
                for c in key:

                    if c not in self._coords:
                        message = "Unknown coordinate variable {}"
                        raise ValueError(message.format(c))

                    coords.append(self.__getattribute__(c))

            except TypeError:
                raise TypeError("Coordinates must be specified using an iterable.")

        return np.dstack(coords)[0]

    def _coord_set_array(self, arr, var):

        with VertexCoordinateError():
            if not isinstance(arr, (np.ndarray,)):
                raise TypeError("Coordinate values must be specified with a numpy array.")

            if arr.shape != (self.length,):
                message = "Coordinate array must have shape ({},)"
                raise TypeError(message.format(self.length))

            self.__getattribute__("set_" + var)(arr)

    def _coord_set_fn(self, fn, var):

        coords = get_parameters(fn)
        args = self[coords]

        if len(coords) == 1:
            args.shape = (self.length,)
            vfn = np.vectorize(fn)
            cs = vfn(args)
            self._coord_set_array(cs, var)
        else:
            vfn = np.vectorize(fn)
            args = args.transpose()
            cs = vfn(*args)
            self._coord_set_array(cs, var)


    def _set_coord(self, arg, var):

        if isinstance(arg, (np.ndarray,)):
            self._coord_set_array(arg, var)
            return

        if callable(arg):
            self._coord_set_fn(arg, var)
            return

        raise TypeError

    def fmt(self, fmtstr, prefix="", suffix="", sep="\n"):
        """Return a string representation of the array according to a given
        format string compatible with Python's :py:meth:`python:str.format` syntax.

        :param fmtstr: The format string to apply to each vertex
        :param prefix: A string to include before the vertex data
        :param suffix: A string to include after the vertex data
        :param sep: A string to include between each vertex.

        :type fmtstr: str
        :type prefix: str
        :type suffix: str
        :type sep: str

        :raises KeyError: The format string cannot contain any named
                          substitutions e.g. :code:`{x}`
        :return: :code:`prefix + foreach vertex <fmtstr + sep> + suffix`
        :rtype: str
        """

        string = prefix
        string += sep.join(fmtstr.format(*v) for v in self.cartesian)
        string += suffix

        return string

    @x.setter
    def x(self, value):
        self._set_coord(value, 'x')

    @y.setter
    def y(self, value):
        self._set_coord(value, 'y')

    @z.setter
    def z(self, value):
        self._set_coord(value, 'z')

    @r.setter
    def r(self, value):
        self._set_coord(value, 'r')

    @t.setter
    def t(self, value):
        self._set_coord(value, 't')

    @abstractmethod
    def set_x(self, arr):
        pass

    @abstractmethod
    def set_y(self, arr):
        pass

    @abstractmethod
    def set_z(self, arr):
        pass

    @abstractmethod
    def set_r(self, arr):
        pass

    @abstractmethod
    def set_t(self, arr):
        pass


class Cartesian(VertexArray):
    """An implementation of a :py:class:`VertexArray` representing vertices
    in Cartesian coordinates.
    """

    def set_x(self, xs):
        self._data[:, 0] = xs

    def set_y(self, ys):
        self._data[:, 1] = ys

    def set_z(self, zs):
        self._data[:, 2] = zs

    def set_r(self, rs):
        ts = self.cylindrical[:, 0]
        xs = rs * np.cos(ts)
        ys = rs * np.sin(ts)

        self._data[:, 0] = xs
        self._data[:, 1] = ys

    def set_t(self, ts):
        rs = self.cylindrical[:, 2]
        xs = rs * np.cos(ts)
        ys = rs * np.sin(ts)

        self._data[:, 0] = xs
        self._data[:, 1] = ys

    @property
    def cartesian(self):
        return self._data

    @property
    def cylindrical(self):
        XS = self._data[:, 0]
        YS = self._data[:, 1]
        ZS = self._data[:, 2]

        RS = np.sqrt(XS*XS + YS*YS)
        TS = np.arctan2(YS, XS)

        return np.dstack([TS, ZS, RS])[0]


class Cylindrical(VertexArray):
    """An implementation of a :py:class:`VertexArray` representing vertices
    in Cylindrical coordinates.
    """

    def set_x(self, xs):
        ys = self.cartesian[:, 1]

        ts = np.arctan2(ys, xs)
        rs = xs / np.cos(ts)  # This might cause problems!

        self._data[:, 0] = ts
        self._data[:, 2] = rs

    def set_y(self, ys):
        xs = self.cartesian[:, 0]

        ts = np.arctan2(ys, xs)
        rs = ys / np.sin(ts)

        self._data[:, 2] = rs
        self._data[:, 0] = ts

    def set_z(self, zs):
        self._data[:, 1] = zs

    def set_r(self, rs):
        self._data[:, 2] = rs

    def set_t(self, ts):
        self._data[:, 0] = ts

    @property
    def cylindrical(self):
        return self._data

    @property
    def cartesian(self):
        TS = self._data[:, 0]
        ZS = self._data[:, 1]
        RS = self._data[:, 2]

        # Do the conversion
        XS = RS * np.cos(TS)
        YS = RS * np.sin(TS)

        return np.dstack([XS, YS, ZS])[0]

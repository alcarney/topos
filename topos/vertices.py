from abc import ABC, abstractmethod
import numpy as np
from magus.inspect import get_parameters


from .codefu import prepare_vertex_array_function
from .errors import raiseError


class VertexArray(ABC):
    """An abstract class that defines what it means to be a Vertex Array.

    As this is an abstract class you cannot create an instance of this directly.
    Instead you have to use one of the built in subclasses such as
    :py:class:`Cartesian` or create your own and inherit from this one.

    Any class inheriting from this one *must* implement the following properties
    and methods:

    - :py:attr:`system` Returns a string representing the coordinate system
      the array uses
    - :py:meth:`native` Method that converts other vertex arrays to the
      format used internally
    - :py:attr:`cartesian` Returns vertices :term:`w.r.t` Cartesian coordinates
    - :py:attr:`cylindrical` Returns vertices :term:`w.r.t` Cylindrical coordinates
    """

    _coord_vars = 'xyzrt'

    def __init__(self, data):
        """
        :param data: Array with shape :code:`(n, 3)` representing the vertices
        :type data: :py:class:`numpy:numpy.ndarray`
        :raises TypeError: If :code:`data` is not a numpy array :ref:`VA01`
        :raises TypeError: If :code:`data` has the wrong shape :ref:`VA01`

        """

        if not isinstance(data, (np.ndarray,)):
            raiseError('VA01.1')

        else:
            shape = data.shape

            if len(shape) != 2 or shape[1] != 3:
                raiseError('VA01.2')

            self._data = data

    def __repr__(self):
        s = self.system + ' '

        if self.length == 1:
            s += 'Array: {} vertex'.format(self.length)
            return s

        s += 'Array: {} vertices'.format(self.length)
        return s

    def __getitem__(self, key):

        if not isinstance(key, (tuple, str, list, set)):
            raiseError('VA03.1')

        coords = []

        for c in key:

            if c not in self._coord_vars:
                raiseError('VA03.2', var=c)

            coords.append(self.__getattribute__(c))

        return np.dstack(coords)[0]

    def __setitem__(self, coords, fn):

        args = self[get_parameters(fn)]

        vfn = np.vectorize(fn)

        new_values = vfn(args)

        idx = 0
        for c in coords:

            self.__setattr__(c, new_values[:, idx])
            idx += 1

    def __add__(self, other):

        if isinstance(other, (VertexArray,)):

            us = self.native()
            vs = self.native(other)
            verts = np.concatenate((vs, us))

            return self.fromarray(verts)

        if isinstance(other, (np.ndarray,)):

            shape = other.shape

            if shape != (3,):
                raiseError('VA02.1', shape=shape)

            vs = self.native()
            return self.fromarray(vs + other)

        raiseError('VA02.3', type=type(other))

    def fmt(self, fmtstr, prefix="", suffix="", sep="\n"):
        """Return a string representation of the array according to a given
        format string compatible with Python's :py:meth:`python:str.format` syntax.


        :param fmtstr: The format string to apply to each vertex
        :type fmtstr: str
        :param prefix: A string to include before the vertex data
        :type prefix: str
        :param suffix: A string to include after the vertex data
        :type suffix: str
        :param sep: A string to include between each vertex.
        :type sep: str

        :raises KeyError: The format string cannot contain any named
                          substitutions e.g. :code:`{x}`

        :return: :code:`prefix + foreach vertex <fmtstr + sep> + suffix`
        :rtype: str
        """

        string = prefix
        string += sep.join(fmtstr.format(*v) for v in self._data)
        string += suffix

        return string

    @property
    def data(self):
        """Return the underlying array as-is."""
        return self._data

    @property
    def length(self):
        """Length of the array, same as the number of vertices."""
        return self._data.shape[0]

    @classmethod
    def fromarray(cls, array):
        """Given a numpy array, construct a :py:class:`VertexArray` from it."""
        return cls(array)

    @abstractmethod
    def native(self, other=None):
        """Returns a vertex array with respect to its "native" coordinate system.

        If called with no arguments then this method returns the internal vertex array.
        If given another vertex array, this calls the relevant property method to get
        that array's vertices with respect to this array's coordinate system. This is
        used internally quite a bit to implement the arithmetic operators generally
        for all VertexArrays.

        It's not the best solution however and we will look to remove this in a future
        release.

        :param other: The vertex array to convert to this array's native coordinate system
        :type other: VertexArray
        """
        pass

    def _coord_setter(self, value, coord):
        """This handles the boilerplate required to set a particular coordinate
        in the array. Checking the type and shape etc.
        """

        if isinstance(value, (np.ndarray,)):

            shape = value.shape

            if len(shape) != 1 or shape[0] != self.length:
                raiseError("VA04.1", length=self.length)

            # Set the coordinate
            self.__getattribute__('set_' + coord)(value)
        else:
            raiseError("VA04.1")


    @property
    @abstractmethod
    def system(self):
        """String representing the natvie coordinate system for the array."""
        pass

    @property
    @abstractmethod
    def cartesian(self):
        """Return the vertices with respect to the cartesian coordinate system."""
        pass

    @property
    @abstractmethod
    def cylindrical(self):
        """Return the vertices with respect to the cylindrical coordinate system."""
        pass

    @property
    def x(self):
        """Return an array of just the x coordinates."""
        return self.cartesian[:, 0]

    @x.setter
    def x(self, value):
        """Set just the x coordinate of each vertex to a new value."""
        self._coord_setter(value, 'x')

    @abstractmethod
    def set_x(self, value):
        pass

    @property
    def y(self):
        """Return an array of just the y coordinates."""
        return self.cartesian[:, 1]

    @y.setter
    def y(self, value):
        """Set just the y coordinate of each vertex to a new value"""
        self._coord_setter(value, 'y')

    @abstractmethod
    def set_y(self, value):
        pass

    @property
    def z(self):
        """Return an array of just the z coordinates."""
        return self.cartesian[:, 2]

    @z.setter
    def z(self, value):
        """Set just the z coordinate of each vertex to a new value"""
        self._coord_setter(value, 'z')

    @abstractmethod
    def set_z(self, value):
        pass

    @property
    def r(self):
        """Return an array of just the r coordinates."""
        return self.cylindrical[:, 2]

    @r.setter
    def r(self, value):
        """Set just the r coordinate of each vertex to a new value."""
        self._coord_setter(value, 'r')

    @abstractmethod
    def set_r(self, value):
        pass

    @property
    def t(self):
        """Return an array of just the t coordinates."""
        return self.cylindrical[:, 0]

    @t.setter
    def t(self, value):
        self._coord_setter(value, 't')

    @abstractmethod
    def set_t(self, value):
        pass


class Cartesian(VertexArray):
    """An implementation of a :py:class:`VertexArray` representing vertices
    in Cartesian coordinates.
    """

    def native(self, other=None):

        if other is not None:
            return other.cartesian

        return self.cartesian

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
    def system(self):
        return 'Cartesian'

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

    def native(self, other=None):

        if other is not None:
            return other.cylindrical

        return self.cylindrical

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
    def system(self):
        return "Cylindrical"

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

from abc import ABC, abstractmethod
import numpy as np


from .errors import raiseError


class VertexArray(ABC):

    def __init__(self, data):

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

    def fmt(self, fmtstr):
        """
        Given a standard python format string, create the
        corresponding string representation
        """

        string = ""

        for vert in self._data:
            string += fmtstr.format(*vert) + '\n'

        return string

    @property
    def data(self):
        return self._data

    @property
    def length(self):
        return self._data.shape[0]

    @classmethod
    def fromarray(cls, array):
        return cls(array)

    @abstractmethod
    def native(self, other=None):
        pass

    @property
    @abstractmethod
    def system(self):
        pass

    @property
    @abstractmethod
    def cartesian(self):
        pass

    @property
    @abstractmethod
    def cylindrical(self):
        pass



class Cartesian(VertexArray):
    """
    Class representing vertices in Cartesian coordinates, implements all
    the conversions to other schemes
    """

    def native(self, other=None):

        if other is not None:
            return other.cartesian

        return self.cartesian

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

    def native(self, other=None):

        if other is not None:
            return other.cylindrical

        return self.cylindrical

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


CoordinateSystems = {
    'CARTESIAN': Cartesian,
    'CYLINDRICAL': Cylindrical
}

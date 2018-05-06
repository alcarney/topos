import numpy as np
from abc import ABC, abstractmethod


from .errors import ToposError


class FaceDataError(ToposError):
    """A face array data error."""


class FaceArray(ABC):

    def __init__(self, data):

        with FaceDataError():

            if not isinstance(data, (np.ndarray)):
                raise TypeError("Faces must be represented with a numpy array")
            shape = data.shape

            # With shape (n, sides)
            if len(shape) != 2 or shape[1] != self.num_sides:
                message = "Face array must have shape (n, {})"
                raise TypeError(message.format(self.num_sides))

            # It must have an integer type
            if not issubclass(data.dtype.type, np.integer):
                raise TypeError("Faces can only be defined using integers.")

        self._data = data

    def __len__(self):
        return self.length

    def __repr__(self):
        s = self.name + " Array: "

        if self.length == 1:
            s += "{} face".format(self.length)

        else:
            s += "{} faces".format(self.length)

        return s

    def fmt(self, fmtstr, prefix="", suffix="", sep="\n"):
        """Return a string representation of the array according to a given
        format string compatible with Python's :py:meth:`python:str.format` syntax.

        :param fmtstr: The format string to apply to each face
        :param prefix: A string to include before the face data
        :param suffix: A string to include after the face data
        :param sep: A string to include between each face.

        :type prefix: str
        :type fmtstr: str
        :type suffix: str
        :type sep: str

        :raises KeyError: The format string cannot contain any named
                          substitutions e.g. :code:`{x}`

        :return: :code:`prefix + foreach face <fmtstr + sep> + suffix`
        :rtype: str
        """

        string = prefix
        string += sep.join(fmtstr.format(*f) for f in self._data)
        string += suffix

        return string


    @property
    def length(self):
        return self._data.shape[0]

    @property
    def data(self):
        return self._data

    @property
    @abstractmethod
    def num_sides(self):
        """The number of sides in each face."""
        pass

    @property
    @abstractmethod
    def name(self):
        """The name of the type of faces this array contains."""
        pass


class Quads(FaceArray):

    @property
    def num_sides(self):
        return 4

    @property
    def name(self):
        return "Quad"


class Tris(FaceArray):

    @property
    def num_sides(self):
        return 3

    @property
    def name(self):
        return "Tri"

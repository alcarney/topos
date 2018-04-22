"""Views allow you to look at a model from different perspectives without
affecting the underlying geometry.

The most common view is perhaps the world view which allows you to position
an object in space without touching the geometry itself.
"""
import numpy as np

from .geometry import Geometry
from .vertices import Cartesian
from .errors import ToposError


class WorldViewDataError(ToposError):
    """A world view data error."""


class WorldViewPosistionError(ToposError):
    """A world view position error."""


class WorldView(Geometry):
    """A world view allows you to place an object within the world wthout
    changing the underlying geometry.
    """

    def __init__(self, geometry=None, position=None, name=None):
        self.geometry = geometry
        self.position = np.array([0., 0., 0.]) if position is None else position
        self.name = "WorldView:" if name is None else name

    def _repr_hook(self):

        string = "Geometry: {}\n".format(self.geometry.name)
        string += "Position: {}\n".format(self.position)
        return string

    @property
    def vertices(self):

        verts = self.geometry.vertices.cartesian
        world_verts = verts + self.position
        return Cartesian(world_verts)

    @property
    def faces(self):
        return self.geometry.faces

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):

        if not isinstance(value, (np.ndarray,)):
            raise TypeError("Position must be represented by a numpy array.")
        shape = value.shape

        if len(shape) != 1 and shape[0] != 3:
            raise TypeError('Position array must have shape (3,)')

        self._position = value

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):

        if value is not None and not isinstance(value, (Geometry,)):
            raise TypeError("Geometry must be represented by an instance of Geometry.")

        self._geometry = value


class EdgeView():
    pass

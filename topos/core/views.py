"""Views allow you to look at a model from different perspectives without
affecting the underlying geometry.

The most common view is perhaps the world view which allows you to position
an object in space without touching the geometry itself.
"""
import numpy as np
from .geometry import Geometry
from .vertices import Cartesian
from .errors import raiseError


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

        if isinstance(value, (np.ndarray,)):
            shape = value.shape

            if len(shape) != 1 and shape[0] != 3:
                raiseError('WV02.2')

            self._position = value
            return

        raiseError('WV02.1')

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):

        if value is not None and not isinstance(value, (Geometry,)):
            raiseError("WV01.1")

        self._geometry = value


class EdgeView():
    pass

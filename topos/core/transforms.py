from abc import ABC, abstractmethod
import numpy as np
from .geometry import Geometry, Mesh


class VertexTransform(ABC):
    """A vertex transform is a transform that only acts on the vertices
    of a geometry."""

    @abstractmethod
    def transform(self, verts):
        pass

    def __rrshift__(self, other):

        if not isinstance(other, Geometry):
            raise TypeError('Transforms can only be applied to Geometry objects')

        new_verts = self.transform(other.vertices.copy())

        return Mesh(verts=new_verts, faces=other.faces, name=other.name)


class Displace(VertexTransform):
    """Displace the vertices in a geometry by a given amount."""

    def __init__(self, x=None, y=None, z=None, r=None, t=None):

        self._displacements = {
            'x': x,
            'y': y,
            'z': z,
            'r': r,
            't': t
        }

    def transform():
        pass


class Scale(VertexTransform):
    """Scale a geometry by a given amount."""

    def __init__(self, dx=None, dy=None, dz=None, dr=None, dt=None):

        self._factors = {
            'x': dx,
            'y': dy,
            'z': dz,
            'r': dr,
            't': dt
        }

    def transform(self, verts):

        for coord, factor in self._factors.items():

            if factor is not None:

                values = verts.__getattribute__(coord)
                verts.__setattr__(coord, values * factor)

        return verts


def scale(dx=None, dy=None, dz=None, dr=None, dt=None):
    return Scale(dx, dy, dz, dr, dt)

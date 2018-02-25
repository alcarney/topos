from enum import Enum
import numpy as np


from .errors import raiseError
from .vertices import VertexArray


class Mesh(object):

    def __init__(self, verts=None, faces=None, name=None):

        if verts is not None and not isinstance(verts, (VertexArray,)):
            raiseError('ME01.1')


        self._verts = verts
        self._faces = faces
        self._name = name


    @property
    def vertices(self):
        return self._verts


    def save(self, filename):

        with open(filename, 'w') as f:

            f.write(self.vertices.fmt("v {} {} {}"))

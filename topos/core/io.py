"""Here we defines readers and loaders etc so that we are able
to interact with the outside world.
"""
import json
import numpy as np

from abc import ABC, abstractmethod
from string import Template

from .geometry import Geometry, Mesh
from .faces import Quads
from .vertices import Cartesian


class DataFormat(ABC):
    """An abstract class, outlining what an object needs to support
    in order to read and write some kind of data."""

    # Implementors must define this to indicate what they save/load
    __type__ = None

    def load(self, filepath):
        """Given some filepath, load the data that is defined there."""

        with open(filepath) as f:
            return self._load(f.read())

    def loads(self, string):
        """Given some string, load the data it defines."""
        return self._load(string)

    def dump(self, filepath, obj):
        """Given a filepath and a object convert the object
        to some format and save it to the given file."""

        with open(filepath, 'w') as f:
            f.write(self.dumps(obj))

    def dumps(self, obj):
        """Given an object convert the object
        to some format and return the string."""

        if not isinstance(obj, (self.__type__,)):
            name = self.__type__.__name__
            message = "Expected a {} object.".format(name)
            raise TypeError(message)

        return self._dump(obj)

    @abstractmethod
    def _load(self, data):
        """Given some string, load the data defined there."""
        pass

    @abstractmethod
    def _dump(self, geometry):
        """Given some object, convert it into some string
        representation that can be written to file."""
        pass


class ObjFormat(DataFormat):
    """An .obj implementation of the DataFormat interface for geometries."""

    __type__ = Geometry

    def _dump_name(self, geometry):
        return "o {}\n".format(geometry.name)

    def _dump_vertices(self, geometry):
        return geometry.vertices.fmt("v {} {} {}", suffix="\n")

    def _dump_faces(self, geometry):
        face_fmt = " ".join("{}" for _ in range(geometry.faces.num_sides))
        return geometry.faces.fmt("f " + face_fmt, suffix="\n")

    def _dump(self, geometry):
        """Save a geometry object in .obj format"""

        name = self._dump_name(geometry)
        vertices = self._dump_vertices(geometry)
        faces = self._dump_faces(geometry)

        return name + vertices + faces

    def _load(self, data):
        raise NotImplementedError("Loading is not yet supported.")


class JsonFormat(DataFormat):
    """A .json implementation of the data format interface for geometries."""

    __type__ = Geometry

    def _dump_vertices(self, geometry):
        params = {}
        params['prefix'] = "["
        params['suffix'] = "]"
        params['sep'] = ", "
        params['fmtstr'] = "[{}, {}, {}]"

        return geometry.vertices.fmt(**params)

    def _dump_faces(self, geometry):
        params = {}
        params['prefix'] = "["
        params['suffix'] = "]"
        params['sep'] = ", "

        fmtstr = ", ".join("{}" for _ in range(geometry.faces.num_sides))

        params['fmtstr'] = "[" + fmtstr + "]"

        return geometry.faces.fmt(**params)


    def _dump(self, geometry):
        json_string = '{"name": $name, "vertices": $vertices, "faces": $faces}'
        json_template = Template(json_string)

        parts = {}
        parts['name'] = '"{}"'.format(geometry.name)
        parts['vertices'] = self._dump_vertices(geometry)
        parts['faces'] = self._dump_faces(geometry)

        return json_template.substitute(**parts)

    def _load(self, data):
        json_data = json.loads(data)

        if 'vertices' not in json_data:
            raise TypeError("Missing expected field: vertices")

        if 'faces' not in json_data:
            raise TypeError("Missig expected field: faces")

        name = "<json_mesh>" if 'name' not in json_data else json_data['name']
        verts = Cartesian(np.array(json_data['vertices']))
        faces = Quads(np.array(json_data['faces']))

        return Mesh(verts=verts, faces=faces, name=name)

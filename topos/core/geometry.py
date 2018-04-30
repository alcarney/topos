from abc import ABC, abstractmethod

from .errors import ToposError
from .faces import FaceArray
from .vertices import VertexArray
from .generators import cylindrical_faces


class GeometryNameError(ToposError):
    """Errors related to the naming of a geometry object.

    .. error::

       Name must be represented by a string.

    In order to work as expected with the rest of the system, a name
    must be given by a string.
    """


class Geometry(ABC):
    """An abstract class which models the notion of "geometry".

    By pulling out what makes "geometry" into its own abstract
    class anything that manipulates geometry can operate on
    a clearly defined interface regardless of what that object
    actually is.

    For example, the file format writers can define their methods
    once and work for any object whether it be a mesh, a world view
    etc.

    Currently there are only two properties that need to be overriden
    in order to define a new geometry representing format:

    - :code:`vertices`: This should return a :code:`VertexArray`
                        representing the object's vertices
    - :code:`faces`: This should return a :code:`FaceArray` representing
                     the object's faces.
    """

    @property
    def name(self):
        """The name of the geometry object."""

        if self._name is None:
            return "Geometry"

        return self._name

    @name.setter
    def name(self, value):

        with GeometryNameError():
            if isinstance(value, (str,)):
                self._name = value
                return

            raise TypeError('Name must be represented by a string.')

    def _repr_hook(self):
        """This method will be called whenever the object's __repr__ string
        is asked for.

        Implementing classes should override this method to add any extra
        information to their instances' __repr__ strings."""
        return ""

    def __repr__(self):
        string = "{}\n".format(self.name)

        string += self._repr_hook()

        if self.vertices is not None:
            string += "Vertices: {}\n".format(self.vertices.length)

        if self.faces is not None:
            string += "Faces: {}\n".format(self.faces.length)

        return string

    @property
    @abstractmethod
    def vertices(self):
        """Return the VertexArray which defines the vertices in the object."""
        pass

    @property
    @abstractmethod
    def faces(self):
        """Return the FaceArray which defines the faces in the object."""
        pass

    def save(self, filename, fmt):
        """Save the geometry to file in according to the format specified
        by the fmt object.

        :param filename: The path to the file to write the data to
        :param fmt: The object to use to save the data

        :type filename: str
        :type fmt: topos.core.io.DataFormat
        """
        writer = fmt()
        writer.dump(filename, self)


class MeshDataError(ToposError):
    """These errors are related to the data you use with a mesh object.

    .. error::

        Vertices must be represented by a VertexArray

    A number of the tools that work with a :code:`Mesh` and other
    :code:`Geometry` objects expect to work with a :code:`VertexArray`
    object. This means the only way to create a Mesh is to use one of
    these arrays.

    .. error::

        Faces must be represented by a FaceArray

    As with the error outlined above, many of the tools expect to work
    with :code:`FaceArray` objects so faces in a mesh must be represented
    in this manner.
    """


class Mesh(Geometry):
    """A simple container for geometry data.

    This is the simplest implementation of the :code:`Geometry` interface
    it is purely a dumb container for geometry data.
    """

    def __init__(self, verts=None, faces=None, name=None):

        with MeshDataError():

            if verts is not None and not isinstance(verts, (VertexArray,)):
                raise TypeError('Vertices must be represented by a VertexArray')

            if faces is not None and not isinstance(faces, (FaceArray,)):
                raise TypeError('Faces must be represented by a FaceArray')


        self._verts = verts
        self._faces = faces
        self._name = name

    @property
    def vertices(self):
        return self._verts

    @property
    def faces(self):
        return self._faces

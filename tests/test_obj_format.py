import pytest
from hypothesis import given
from hypothesis.strategies import text
from unittest import TestCase
from unittest.mock import Mock, PropertyMock

from .strategies import cartesian, quads, tris

import numpy as np
from topos.core.io import ObjFormat
from topos.core.faces import Quads, Tris
from topos.core.vertices import Cartesian


@pytest.mark.io
@pytest.mark.obj
class TestObjFormat(TestCase):
    """Tests relating to the ObjFormat writer."""

    def setUp(self):
        self.obj = ObjFormat()

    @given(name=text())
    def test_dump_name(self, name):
        """Test that the name of a geometry is formatted correctly."""

        geometry = Mock()
        type(geometry).name = PropertyMock(return_value=name)

        o_name = self.obj._dump_name(geometry)
        assert o_name == "o {}\n".format(name)

    @given(vs=cartesian)
    def test_dump_vertices(self, vs):
        """Test that the vertices of a geometry are formatted correctly."""

        geometry = Mock()
        vs = Cartesian(np.array(vs))
        type(geometry).vertices = PropertyMock(return_value=vs)

        v_verts = self.obj._dump_vertices(geometry)
        verts = v_verts.split("\n")[:-1]

        assert len(verts) == vs.length
        assert all(v[0:2] == 'v ' for v in verts)
        assert all(len(v.split(' ')) == 4 for v in verts)

    @given(fs=quads())
    def test_dump_quads(self, fs):
        """Test that faces are formatted correctly for quads."""

        geometry = Mock()
        fs = Quads(fs)
        type(geometry).faces = PropertyMock(return_value=fs)

        f_faces = self.obj._dump_faces(geometry)
        faces = f_faces.split("\n")[:-1]

        assert len(faces) == fs.length
        assert all(f[0:2] == 'f ' for f in faces)
        assert all(len(f.split(' ')) == 5 for f in faces)

    @given(fs=tris())
    def test_dump_tris(self, fs):
        """Test that faces are formatted correctly for tris."""

        geometry = Mock()
        fs = Tris(fs)
        type(geometry).faces = PropertyMock(return_value=fs)

        f_faces = self.obj._dump_faces(geometry)
        faces = f_faces.split("\n")[:-1]

        assert len(faces) == fs.length
        assert all(f[0:2] == 'f ' for f in faces)
        assert all(len(f.split(' ')) == 4 for f in faces)

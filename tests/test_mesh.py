from pytest import raises
from hypothesis import given
from hypothesis.strategies import text
from .strategies import cartesian, quads

import numpy as np
from topos.core.geometry import Mesh
from topos.core.vertices import Cartesian


class TestInit(object):

    def test_no_args(self):

        m = Mesh()

        assert m._verts is None
        assert m._faces is None
        assert m._name is None

    def test_bad_verts(self):

        with raises(TypeError):
            Mesh(verts=2)

    def test_bad_faces(self):

        with raises(TypeError):
            Mesh(faces=2)


class TestProperties(object):

    @given(vs=cartesian)
    def test_vertices(self, vs):

        cs = Cartesian(np.array(vs))
        m = Mesh(verts=cs)

        assert m.vertices == cs

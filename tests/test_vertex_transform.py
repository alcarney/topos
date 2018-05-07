import pytest
from pytest import raises
from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import integers

import numpy as np
from topos.core.transforms import VertexTransform
from topos.core.geometry import Mesh
from topos.core.primitives import Plane
from topos.core.vertices import Cartesian


class DummyTransform(VertexTransform):
    """A dummy transform that we can use for testing purposes."""

    def transform(self, verts):

        zeros = np.zeros((verts.length,))
        verts.x = zeros

        return verts


@pytest.mark.transforms
@pytest.mark.vertices
class TestVertexTransform(TestCase):
    """Tests relating to the base vertex transform class."""

    @given(size=integers(min_value=4, max_value=128))
    def test_copy_data(self, size):
        """A transform should leave the previous object unchanged."""

        p = Plane(size)

        before = p.vertices.data

        q = p >> DummyTransform()

        assert (q.vertices.x == 0.0).all()
        assert isinstance(q, (Mesh,))
        assert (before == p.vertices.data).all()


    def test_enforce_geometry(self):
        """Transforms should only apply to geometry objects."""

        with raises(TypeError) as err:

            Cartesian(np.zeros((3, 3))) >> DummyTransform()

        assert 'Geometry objects' in str(err.value)

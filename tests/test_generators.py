import pytest
from hypothesis import given, assume, settings
from unittest import TestCase

import numpy as np
from topos.core.generators import (planar_vertices, planar_faces,
                                   cylindrical_vertices, cylindrical_faces)

from .strategies import size, real, pve_real


@pytest.mark.generators
class TestPlanarVertices(TestCase):
    """Tests for the :code:`planar_vertices` generator."""

    @given(N=size)
    def test_grid_size(self, N):
        """A grid of size :math:`N` should contiain :math:`N^2` vertices."""

        verts = planar_vertices(N)
        M, dim = verts.shape

        assert dim == 3
        assert M == N * N

    @given(N=size, x=real, dx=pve_real)
    def test_x_min_max(self, N, x, dx):
        """Check that the function respects the :code:`xmin`,
        :code:`xmax` arguments."""

        assume(N > 1)
        verts = planar_vertices(N, xmin=x, xmax=(x + dx))
        xs = verts[:, 0]

        assert xs.min() == x
        assert xs.max() == x + dx

    @given(N=size, y=real, dy=pve_real)
    def test_y_min_max(self, N, y, dy):
        """Check that the function respects the :code:`ymin`,
        :code:`ymax` arguments."""

        assume(N > 1)
        verts = planar_vertices(N, ymin=y, ymax=(y + dy))
        ys = verts[:, 1]

        assert ys.min() == y
        assert ys.max() == y + dy

    @given(N=size)
    def test_z_value(self, N):
        """The :math:`z` value of every vertex should be zero."""

        verts = planar_vertices(N)
        zs = verts[:, 2]

        assert (zs == 0.0).all()


def old_planar_faces(N):
    """This is the older, slower implementation of planar_faces
    we keep it around to ensure correctness."""
    # TODO: Is there a more "numpy" way to do this?
    faces = []
    for j in range(0, N - 1):
        for i in range(1, N):

            lower_left = i + (j * N)
            lower_right = (i + 1) + (j * N)
            upper_right = (i + 1) + ((j + 1) * N)
            upper_left = i + ((j + 1) * N)

            faces.append([lower_left, lower_right, upper_right, upper_left])

    return np.array(faces)


@pytest.mark.generators
class TestPlanarFaces(TestCase):
    """Tests for the :code:`planar_faces` generator."""

    @given(N=size)
    def test_grid_size(self, N):
        """A grid of size :math:`N` should contain :math:`(N-1)^2` faces."""
        assume(N > 1)

        faces = planar_faces(N)
        M, dim = faces.shape

        assert dim == 4
        assert M == (N - 1)**2

    @given(N=size)
    @settings(max_examples=10)
    def test_consistency(self, N):
        """The current implementation should match the reference
        implementation."""
        assume(N > 1)

        old = old_planar_faces(N)
        new = planar_faces(N)

        assert (old == new).all()

    @given(N=size)
    def test_face_definitions(self, N):
        """The faces definitions should be correct.
        This means the following must be true for each face::

            ul -------- ur
            |           |     ul = upper left
            |           |     ur = upper right
            |           |     ll = lower left
            |           |     lr = lower right
            ll -------- lr

        - :math:`lr - ll = 1`
        - :math:`ur - ul = 1`
        - :math:`ul - ll = N`
        - :math:`ur - lr = N`
        """
        assume(N > 1)

        faces = planar_faces(N)

        ll = faces[:, 0]
        lr = faces[:, 1]
        ur = faces[:, 2]
        ul = faces[:, 3]

        assert ((lr - ll) == 1).all()
        assert ((ur - ul) == 1).all()
        assert ((ur - lr) == N).all()
        assert ((ul - ll) == N).all()

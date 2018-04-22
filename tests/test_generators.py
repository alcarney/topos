from math import pi

import pytest
from hypothesis import given, assume, settings
from unittest import TestCase

import numpy as np
from topos.core.generators import (planar_vertices, planar_faces,
                                   cylindrical_vertices, cylindrical_faces)

from .strategies import size, real, pve_real, theta


@pytest.mark.planar_geometry
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


@pytest.mark.planar_geometry
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


@pytest.mark.generators
@pytest.mark.cylindrical_geometry
class TestCylindricalVertices(TestCase):
    """Tests for the :code:`cylindrical_vertices` generator."""

    @given(N_t=size, N_z=size)
    def test_grid_size(self, N_t, N_z):
        """A grid should contains :math:`N_t \\times N_z` vertices."""

        verts = cylindrical_vertices(N_t, N_z)
        M, dim = verts.shape

        assert dim == 3
        assert M == N_t * N_z

    @given(N_t=size, N_z=size)
    def test_theta_min_max_defaults(self, N_t, N_z):
        """Check that :math:`\\theta \\in [0, 2\\pi)` with default ranges"""

        assume(N_t > 1)

        verts = cylindrical_vertices(N_t, N_z)
        ts = verts[:, 0]

        # There should be N_t distinct values of theta
        uniques = np.unique(ts)
        assert uniques.shape == (N_t,)

        assert uniques.min() == 0.0
        assert uniques.max() < 2*pi

    @given(N_t=size, N_z=size, tmin=theta, tmax=theta)
    def test_theta_min_max_args(self, N_t, N_z, tmin, tmax):
        """Check that :math:`\\theta \\in [\\theta_{min}, \\theta_{max}]` when
        specified."""

        assume(N_t > 1)
        assume(tmax - tmin > 0)

        verts = cylindrical_vertices(N_t, N_z, theta_min=tmin, theta_max=tmax)
        ts = verts[:, 0]

        uniques = np.unique(ts)
        assert uniques.shape == (N_t,)

        assert uniques.min() == tmin
        assert uniques.max() == tmax

    @given(N_t=size, N_z=size)
    def test_z_min_max_defaults(self, N_t, N_z):
        """Check that :math:`z \\in [0, 1]` by default"""

        assume(N_z > 1)

        verts = cylindrical_vertices(N_t, N_z)
        zs = verts[:, 1]

        uniques = np.unique(zs)
        assert uniques.shape == (N_z,)

        assert uniques.min() == 0.0
        assert uniques.max() == 1.0

    @given(N_t=size, N_z=size, zmin=real, zmax=real)
    def test_z_min_max_args(self, N_t, N_z, zmin, zmax):
        """Check that :math:`z \\in [zmin, zmax]` when specified."""

        assume(N_z > 1)
        assume(zmax - zmin > 0)

        verts = cylindrical_vertices(N_t, N_z, zmin=zmin, zmax=zmax)
        zs = verts[:, 1]

        uniques = np.unique(zs)
        assert uniques.shape == (N_z,)

        assert uniques.min() == zmin
        assert uniques.max() == zmax

    @given(N_t=size, N_z=size, r=pve_real)
    def test_r_args(self, N_t, N_z, r):
        """Check that r takes the value given."""

        assume(N_t * N_z > 1)

        verts = cylindrical_vertices(N_t, N_z, r=r)
        rs = verts[:, 2]

        assert rs.shape == (N_t * N_z,)
        assert (rs == r).all()

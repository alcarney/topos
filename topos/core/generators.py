"""Generators for known geometries.

This module provides a number of functions which can easily create
geometry in "known" configurations they are typically used internally
to create the geometry for the standard primitives.

Typically they come in :code:`<name>_vertices` and :code:`<name>_faces`
pairs, that is where one generates the vertices representing the spatial
configuration and the other generates the faces that those vertices define
and represents the topology of the mesh.

These generators are pretty simple and not very versatile,
hopefully at some point they may be expanded upon.

Currently the following geometries are supported:

    - Planar: The :math:`xy`-plane in cartesian coordinates
    - Cylindrical: A hollow tube in cylindrical coordinates
"""

from math import pi
import numpy as np

from .errors import ToposError


def planar_vertices(N, xmin=0., xmax=1., ymin=0., ymax=1.):
    """Generate a grid of vertices in the :math:`xy`-plane.

    The resulting grid will have :math:`N \\times N` vertices
    and will cover the domain :math:`[xmin, xmax] \\times [ymin, ymax]`.

    :param N: The number of vertices to generate on each side of the grid
    :param xmin: The minimum :math:`x` value. Default :code:`0.0`
    :param xmax: The maximum :math:`x` value. Default :code:`1.0`
    :param ymin: The minimum :math:`y` value. Default :code:`0.0`
    :param ymax: The maximum :math:`y` value. Default :code:`1.0`

    :type N: int
    :type xmin: float
    :type xmax: float
    :type ymin: float
    :type ymax: float

    :rtype: numpy.ndarray
    :returns: The vertices in :math:`(x, y, z)` coordinates representing
              the grid. An array with shape :math:`(N^2, 3)`
    """
    # Generate a grid of x-y values at the desired resolution
    xs = np.linspace(xmin, xmax, N)
    ys = np.linspace(ymin, ymax, N)
    XS, YS = np.meshgrid(xs, ys)

    # Reshape the grids to be one long array
    XS.shape = (N*N,)
    YS.shape = (N*N,)
    zeros = np.zeros(XS.shape)

    # Return the vertices all at z=0
    return np.dstack([XS, YS, zeros])[0]


class CylindricalVerticesError(ToposError):
    """a cylindrical vertices error."""


@CylindricalVerticesError.annotate()
def cylindrical_vertices(N_theta, N_z, r=1., zmin=0., zmax=1., theta_min=0.,
                         theta_max=2*pi):
    """Generate a hollow tube of vertices using cylindrical coordinates.

    So that we can reuse the face numbering method used in the planar geometry
    we alter the representation of cylindrical coordinates from the standard
    :math:`(r, \\theta, z)` order to the order :math:`(\\theta, z, r)`.

    This means topologically the plane and cylinder's surface look the same
    (Assuming that we stop before connecting the first and last vertices
    generated). Indeed if we were to "plot" the resulting vertices in cartesian
    space they would look like a plane occupying the domain :math:`[0, 2\\pi]
    \\times [0, 1]` with the :math:`z` coordinate equal to the given radius.

    .. versionchanged:: 0.0.7

        You can alter the tube that this function generates. The :math:`z`
        dimensions can be changed wih the :code:`zmin, zmax` parameters.
        The :math:`\\theta` dimensions can be changed with the
        :code:`theta_min, theta_max` parameters.

    :param r: The radius of the tube. Default :code:`1.0`
    :param zmin: The minimum :math:`z`-value. Default :code:`0.0`
    :param zmax: The maximum :math:`z`-value. Default :code:`1.0`
    :param theta_min: The minimum :math:`\\theta`-value. Default :code:`0.0`
    :param theta_max: The maximum :math:`\\theta`-value. Default :code:`2*pi`
    :param N_z: The number of vertices to use in the :math:`z` direction
    :param N_theta: The number of vertices to use in the :math:`\\theta`
                    direction.

    :type r: float
    :type N_z: int
    :type zmin: float
    :type zmax: float
    :type N_theta: int
    :type theta_min: float
    :type theta_max: float

    :rtype: numpy.ndarray
    :returns: The vertices representing the hollow tube using our representation
              of cylindrical coordinates :math:`(\\theta, z, r)`. An array with
              shape :math:`(N_{\\theta}N_z, 3)`
    """

    if not isinstance(N_theta, (int,)):
        raise TypeError("Argument N_theta must be an integer")

    if N_theta < 1:
        raise ValueError("Argument N_theta must be positive")


    # Only include the endpoint if we aren't doing a full loop
    endpoint = theta_max < 2*pi
    ts = np.linspace(theta_min, theta_max, N_theta, endpoint=endpoint)
    zs = np.linspace(zmin, zmax, N_z)

    TS, ZS = np.meshgrid(ts, zs)
    TS.shape = (N_theta * N_z,)
    ZS.shape = (N_theta * N_z,)
    ones = np.full(ZS.shape, r)

    return np.dstack([TS, ZS, ones])[0]


def cylindrical_faces(N_theta, N_z, close_loop=True):
    """Generate the face definitions for an :math:`N_{\\theta} \\times N_z`
    hollow tube of vertices.

    This case is very similar to the planar case, thanks to our choice of
    the order of cylindrical coordinate variables :math:`(\\theta, z, r)`
    However this function also gives the choice of connecting the left
    and right "edges" of the tube so that we get a complete loop

    :param N_theta: The number of vertices in the :math:`\\theta`-direction
    :param N_z: The number of vertices in the :math:`z`-direction

    :type N_theta: int
    :type N_z: int

    :rtype: numpy.ndarray
    :returns: The face definitions corresponding to a
              :math:`N_{\\theta} \\times N_z`
              tube of vertices. An array with shape
              :math:`((N_{\\theta} - 1)(N_z - 1), 4)`
    """

    faces = []

    for j in range(0, N_z - 1):

        # Here I am using the fact that python promotes True/False to
        # 1/0 respectively when used in arithmetic to calculate the range
        for i in range(1, N_theta + (close_loop * 1)):

            # To get the normals pointing in the right direction we need
            # to define the corners in anti-clockwise order. So we will
            # # do it as follows:
            #      Lower left -> Lower right -> Upper right -> Upper left
            lower_left = j * N_theta + i
            lower_right = j*N_theta + i + 1
            upper_right = (j + 1) * N_theta + i + 1
            upper_left = (j + 1) * N_theta + i

            # Only the 'right hand' values could be problematic when closing
            # the loop
            if lower_right >= (j+1) * N_theta:
                lower_right -= N_theta - 1

            if upper_right >= (j+2) * N_theta:
                upper_right -= N_theta - 1

            # Add the face to the mesh
            faces.append((lower_left, lower_right, upper_right, upper_left))

    return np.array(faces)


def planar_faces(N):
    """Generate the face definitions for an :math:`N^2` grid of vertices.

    So that the normals face the correct direction the vertices have to
    be listed in an anti-clockwise direction a shown below::

                    ←
        4 --------- 3
        |           |
        |           |
        |           |
        |           |
        1 --------- 2 ↑
        →

    :param N: The number of vertices on each side of the grid.

    :type N: int
    :rtype: numpy.ndarray

    :returns: The face definitions that correspond to a :math:`N^2` grid
              of vertices. An array with shape :math:`((N-1)^2, 4)`
    """

    M = N - 1

    # Generate the main grid of numbers that will become the lower left
    # definitions and what we will shift around to form the other corners
    ns = np.array([i for i in range(1, N * M) if i % N != 0])

    lower_left = ns
    lower_right = ns + 1
    upper_left = ns + N
    upper_right = ns + (N + 1)

    return np.dstack([lower_left, lower_right, upper_right, upper_left])[0]

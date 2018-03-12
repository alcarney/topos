from pytest import raises
from hypothesis import given, assume
from unittest.mock import patch
import numpy as np
import numpy.random as npr
import numpy.testing as npt


from topos.vertices import VertexArray, Cartesian, Cylindrical


from .strategies import cartesian, cylindrical, size, cart


# Dummy vertex array to let us test the main base class
class DummyArray(VertexArray):

    def native(self, other=None):

        if other is not None:
            return other.data

        return self.data


    @property
    def system(self):
        return 'Dummy'

    @property
    def cartesian(self):
        return self._data

    @property
    def cylindrical(self):
        return self._data


class TestInit(object):

    @patch('topos.vertices.raiseError')
    def test_init_bad_type(self, Err):

        DummyArray("string")
        Err.assert_called_once_with("VA01.1")

    @patch('topos.vertices.raiseError')
    def test_init_bad_shape(self, Err):

        DummyArray(np.array([[[2, 3]]]))
        Err.assert_called_once_with("VA01.2")

    @given(vs=cartesian)
    def test_with_array(self, vs):

        verts = np.array(vs)
        vertices = DummyArray(verts)
        assert (vertices._data == verts).all()


class TestProperties(object):

    @given(length=size)
    def test_length(self, length):

        verts = npr.rand(length, 3)
        vertices = DummyArray(verts)

        assert vertices.length == length

    def test_set_length(self):

        vs = DummyArray(np.zeros((4, 3)))

        with raises(AttributeError) as err:
            vs.length = 4

        assert "can't set attribute" in str(err.value)

    @given(length=size)
    def test_repr(self, length):

        assume(length != 1)

        vs = DummyArray(np.zeros((length, 3)))
        s = 'Dummy Array: {} vertices'.format(length)

        assert s == str(vs)

    def test_repr_single(self):

        vs = DummyArray(np.zeros((1, 3)))
        s = 'Dummy Array: 1 vertex'

        assert s == str(vs)

    @given(v=cart)
    def test_fmt_single(self, v):

        arr = DummyArray(np.array([v]))
        s = arr.fmt('{} {} {}')

        assert s == '{} {} {}'.format(*v)

        s = arr.fmt('{1} {2} {0}')
        assert s == '{1} {2} {0}'.format(*v)

    @given(length=size)
    def test_fmt_many(self, length):

        arr = DummyArray(npr.rand(length, 3))
        s = arr.fmt('{} {} {}')

        segments = s.split('\n')
        assert len(segments) == length

    @given(length=size)
    def test_x(self, length):

        arr = npr.rand(length, 3)
        VS = DummyArray(arr)

        assert (VS.x == arr[:, 0]).all()

    @given(length=size)
    def test_y(self, length):

        arr = npr.rand(length, 3)
        VS = DummyArray(arr)

        assert (VS.y == arr[:, 1]).all()

    @given(length=size)
    def test_z(self, length):

        arr = npr.rand(length, 3)
        VS = DummyArray(arr)

        assert (VS.z == arr[:, 2]).all()

    @given(length=size)
    def test_r(self, length):

        arr = npr.rand(length, 3)
        VS = DummyArray(arr)

        assert (VS.r == arr[:, 2]).all()

    @given(length=size)
    def test_t(self, length):

        arr = npr.rand(length, 3)
        VS = DummyArray(arr)

        assert (VS.t == arr[:, 0]).all()


class TestGetItem(object):

    @given(length=size)
    def test_get_single(self, length):

        vs = npr.rand(length, 3)
        verts = DummyArray(vs)

        arr = verts['x']
        arr.shape = (length,)

        assert (arr == vs[:,0]).all()


    @given(length=size)
    def test_get_many(self, length):

        vs = npr.rand(length, 3)
        verts = DummyArray(vs)

        arr = verts['rzt']

        assert(arr[:,0] == vs[:,2]).all()
        assert(arr[:,1] == vs[:,2]).all()
        assert(arr[:,2] == vs[:,0]).all()


class TestOperations(object):

    @given(vs=cartesian, us=cartesian)
    def test_vertexarray_add(self, vs, us):

        VS = DummyArray(np.array(vs))
        US = DummyArray(np.array(us))

        TS = VS + US
        assert TS.length == (VS.length + US.length)

    @given(vs=cartesian, c=cart)
    def test_array_add(self, vs, c):

        VS = DummyArray(np.array(vs))
        C = np.array(c)
        TS = VS + C

        assert TS.length == VS.length

        QS = TS + (-C)
        assert QS.length == VS.length

        # Hypothesis and floating point numbers are evil
        diff = np.round((QS.data - VS.data), decimals=0)
        assert (diff == 0).all()




class TestCartesian(object):

    def test_system_set(self):

        c = Cartesian(np.zeros((1, 3)))
        assert c.system == 'Cartesian'

    @given(vs=cartesian)
    def test_cartesian(self, vs):

        verts = Cartesian(np.array(vs))
        assert (verts.cartesian == vs).all()


class TestCylindrical(object):

    def test_system_set(self):

        c = Cylindrical(np.zeros((1, 3)))
        assert c.system == 'Cylindrical'

    @given(vs=cylindrical)
    def test_cylindrical(self, vs):

        verts = Cylindrical(np.array(vs))
        assert (verts.cylindrical == vs).all()

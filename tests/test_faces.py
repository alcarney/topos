import numpy as np
from pytest import raises
from topos.core.faces import FaceArray


class DummyArray(FaceArray):
    """Dummy face array used for testing."""

    @property
    def num_sides(self):
        return 4

    @property
    def name(self):
        return "Dummy"


class TestInit(object):

    def test_with_bad_type(self):

        with raises(TypeError):
            DummyArray([1, 2, 3, 4])

    def test_with_bad_shape(self):

        with raises(TypeError):
            DummyArray(np.array([1, 2, 3, 4]))

    def test_with_bad_dtype(self):

        with raises(TypeError):
            DummyArray(np.array([[1, 2, 3., 4]]))

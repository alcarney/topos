import pytest
from unittest import TestCase
from hypothesis import given
from hypothesis.strategies import integers

from topos.core.primitives import Cylinder
from topos.core.io import JsonFormat


@pytest.mark.io
@pytest.mark.json
class TestJsonFormat(TestCase):
    """Tests relating to the json format object."""

    @given(N=integers(min_value=4, max_value=128))
    def test_json_dump_load(self, N):
        """We should be able to (de)serialise an object and not lose
        any information."""

        cylinder = Cylinder(N)
        json = JsonFormat()

        json_string = json.dumps(cylinder)
        mesh = json.loads(json_string)

        assert mesh.name == cylinder.name
        assert mesh.vertices.length == cylinder.vertices.length
        assert mesh.faces.length == cylinder.faces.length

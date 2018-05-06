.. _use_ref_face_array:

FaceArrays
==========

.. py:currentmodule:: topos.core.faces

The :py:class:`FaceArray` family of objects are responsible for managing and
manipulating collections of faces. Their use is identical with the only
difference being the number of sides on each face they support.

.. todo::

   Link to a discussion on the pros/cons for tris vs quads etc.

Currently :code:`topos` comes with the following FaceArray implementations

- :py:class:`Quads`: For faces with 4 sides
- :py:class:`Tris`: For faces with 3 sides

Initialisation
--------------

:py:class:`FaceArray` objects are wrappers over a :term:`numpy array` providing
additional features that are useful when treating these arrays as a list of
faces. To create a face array simply pass a numpy array with the right data to
one of these objects.

.. doctest:: ref-face-array-init

    >>> import numpy as np
    >>> from topos.core.faces import Quads

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> Quads(fs)
    Quad Array: 2 faces

Similarly for :py:class:`Tris`

.. doctest:: ref-face-array-init

    >>> from topos.core.faces import Tris

    >>> fs = np.array([[1, 2, 3], [4, 5, 6]])
    >>> Tris(fs)
    Tri Array: 2 faces

.. todo::

   Write a page outlining the way mesh data is represented and link to it here.

.. note::

   Due to the way geometry is represented the elements of a face array *must* be
   integers.

Properties
----------

:py:class:`FaceArray` objects have a number of properties which allow you to get
information about each array

.. hlist::
    :columns: 3

    - :ref:`use_ref_face_length`
    - :ref:`use_ref_face_num_sides`
    - :ref:`use_ref_face_data`
    - :ref:`use_ref_face_name`

.. _use_ref_face_length:

Length - Read Only
^^^^^^^^^^^^^^^^^^

.. testsetup:: ref-face-array-props

    import numpy as np
    from topos.core.faces import Quads, Tris

:py:attr:`FaceArray.length` allows you to get the number of faces in the
array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.length
    2

.. _use_ref_face_num_sides:

Num Sides - Read Only
^^^^^^^^^^^^^^^^^^^^^

:py:attr:`FaceArray.num_sides` returns the number of sides of each face in the
array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3], [4, 5, 6]])
    >>> faces = Tris(fs)
    >>> faces.num_sides
    3

.. _use_ref_face_data:

Data - Read Only
^^^^^^^^^^^^^^^^

:py:attr:`FaceArray.data` returns the underlying numpy array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.data
    array([[1, 2, 3, 4],
           [5, 6, 7, 8]])

.. _use_ref_face_name:

Name - Read Only
^^^^^^^^^^^^^^^^

:py:attr:`FaceArray.name` returns a name representing the type of faces in the array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.name
    'Quad'

Formatting
----------

.. testsetup:: ref-face-array-fmt

    import numpy as np
    from topos.core.faces import Quads

There will be times where you will want to show the data inside a face
array in a particular way, perhaps you are writing a new :code:`DataFormat`
implementation or just want to see just what is inside a particular array.
This is where the :py:meth:`FaceArray.fmt` method comes in.

The most straightforward use would be to pass it a valid `format string`_
which would be applied to each face in turn. For example to simply print out
the definition of each face one on each line we could do the following

.. doctest:: ref-face-array-fmt

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> print(faces.fmt("{} {} {} {}"))
    1 2 3 4
    5 6 7 8

The format string supports indices so we can if we wanted to change the order
in which the faces are shown

.. doctest:: ref-face-array-fmt

    >>> print(faces.fmt("{2} {1} {3} {0}"))
    3 2 4 1
    7 6 8 5

You can of course put any other symbols or strings you wanted to in this format
string

.. doctest:: ref-face-array-fmt

    >>> print(faces.fmt("{} -> {} -> {} -> {}"))
    1 -> 2 -> 3 -> 4
    5 -> 6 -> 7 -> 8

There are a few options that allow to alter how the final string is generated:

- :code:`prefix`: Use this option to start the formatted string with a given string.
  This is only used once *before* any of the faces have been processed.
- :code:`suffix`: Use the option to end the formatted string with a given string.
  This is only used once *after* all the faces have been processed.
- :code:`sep`: Use this to change the default separator between faces (:code:`"\n"`)
  to a string of your choosing.

As a final example here is how you can format the faces as a list of lists using this
function

.. doctest:: ref-face-array-fmt

    >>> print(faces.fmt("[{}, {}, {}, {}]", prefix="[", suffix="]", sep=", "))
    [[1, 2, 3, 4], [5, 6, 7, 8]]

.. _format string: https://docs.python.org/3/library/string.html#formatstrings

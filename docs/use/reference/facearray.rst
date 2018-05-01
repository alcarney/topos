.. _use_ref_face_array:

FaceArrays
==========

The :code:`FaceArray` family of objects are responsible for managing and
manipulating collections of faces. Their use is identical with the only
difference being the number of sides on each face they support.

.. todo::

   Link to a discussion on the pros/cons for tris vs quads etc.

Currently :code:`topos` comes with the following FaceArray implementations

- :code:`Quads`: For faces with 4 sides
- :code:`Tris`: For faces with 3 sides

Initialisation
--------------

:code:`FaceArray` objects are wrappers over a :term:`numpy array` providing
additional features that are useful when treating these arrays as a list of
faces. To create a face array simply pass a numpy array with the right data
to one of these objects.

.. doctest:: ref-face-array-init

    >>> import numpy as np
    >>> from topos.core.faces import Quads

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> Quads(fs)
    Quad Array: 2 faces

Similarly for :code:`Tris`

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

:code:`FaceArray` objects have a number of properties which allow you to get
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

This allows you to get the number of faces in the array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.length
    2

.. _use_ref_face_num_sides:

Num Sides - Read Only
^^^^^^^^^^^^^^^^^^^^^

Return the number of sides of each face in the array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3], [4, 5, 6]])
    >>> faces = Tris(fs)
    >>> faces.num_sides
    3

.. _use_ref_face_data:

Data - Read Only
^^^^^^^^^^^^^^^^

Returns the underlying numpy array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.data
    array([[1, 2, 3, 4],
           [5, 6, 7, 8]])

.. _use_ref_face_name:

Name - Read Only
^^^^^^^^^^^^^^^^

Returns a name representing the type of faces in the array

.. doctest:: ref-face-array-props

    >>> fs = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    >>> faces = Quads(fs)
    >>> faces.name
    'Quad'

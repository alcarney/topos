0.0.7 Unreleased
----------------

**Users**

- **NEW:CODE**: Geometries! There is now an abstract notion of geometry which
  should mean it will be easier to write things that "just work". With this
  release :code:`topos` comes with the following geometries:

  + :code:`Mesh`: Just like the previous mesh, the :code:`Mesh` object is now
    the simplest implementation of a :code:`Geometry` and is a simple container
    for vertices and faces.

- **NEW:CODE**: Views! Related to geometries, views allow you to have new
  perspectives on your models and most should work with anything that work with
  a geometry. With this release :code:`topos` comes with the following views:

  + :code:`WorldView`: This allows you to easily place an object in "WorldSpace"
    setting its location and rotation without changing the underlying geometry.

- **IMPROVE:CODE**: The implementation of :code:`planar_faces` has been improved
  making it much quicker than the old one for large values of :code:`N`

- **IMPROVE:DOCS**: The docs have had a major redesign hoping to be much more
  readable and easier to navigate.

**Contributors**

- **NEW:DOCS**: There is now a :code:`scripts/apidoc.py` script that will
  automatically generate the reference section - much like :code:`sphinx-apidoc`

- **CHANGED:DOCS**: The troubleshooting page is now automatically generated
  using the :code:`erratum` package. This means that all troubleshooting
  entries are defined in the codebase alongside the :code:`Error` classes which
  automatically provide a link to the troubleshooting documentation in the
  error message.

0.0.6 30/03/2018
----------------

- :code:`topos` is now a namespace package this means everything that was under
  the `topos.*` is now under `topos.core.*`

0.0.5 21/03/2018
----------------

**Users**

- **NEW:CODE** :code:`Cartesian` and :code:`Cylindrical` classes which handle
  vertex arrays in Cartesian and Cylindrical coordinates respectively.
- **NEW:DOCS** *Troubleshooting* page that attempts to detail all errors you might
  encounter using :code:`topos` and what you can do to fix them.


**Contributors**

- **NEW:DOCS** :code:`showmodel` directive that will take a name, obj file and
  mtl file (all optional) in insert a interactive 3D preview of the given mesh.

0.0.4 21/03/2018
----------------

Setting the release to only be on the test_travis task and python version 3.6

0.0.3 21/02/2018
----------------

Another "release" that will hopefully work this time

0.0.2 21/02/2018
----------------

This release is mainly to test the deploy: option on travis although there
have been some changes

**Added**

- Mesh class to manage and export object data
- Mesh data can be exported in .obj format
- Generators that can generate either a plane or a uncapped cylinder
- New Primitives:
  + Plane
  + Cylinder
- Started thinking about a transformation framework which makes use of the
  :code:`>>` operator to support 'pipeline' operations e.g. obj >> scale >>
  transform


0.0.1 17/02/2018
----------------

Initial release

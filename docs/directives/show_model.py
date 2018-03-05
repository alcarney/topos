from string import Template
from docutils import nodes
from docutils.parsers.rst import Directive, directives

# This creates a custom node - do we need this?
class showmodel_node(nodes.Inline, nodes.Element):
    pass


def write_html(options):
    """
    This function writes the HTML + JS needed to load and render
    an object in the webpage
    """

    # Unpack the options, choosing sensible defaults if not defined
    name = "model" if 'name' not in options.keys() else options['name']
    obj = "plane.obj" if 'obj' not in options.keys() else options['obj']
    mtl = "materials.mtl" if 'mtl' not in options.keys() else options['mtl']

    opts = {"name": name, "obj": obj, "mtl": mtl}

    # The code in the file we read from is based of the following article
    # https://manu.ninja/webgl-3d-model-viewer-using-three-js/
    with open('directives/model_code.html') as f:
        html_template = Template(f.read())

    return html_template.safe_substitute(opts)



class ShowModelDirective(Directive):
    """
    This class takes the directive in the source markup and does the
    necessary processing steps to convert it to the output HTML
    """

    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = True

    option_spec = {
        'name': directives.unchanged,
        'obj': directives.unchanged,
        'mtl': directives.unchanged,
    }

    has_content = True
    add_index = False

    def run(self):
        html = write_html(self.options)
        raw_node = nodes.raw('', html, format="html")
        return [ raw_node ]

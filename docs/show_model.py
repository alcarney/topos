from docutils import nodes
from docutils.parsers.rst import Directive

# This will become the name of the directive people use in markup
class showmodel(nodes.Structure, nodes.Element):
    pass


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
    }

    has_content = True
    add_index = False

    def run(self):
        pass

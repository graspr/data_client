from pyqtgraph.flowchart import Node

import pyqtgraph.flowchart.library as fclib
from graspr_client import get_buffer


class DataProcessingNode(Node):
    """SpecialFunction: short description

    This description will appear in the flowchart design window when the user
    selects a node of this type.
    """
    nodeName = 'DataProcessing' # Node type name that will appear to the user.

    def __init__(self, name):  # all Nodes are provided a unique name when they
                               # are created.
        Node.__init__(self, name, terminals={  # Initialize with a dict
                                               # describing the I/O terminals
                                               # on this Node.
            'inputTerminal': {'io': 'in'},
                'output1': {'io': 'out'},
                'output2': {'io': 'out'},
                'output3': {'io': 'out'},
                'output4': {'io': 'out'},
                'output5': {'io': 'out'},
                'output6': {'io': 'out'},
                'output7': {'io': 'out'},
                'output8': {'io': 'out'},
                'output9': {'io': 'out'},
                'output10': {'io': 'out'},
                'output11': {'io': 'out'},
                'output12': {'io': 'out'},
                'output13': {'io': 'out'},
                'output14': {'io': 'out'},
                'output15': {'io': 'out'},
                'output16': {'io': 'out'},
            })

    def process(self, inputTerminal,**kwds):
        # kwds will have one keyword argument per input terminal.
        ret = {
            'output1': get_buffer(0),
            'output2': get_buffer(1),
            'output3': get_buffer(2),
            'output4': get_buffer(3),
            'output5': get_buffer(4),
            'output6': get_buffer(5),
            'output7': get_buffer(6),
            'output8': get_buffer(7),
            'output9': get_buffer(8),
            'output10': get_buffer(9),
            'output11': get_buffer(10),
            'output12': get_buffer(11),
            'output13': get_buffer(12),
            'output14': get_buffer(13),
            'output15': get_buffer(14),
            'output16': get_buffer(15),
        }
        return ret

    # def ctrlWidget(self):  # this method is optional
    #     return someQWidget


fclib.registerNodeType(DataProcessingNode, [('Data',)])

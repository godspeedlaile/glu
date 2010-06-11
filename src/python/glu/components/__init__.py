"""
Exports the various components, which are available.

Also defines a base class for all components.

"""
# Import all the components
import glu_components_list

#
# Assemble list of the known components
#
_KNOWN_COMPONENTS = [ getattr(glu_components_list, name) for name in dir(glu_components_list) if not name.startswith("__") ]
_CODE_MAP = dict([ (component_class().getName(), component_class) for component_class in _KNOWN_COMPONENTS ])


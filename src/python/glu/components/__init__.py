"""
Exports the various components, which are available.

Also defines a base class for all components.

"""
#
# When adding a new component, all that is required is to
# add the import statement and add the component to the 'KNOWN_COMPONENTS' list.
# 

# Exporting these components
from glu.components.BaseComponent         import BaseComponent
from glu.components.TwitterComponent      import TwitterComponent
from glu.components.GsearchComponent      import GsearchComponent
from glu.components.CombinerComponent     import CombinerComponent
from glu.components.GpsWalkerComponent    import GpsWalkerComponent
from glu.components.StorageComponent      import StorageComponent

#from glu.components.salesforce_component   import SalesforceComponent
#from glu.components.marakana_component     import MarakanaComponent

from org.mulesource.glu.component import TestComponent
from org.mulesource.glu.component import JavaTwitterComponent

#
# The known components
#
_KNOWN_COMPONENTS = [ TwitterComponent, GsearchComponent, CombinerComponent, GpsWalkerComponent, StorageComponent,
                      TestComponent, JavaTwitterComponent ]
# SalesforceComponent, MarakanaComponent ]

# -------------------------------------------------------------------------------------
# Don't edit down here...
# -------------------------------------------------------------------------------------

_CODE_MAP = dict([ (component_class().getName(), component_class) for component_class in _KNOWN_COMPONENTS ])

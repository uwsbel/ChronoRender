'''loads C::R into maya scene'''

import cr_for_maya.cr_types as cr_types
from chronorender import ChronoRender
from chronorender.cr_object import Object
from chronorender.metadata import MetaData

def import_from_md(filename):
    '''create maya node tree from C::R data'''
    meta = MetaData(filename)
    facts = ChronoRender().getFactories()

    nodes = []
    for typename, elem in meta.getElementsDict().iteritems():
        for root in elem:
            nodes.append(_generate_node(root, typename, facts))

    return nodes

def _generate_node(root, typename, factories):
    if typename not in cr_types.type_dict: return None

    m_obj = cr_types.type_dict[typename](factories, **root)

    children = []
    for childtype, childelem, in root.iteritems():
        if isinstance(childelem, list):
            for node in childelem:
                children.append(_generate_node(node, childtype, factories))
        else:
            children.append(_generate_node(childelem, childtype, factories))

    children = [child for child in children if child != None]
    for child in children:
        m_obj.addChild(child)

    return m_obj

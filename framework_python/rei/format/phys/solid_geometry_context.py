from lxml import etree

from rei.format.semantics.CognitiveEntity import GeometryNode, CylinderGeometry, EllipsoidGeometry, VisualMaterial
from rei.hypergraph.base_elements import HypergraphEdge, HypergraphPort, HypergraphNode, HypergraphElement


def encode_typegeometry_element(e: GeometryNode) -> etree.Element:
    el_geom = None
    match e:
        case CylinderGeometry():
            el_geom = etree.Element("cylinder")
            el_radius = etree.Element("radius")
            el_radius.text = str(e["values"][0])
            el_length = etree.Element("length")
            el_length.text = str(e["values"][1])
            el_geom.append(el_radius)
            el_geom.append(el_length)
        case EllipsoidGeometry():
            if len(e["values"]) == 1:
                el_geom = etree.Element("sphere")
                el_radius = etree.Element("radius")
                el_radius.text = str(e["values"][0])
                el_geom.append(el_radius)
            else:
                el_geom = etree.Element("ellipsoid")
                el_radii = etree.Element("radii")
                el_radii.text = ' '.join([str(x) for x in  e["values"]])
                el_geom.append(el_radii)
    return el_geom


def extract_geometry_element(element):
    for e in element.get_subelements(lambda x: isinstance(x, GeometryNode)):
        el_top_geom = etree.Element("geometry")
        el_geom = encode_typegeometry_element(e)
        if el_geom is not None:
            el_top_geom.append(el_geom)
        yield el_top_geom
    # Check reference
    for e in element.get_subelements(lambda x: isinstance(x, HypergraphPort)):
        __ref_: HypergraphEdge = e.endpoint.parent
        for x in __ref_.get_outgoing_relations():
            for g in x.endpoint.get_subelements(lambda x: isinstance(x, HypergraphNode)):
                for __g in g.get_subelements(lambda x: isinstance(x, GeometryNode)):
                    el_top_geom = etree.Element("geometry")
                    el_geom = encode_typegeometry_element(__g)
                    el_top_geom.append(el_geom)
                    yield el_top_geom


def encode_visual_elements(element: HypergraphElement, material: VisualMaterial):
    el_visual = etree.Element("visual")
    el_visual.attrib["name"] = element.id_name
    for __x in extract_geometry_element(element):
        el_visual.append(__x)
    # Material
    el_material = etree.Element("material")
    el_script = etree.Element("script")
    el_script_uri = etree.Element("uri")
    el_script_uri.text = "file://media/materials/scripts/gazebo.material"
    el_material_name = etree.Element("name")
    # TODO: revise it to load from file
    el_material_name.text = '/'.join(["Gazebo", material["material_name"].capitalize()])
    el_script.append(el_script_uri)
    el_script.append(el_material_name)
    el_material.append(el_script)
    el_visual.append(el_material)
    yield el_visual


def encode_collision_elements(element: HypergraphElement):
    el_coll = etree.Element("collision")
    el_coll.attrib["name"] = element.id_name
    for __x in extract_geometry_element(element):
        el_coll.append(__x)
    yield el_coll


def encode_geometry_element(cont_node):
    # Visual & collision geometry setup
    sub_nodes = [x for x in cont_node.get_subelements(lambda x: isinstance(x, HypergraphNode))]
    __sem_collision = []
    __sem_visual = []
    __sem_material = {}
    for n in sub_nodes:
        geometries = [x for x in n.get_subelements(lambda x: isinstance(x, HypergraphNode))]
        mat = [x for x in n.get_subelements(lambda x: isinstance(x, VisualMaterial))]
        if len(mat) != 0:
            __sem_visual.extend(geometries)
            __sem_material = ({i: mat[0] for i in geometries})
        else:
            __sem_collision.extend(geometries)
    # Visual geometry setup
    for __v in __sem_visual:
        # Yield visual element
        yield from encode_visual_elements(__v, __sem_material[__v])
    # Collision geometry setup
    for __c in __sem_collision:
        yield from encode_collision_elements(__c)

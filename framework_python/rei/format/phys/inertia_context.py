
from lxml import etree

from rei.format.semantics.CognitiveEntity import InertiaElement, GeometryNode, CylinderGeometry, EllipsoidGeometry
from rei.hypergraph.base_elements import HypergraphNode


def encode_inertia_element(element):
    inertlist = [x for x in element.parent.get_subelements(lambda x: isinstance(x, InertiaElement))]
    __geom = []
    for _el in element.parent.get_subelements(lambda x: isinstance(x, HypergraphNode)):
        for _geom_node in _el.get_subelements(lambda x: isinstance(x, HypergraphNode)):
            __geom = list(_geom_node.get_subelements(lambda x: isinstance(x, GeometryNode)))
            break
        if len(__geom) > 0:
            break
    if len(inertlist) > 0:
        el_inertial = etree.Element("inertial")
        for iner in inertlist:
            el_mass = etree.Element("mass")
            m = iner["mass"]
            el_mass.text = str(m)
            el_inertial.append(el_mass)
            # Calculate inertia
            inertia_values = [1.0, 1.0, 1.0, 0.0, 0.0, 0.0]
            if len(__geom) > 0:
                for __g in __geom:
                    match __g:
                        case CylinderGeometry():
                            inertia_values = calc_cylinder_inertia(m, __g)
                        case EllipsoidGeometry():
                            inertia_values = calc_ellipsoid_inertia(m, __g)
            # Add inertia matrix elements
            el_ixx = etree.Element("ixx")
            el_ixx.text = str(inertia_values[0])
            el_iyy = etree.Element("iyy")
            el_iyy.text = str(inertia_values[1])
            el_izz = etree.Element("izz")
            el_izz.text = str(inertia_values[2])
            el_ixy = etree.Element("ixy")
            el_ixy.text = str(inertia_values[3])
            el_ixz = etree.Element("ixz")
            el_ixz.text = str(inertia_values[4])
            el_iyz = etree.Element("iyz")
            el_iyz.text = str(inertia_values[5])
            # Add remaining elements
            el_inertia = etree.Element("inertia")
            el_inertia.append(el_ixx)
            el_inertia.append(el_iyy)
            el_inertia.append(el_izz)
            el_inertia.append(el_ixy)
            el_inertia.append(el_ixz)
            el_inertia.append(el_iyz)
            el_inertial.append(el_inertia)
        yield el_inertial


def calc_cylinder_inertia(mass: float, geom: CylinderGeometry):
    l = geom['values'][0]
    r = geom['values'][1]
    ixy = 1.0/12.0*mass*(3*r*r+ l*l)
    izz = 0.5*mass*r*r
    return [ixy, ixy, izz, 0.0, 0.0, 0.0]

def calc_ellipsoid_inertia(mass: float, geom: EllipsoidGeometry):
    if len(geom['values']) == 1:
        r = geom['values'][0]
        ixyz = 2.0/5.0*mass*r*r
        return [ixyz, ixyz, ixyz, 0.0, 0.0, 0.0]



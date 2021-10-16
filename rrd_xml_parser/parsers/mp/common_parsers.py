from rrd_xml_parser.coord.es2wkt import EntitySpatialZUOut
from rrd_xml_parser.parsers.mp.mp_names import Geometry_check, NAMES_MP
from copy import deepcopy
from lxml.etree import QName
from rrd_xml_parser.models import Feature
from rrd_xml_parser.parsers.utils import nodes2str


def geometry_parser(feature, element, xpath_geom):
    if xpath_geom['names'].get('EntitySpatial', None):
        nodes = element.xpath(xpath_geom['names']['EntitySpatial'])
        if nodes:
            if len(nodes):
                esc = EntitySpatialZUOut(nodes[0])
                geometry = esc.wkt()
                del esc
                for geom in geometry:
                    feature.geometry = geom
                    yield feature

    if xpath_geom['names'].get('Contours', None):
        nodes = element.xpath(xpath_geom['names']['Contours'])
        if nodes:
            fields = xpath_geom['Contours']
            for node in nodes:
                esc = EntitySpatialZUOut(node)
                geometry = esc.wkt()
                del esc
                for geom in geometry:
                    new_feature = deepcopy(feature)
                    new_feature.registration_number = node.xpath(fields['registration_number'])
                    new_feature.area = node.xpath(fields['area'])
                    new_feature.geometry = geom
                    yield new_feature

    if xpath_geom['names'].get('NewContours', None):
        nodes = element.xpath(xpath_geom['names']['NewContours'])
        if nodes:
            fields = xpath_geom['NewContours']
            for node in nodes:
                esc = EntitySpatialZUOut(node)
                geometry = esc.wkt()
                del esc
                for geom in geometry:
                    new_feature = deepcopy(feature)
                    new_feature.registration_number = node.xpath(fields['registration_number'])
                    new_feature.area = node.xpath(fields['area'])
                    new_feature.geometry = geometry
                    yield new_feature

    if xpath_geom['names'].get('CompositionEZ', None):
        nodes = element.xpath(xpath_geom['names']['CompositionEZ'])
        if nodes:
            fields = xpath_geom['CompositionEZ']
            for node in nodes:
                esc = EntitySpatialZUOut(node)
                geometry = esc.wkt()
                del esc
                for geom in geometry:
                    new_feature = deepcopy(feature)
                    new_feature.registration_number = node.xpath(fields['registration_number'])
                    new_feature.area = node.xpath(fields['area'])
                    new_feature.geometry = geom
                    yield new_feature


def parts_parser(element, cls, xpaths, xpath_geom):
    parts = element.xpath(xpaths['name'])
    if parts:
        for node in parts:
            part = Feature()
            part_tag = QName(node).localname
            part.type = NAMES_MP[part_tag]
            part.parent = QName(element.tag).localname
            for k, v in xpaths['data'].items():
                nodes = node.xpath(v)
                value = nodes2str(nodes)
                setattr(part, k, value)
            if not element.xpath(Geometry_check):
                yield part
            else:
                yield from geometry_parser(part, node, xpath_geom)

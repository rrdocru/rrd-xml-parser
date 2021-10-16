# coding: utf-8
from copy import deepcopy
from lxml.etree import QName

from rrd_xml_parser.models import Feature
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.utils import nodes2str
from rrd_xml_parser.parsers.mp.utils import nodes2address
from rrd_xml_parser.parsers.mp import mp_names as names
from rrd_xml_parser.parsers.mp.common_parsers import geometry_parser, parts_parser


class ParserMP06(BaseParser):
    NAMESPACE = r'06'

    GROUPS = names.MP06_GroupList
    LEVELS = dict(
        MP=dict(
            Package=dict(
                FormParcels=dict(NewParcel=None,
                                 ChangeParcel=None,
                                 SpecifyRelatedParcel=None,
                                 SpecifyParcelApproximal=dict(ExistParcel=None,
                                                              ExistEZ=['ExistEZParcels', 'ExistEZEntryParcels'])
                                 ),
                SpecifyParcel=dict(ExistParcel=None,
                                   ExistEZ=['ExistEZParcels', 'ExistEZEntryParcels']),
                SubParcels=['NewSubParcel', 'ExistSubParcel'],
                SpecifyParcelsApproximal=dict(
                    SpecifyParcelApproximal=dict(ExistParcel=None,
                                                 ExistEZ=['ExistEZParcels', 'ExistEZEntryParcels'])
                )
            )
        )
    )

    @classmethod
    def geometry_parser_specify_related(cls, feature, element, xpath_geom):
        nodes = element.xpath(xpath_geom['names']['DeleteAllBorder'])
        nodes = element.xpath(xpath_geom['names']['ChangeBorder '])
        if not element.xpath(names.Geometry_check):
            yield feature
        else:
            yield from geometry_parser(feature, element, xpath_geom)

    @classmethod
    def _el2NewParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                # TODO: если получится переработать в общую функцию node2feature
                #   Дальше по тексту тоже
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.NEW_PARCEL.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes, xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.NEW_PARCEL_GEOMETRY)

                yield from parts_parser(element, cls, names.NEW_PARCEL_SUB_PARCELS,
                                        names.NEW_PARCEL_SUB_PARCELS_GEOMETRY)
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2ChangeParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.CHANGE_PARCEL.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                yield from parts_parser(element, cls, names.CHANGE_PARCEL_NEW_SUB, names.CHANGE_PARCEL_GEOMETRY_SUB)
                yield from parts_parser(element, cls, names.CHANGE_PARCEL_EXIST_SUB, names.CHANGE_PARCEL_GEOMETRY_SUB)
                yield from parts_parser(element, cls, names.CHANGE_PARCEL_INVARIABLE_SUB,
                                        names.CHANGE_PARCEL_GEOMETRY_SUB)
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2SpecifyRelatedParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.SPECIFY_RELATED_PARCELS.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.SPECIFY_RELATED_PARCELS_GEOMETRY)

                yield from parts_parser(element, cls, names.SPECIFY_RELATED_SUB_PARCELS,
                                        names.SPECIFY_RELATED_SUB_GEOMETRY)
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2ExistEZParcels(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.SPECIFY_PARCEL_EXIST.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.SPECIFY_PARCEL_GEOMETRY)

                yield from parts_parser(element, cls, names.SPECIFY_PARCEL_NEW_SUB, names.SPECIFY_PARCEL_SUB_GEOMETRY)
                yield from parts_parser(element, cls, names.SPECIFY_PARCEL_EXIST_SUB, names.SPECIFY_PARCEL_SUB_GEOMETRY)
                parts = element.xpath(names.SPECIFY_PARCEL_INVARIABLE_SUB['name'])
                if parts:
                    for node in parts:
                        part = Feature()
                        part_tag = QName(node).localname
                        part.type = names.NAMES_MP[part_tag]
                        for k, v in names.SPECIFY_PARCEL_INVARIABLE_SUB['data'].items():
                            nodes = node.xpath(v)
                            value = nodes2str(nodes)
                            setattr(part, k, value)
                        contours = element.xpath(names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['name'])
                        if contours:
                            for contour in contours:
                                new_feature = deepcopy(feature)
                                new_feature.registration_number = contour.xpath(
                                    names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['registration_number'])
                                new_feature.area = contour.xpath(
                                    names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['area'])
                                yield new_feature

                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2ExistParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.SPECIFY_PARCEL_EZ.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.SPECIFY_PARCEL_GEOMETRY)

                yield from parts_parser(element, cls, names.SPECIFY_PARCEL_NEW_SUB, names.SPECIFY_PARCEL_SUB_GEOMETRY)
                yield from parts_parser(element, cls, names.SPECIFY_PARCEL_EXIST_SUB, names.SPECIFY_PARCEL_SUB_GEOMETRY)
                parts = element.xpath(names.SPECIFY_PARCEL_INVARIABLE_SUB['name'])
                if parts:
                    for node in parts:
                        part = Feature()
                        part_tag = QName(node).localname
                        part.type = names.NAMES_MP[part_tag]
                        for k, v in names.SPECIFY_PARCEL_INVARIABLE_SUB['data'].items():
                            nodes = node.xpath(v)
                            value = nodes2str(nodes)
                            setattr(part, k, value)
                        contours = element.xpath(names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['name'])
                        if contours:
                            for contour in contours:
                                new_feature = deepcopy(feature)
                                new_feature.registration_number = contour.xpath(
                                    names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['registration_number'])
                                new_feature.area = contour.xpath(
                                    names.SPECIFY_PARCEL_INVARIABLE_SUB['geometry']['area'])
                                yield new_feature

                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2NewSubParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.PACKAGE_SUB_PARCEL_NEW.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.PACKAGE_SUB_PARCEL_NEW_GEOM)

                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2ExistSubParcel(cls, context, tag_exit):
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname
            if element_tag == tag_exit and event == 'end':
                feature = Feature()
                feature.type = names.NAMES_MP[tag_exit]
                for k, v in names.PACKAGE_SUB_PARCEL_EXIST.items():
                    nodes = element.xpath(v)
                    value = None
                    if k == 'address':
                        if len(nodes) > 0:
                            value = nodes2address(nodes[0], xpaths=names.ADDRESS, namespaces=cls.NAMESPACES)
                    else:
                        value = nodes2str(nodes)
                    setattr(feature, k, value)

                if not element.xpath(names.Geometry_check):
                    yield feature
                else:
                    yield from geometry_parser(feature, element, names.PACKAGE_SUB_PARCEL_EXIST_GEOM)

                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)


settings_pars = {
    'mp': {
        'versions': {
            ParserMP06.NAMESPACE: ParserMP06,
        }
    }
}

import itertools
import logging
from abc import ABCMeta, abstractmethod
from typing import List, Union
from lxml.etree import QName, _Element
from shapely import wkt
from shapely.geometry import Polygon, MultiPolygon, LineString, Point
from rrd_xml_parser.coord.node2wkt import TContour, TSpatialElement

logger = logging.getLogger(__name__)


def node2coord(element, context, **kwargs):
    """
    Преобразование xml-элемента в геометрию

    :param _Element element: xml-элемент
    :param context: контекст вычислени (зу, окс, образование, изменение)
    :param kwargs: дополнительные именованные аргументы
    :key namespaces: словарь namespaces
    :return:
    """

    # eapl, ebpl, kpt11 land_record
    if context == 'entityspatialzu':
        return EntitySpatialZU(element, **kwargs)

    # KVZU_07, KPZU_06, KPT_10
    elif context == 'entityspatialzuout':
        return EntitySpatialZUOut(element, **kwargs)

    elif context == 'entityspatialzuout_ez':
        return EntitySpatialZUOut_EZ(element, **kwargs)

    # eapc, ebpc, kpt11 build_record и т.п.
    elif context == 'entityspatialoks':
        return EntitySpatialOKS(element, **kwargs)

    # KVOKS_03, KPOKS_04, KPT_10 Building, Construction, Uncompleted
    elif context == 'entityspatialoskout':
        return EntitySpatialOKSOut(element, **kwargs)

    # KPT_10, KPT_11 OMSPoint
    if context == 'entityspatialoms':
        return EntitySpatialOMS(element, **kwargs)

    else:
        return EntitySpatialZUOut(element)


class SpatialConvertor:
    __metaclass__ = ABCMeta

    element = None  # type: Union[_Element, List[_Element]]
    namespaces = None

    def __init__(self, element: Union[_Element, List[_Element]], **kwargs: dict):
        """
        Объект инициализации очередного экземпляра SpatialConvertor

        :param element: одиночный или список xml-элементов
        :type element: Union[_Element, List[_Element]]
        :param dict kwargs: дополнительные ключевые аргументы
        :key dict namespaces: словарь namespaces
        """

        self.namespaces = kwargs.get('namespaces', None)
        self.element = []
        if isinstance(element, list):
            self.element += element
        else:
            self.element.append(element)

    def _spelement2list(self, node):
        """
        Преобразование xml-элемента в список координат
        :param _Element node: xml-элемента
        :param str prefix: namespace для координат

        :return: list[tuple(float, float)]
        """
        list_x = node.xpath('.//@X | .//x/text() | .//_x/text()', namespaces=self.namespaces)
        list_y = node.xpath('.//@Y | .//y/text() | .//_y/text()', namespaces=self.namespaces)
        # NOTE: обмен координат местами
        return [(float(c[0]), float(c[1])) for c in
                itertools.zip_longest(list_y, list_x, fillvalue=0.0)]  # noqa

    def to_WKT(self):
        return self.wkt()

    @abstractmethod
    def wkt(self):
        pass


class EntitySpatialZU(SpatialConvertor):
    """
    Класс преобразования типа ContourZU

    Используется в eapl, ebpl, ktp11 land_record
    """
    def __init__(self, contour, **kwargs):
        self.element = contour
        self.namespaces = kwargs.get('namespaces', None)

    def wkt(self):
        return [TContour(self.element).wkt]


class EntitySpatialZUOut(SpatialConvertor):
    """
    При извлечении координат из xml массив формируется в порядке следования координат Ordinate.Y, Ordinate.X
    """

    def wkt(self):
        result = []
        for entityspatial in self.element:
            contour_parts = []
            spelements = entityspatial.xpath('./*[translate(local-name(), "_", "")="SpatialElement"]', namespaces=self.namespaces)
            for spelement in spelements:
                coords = self._spelement2list(spelement)
                if len(coords) < 3:
                    logger.error('Контур земельного участка состоит меньше чем из 3-х точек. {}'.format(coords))
                else:
                    contour_parts.append(coords)
            try:
                result.append(wkt.dumps(Polygon(contour_parts[0], contour_parts[1:]), rounding_precision=2))
            except Exception as e:
                logger.error(e)
                logger.debug(result)
        return result


class EntitySpatialZUOut_EZ(EntitySpatialZUOut):
    """
    При извлечении координат из xml массив формируется в порядке следования координат Ordinate.Y, Ordinate.X
    """

    def __init__(self, element, **kwargs):
        super().__init__(element, **kwargs)
        self.element = element.xpath('./a:EntitySpatial', namespaces=self.namespaces)


class EntitySpatialOKS(SpatialConvertor):
    """
    Класс преобразования типа ContourOKS

    Используется в ktp11 build_record
    """

    def wkt(self):
        return [TSpatialElement(spelement).wkt for spelement in self.element]


class EntitySpatialOKSOut(SpatialConvertor):

    def wkt(self):
        results = []
        for spelement in self.element:
            coord = self._spelement2list(spelement)
            if len(coord) == 1:  # Точка
                result = Point(coord[0])
            else:
                if coord[0] == coord[-1] and len(coord) > 2:
                    result = Polygon(coord)
                else:
                    result = LineString(coord)
            results.append(wkt.dumps(result, rounding_precision=2))
        return results


class EntitySpatialOMS(SpatialConvertor):

    def _spelement2list(self, node):
        list_x = node.xpath('a:OrdX/text() | ord_x/text()', namespaces=self.namespaces)
        list_y = node.xpath('a:OrdY/text() | ord_y/text()', namespaces=self.namespaces)
        # NOTE: обмен координат местами
        return [(float(c[0]), float(c[1])) for c in itertools.zip_longest(list_y, list_x, fillvalue=0.00)]

    def wkt(self):
        return [wkt.dumps(Point(self._spelement2list(point)), rounding_precision=2) for point in self.element]


class EntitySpatialOldNew(SpatialConvertor):
    entity_spatial = None

    def __init__(self, entity_spatial, old=True):
        self.entity_spatial = entity_spatial
        self._old = old

    def _spelement2list(self, node, **kwargs):
        """
        Преобразование xml-элемента в список координат
        :param _Element node: xml-элемента
        :param str prefix: namespace для координат

        :return: list[tuple(float, float)]
        """
        if self._old:
            list_x = node.xpath('.//OldOrdinate/@X')
            list_y = node.xpath('.//OldOrdinate/@Y')
        else:
            list_x = node.xpath('.//NewOrdinate/@X')
            list_y = node.xpath('.//NewOrdinate/@Y')
        return [(float(c[0]), float(c[1])) for c in itertools.zip_longest(list_x, list_y, fillvalue=0.0)]  # noqa

    def wkt(self):
        result = None
        poly_list = []
        for spelement in self.entity_spatial:
            coord = self._spelement2list(spelement)
            if coord[0] == coord[-1]:
                if len(poly_list) == 0:
                    poly_list.append(Polygon(coord))
                else:
                    if poly_list[-1].contains(Polygon(coord)):
                        poly_list[-1] = poly_list[-1] - Polygon(coord)
                    else:
                        poly_list.append(Polygon(coord))
            else:
                return LineString(coord)
        if len(poly_list) == 1:
            return poly_list[0].wkt
        else:
            return MultiPolygon(poly_list).wkt


import logging
from shapely import wkt, wkb
from shapely.geometry import Point, MultiPoint, LineString, MultiLineString, Polygon, MultiPolygon, GeometryCollection
from shapely.geometry.base import BaseGeometry, EMPTY


logger = logging.getLogger(__name__)


def geometry2wkt(geometry):
    """
    Преобразование объекта BaseGometry в wkt формат с округлением до 2-х символов

    :param BaseGeometry geometry: объект геометрии

    :return: wkt представление геометрии
    :rtype: str
    """
    return wkt.dumps(geometry, rounding_precision=2)


def geometry2wkb(geometry):
    """
    Преобразование объекта BaseGometry в wkb формат с округлением до 2-х символов

    :param BaseGeometry geometry: объект геометрии

    :return: wkb представление геометрии
    :rtype: str
    """
    return wkb.dumps(geometry, rounding_precision=2)


class TOrdinate:
    """
    Класс описания одной точки
    """
    def __init__(self, node):
        self._geom = None  # type: BaseGeometry
        for element in node:
            setattr(self, element.tag.strip('_'), element.text)

    def __str__(self):
        return self.wkt

    def __eq__(self, other):
        return self.xy() == other.xy()

    def __ne__(self, other):
        return self.xy() != other.xy()

    def has_z(self):
        return getattr(self, 'z', False)

    def has_r(self):
        return getattr(self, 'r', False)

    def _to_geometry(self):
        if self._geom:
            return self._geom

        attr_x = getattr(self, 'x', None) or getattr(self, 'ord_x', None)
        attr_y = getattr(self, 'y', None) or getattr(self, 'ord_y', None)
        x, y = None, None

        if attr_x and attr_y:
            try:
                # NOTE: изменение порядка координат из геодезического на декартовый
                y, x = float(attr_x), float(attr_y)
            except Exception as e:
                logger.exception(e)

            if x is not None and y is not None:
                self._geom = Point(x, y)
            # NOTE: в случае эллипса можно выдавать буфер или координаты точки
            # if self.has_r():
            #     self._geom = self._geom.buffer(float(getattr(self, 'r', 0.0)))
        return self._geom

    @property
    def geometry(self):
        """
        Геометрия в формате Shapely

        :return: Геометрия
        :rtype: BaseGeometry
        """
        return self._to_geometry()

    @property
    def wkt(self):
        """
        Координата в wkt-формате

        :return: координаты точки в формате WKT
        :rtype: str
        """
        return geometry2wkt(self.geometry) if self.geometry else None

    @property
    def wkb(self):
        """
        Координата в wkb-формате

        :return: координаты точни в формате WKT
        :rtype: str
        """
        return geometry2wkb(self.geometry) if self.geometry else None

    def xy(self):
        """
        X, Y представление координат

        :return: x, y
        :rtype: tuple
        """
        _point = self._to_geometry()
        if not _point:
            return None
        _x, _y = _point.x, _point.y
        del _point
        return _x, _y


class TOrdinates:
    """
    Класс описания списка точек (контура)
    """
    def __init__(self, node):
        self.list_ordinate = []
        for element in node:
            self.list_ordinate.append(TOrdinate(element))

    def __len__(self):
        return len(self.list_ordinate)

    def xy(self):
        """
        Список представлений x,y координат

        :return: список координат
        :rtype: list[typle]
        """
        # ((1, 1), (2, 2), ...)
        return [ordinate.xy() for ordinate in self.list_ordinate]

    def is_point(self):
        """
        Является ли геометрия точкой

        :return:
        :rtype: bool
        """
        return len(self.list_ordinate) == 1

    def is_line(self):
        """
        Является ли геометрия линией

        :return:
        :rtype: bool
        """
        return self.list_ordinate[0] != self.list_ordinate[-1]

    def is_closed(self):
        """
        Является ли геометрия замкнутым контуром

        :return:
        :rtype: bool
        """
        return self.list_ordinate[0] == self.list_ordinate[-1]


class TSpatialElement:
    """
    Класс описания элемента контура

    """

    def __init__(self, node):
        self._geom = None

        self.ordinates = TOrdinates(node.xpath('./ordinates')[0])

    def __getitem__(self, item):
        return self.ordinates.list_ordinate[item]

    def __len__(self):
        return len(self.ordinates)

    def __iter__(self):
        self._index = 0
        self._length = len(self)
        return self

    def __next__(self):
        if self._index < self._length:
            ordinate = self.ordinates.list_ordinate[self._index]
            self._index += 1
            return ordinate
        else:
            raise StopIteration

    def xy(self):
        """
        Список представлений x,y координат

        :return: список координат
        :rtype: list[type]
        """
        return self.ordinates.xy()

    def is_point(self):
        """
        Является ли элемент контура точкой

        :return:
        :rtype: bool
        """
        return self.ordinates.is_point()

    def is_line(self):
        """
        Является ли элемент контура линией

        :return:
        :rtype: bool
        """
        return self.ordinates.is_line()

    def is_closed(self):
        """
        Является ли элемент контура замкнутым контуром

        :return:
        :rtype: bool
        """
        return self.ordinates.is_closed()

    def _has_geometry(self):
        return len(self) != 0

    def _to_geometry(self):
        if not self._has_geometry():
            return EMPTY()

        if self._geom:
            return self._geom

        # Контур без дырок (всё просто)

        if self.is_point():
            self._geom = self[0].geometry
        elif self.is_line():
            self._geom = LineString(self.xy())
        else:
            self._geom = Polygon(self.xy())
        return self._geom

    @property
    def geometry(self):
        return self._to_geometry()

    @property
    def wkt(self):
        return geometry2wkt(self.geometry) if self.geometry else None

    @property
    def wkb(self):
        return geometry2wkb(self.geometry) if self.geometry else None


class TSpatialElements:
    """
    Класс описания элементов контура
    """
    def __init__(self, node):
        self.list_spatial_element = []
        for element in node:
            self.list_spatial_element.append(TSpatialElement(element))

    def __getitem__(self, item):
        return self.list_spatial_element[item]

    def __len__(self):
        return len(self.list_spatial_element)

    def __iter__(self):
        self._index = 0
        self._length = len(self)
        return self

    def __next__(self):
        if self._index < self._length:
            spatial_element = self.list_spatial_element[self._index]
            self._index += 1
            return spatial_element
        else:
            raise StopIteration

    def xy(self):
        """
        Список представлений x,y координат

        :return: список координат
        :rtype: list[typle]
        """

        return [spatial_element.xy() for spatial_element in self.list_spatial_element]

    @property
    def geometry(self):
        return [spatial_element.geometry for spatial_element in self]

    @property
    def wkt(self):
        return [spatial_element.wkt for spatial_element in self]

    @property
    def wkb(self):
        return [spatial_element.wkb for spatial_element in self]


class TEntitySpatial:
    def __init__(self, node):
        sp_elements = node.xpath('./spatials_elements')
        self.spatial_elements = TSpatialElements(sp_elements[0] if len(sp_elements) > 0 else [])

    def __len__(self):
        return len(self.spatial_elements)

    def __getitem__(self, item):
        return self.spatial_elements[item]

    def xy(self):
        """
        Список представлений x,y координат

        :return: список координат
        :rtype: list[typle]
        """
        return self.spatial_elements.xy()


class TContour:

    entity_spatial = None  # type: TEntitySpatial

    def __init__(self, node):
        self._geom = None  # type: BaseGeometry

        # NOTE: бывают случаи когда ветка котруров есть, а координат внутри них нет
        es = node.xpath('.//entity_spatial')
        if len(es) != 0:
            self.entity_spatial = TEntitySpatial(es[0])
        else:
            logger.warning('Пустая геометрия в объекте, хотя должна быть заполнена!')

    def xy(self):
        return self.entity_spatial.xy()

    def _has_geometry(self):
        return self.entity_spatial is not None and len(self.entity_spatial) != 0

    def _to_geometry(self):
        if not self._has_geometry():
            return

        if self._geom:
            return self._geom

        # Контур без дырок (всё просто)
        if len(self.entity_spatial) == 1:
            spatial_element = self.entity_spatial[0]
            if spatial_element.is_point():
                self._geom = Point(spatial_element.xy())
            elif spatial_element.is_line():
                self._geom = LineString(spatial_element.xy())
            else:
                self._geom = Polygon(spatial_element.xy())

        # Контур с дырками или последовательность объектов (опоры), линейные объекты, эллипсы
        else:
            _points = []
            _lines = []
            _polygons = []
            for spatial_element in self.entity_spatial.spatial_elements:
                if spatial_element.is_point():
                    _points.append(spatial_element.xy())
                elif spatial_element.is_line():
                    _lines.append(spatial_element.xy())
                else:
                    _polygons.append(spatial_element.xy())
            if _points and not _lines and not _polygons:
                self._geom = MultiPoint(_points)
            elif _lines and not _points and not _polygons:
                self._geom = MultiLineString(_lines)
            elif _polygons and not _points and not _lines:
                self._geom = Polygon(_polygons[0], _polygons[1:])
            else:
                self._geom = GeometryCollection([MultiPoint(_points), MultiLineString(_lines), Polygon(_polygons[0], _polygons[1:])])
        return self._geom

    @property
    def geometry(self):
        return self._to_geometry()

    @property
    def wkt(self):
        return geometry2wkt(self.geometry) if self.geometry else None

    @property
    def wkb(self):
        return geometry2wkb(self.geometry) if self.geometry else None


class TContours:
    def __init__(self, node):
        self.contours = []
        self._geom = None   # type: BaseGeometry
        for element in node:
            self.contours.append(TContour(element))

    def _has_geom(self):
        return len(self.contours) != 0

    def _node_to_geom(self):
        """
        Земельный участок в геометрию

        Отличительной особенностью является то, что участок не может быть линией и точной
        :param node: xml-элемент
        :return GEOSGeometry
        """
        def __contour_to_geom(coords):
            if isinstance(coords, TSpatialElements):
                coords = coords.xy()

            _shell = coords[0]
            if len(_shell) < 3:
                logger.exception('В полигоне должно быть не менее 3-х точек')
                return

            _holes = []
            for _hole in coords[1:]:
                if len(_hole) < 3:
                    logger.exception('Во полигоне должно быть не менее 3-х точек')
                    continue
                _holes.append(_hole)
            return Polygon(_shell, _holes)

        if not self._has_geom():
            return

        # Одноконтурный земельный участок
        if len(self.contours) == 1:
            return __contour_to_geom(self.contours[0].xy())

        else:
            _polys = []
            for contour in self.contours:
                _poly = __contour_to_geom(contour.xy())
                if _poly:
                    _polys.append(_poly)
            if len(_polys):
                return MultiPolygon(_polys)

    def _node_to_geomcollection(self):

        def __contour_to_geom(contour):

            # Контур без дырок
            if len(contour.entity_spatial) == 1:
                spatial_element = contour.entity_spatial[0]
                if spatial_element.is_point():
                    return Point(spatial_element.xy())
                elif spatial_element.is_line():
                    return LineString(spatial_element.xy())
                else:
                    return Polygon(spatial_element.xy())
            # Контур с дырками или последовательность объектов (опоры), линейные объекты, эллипсы
            else:
                _points = []
                _lines = []
                _polygons = []
                for spatial_element in contour.entity_spatial.spatial_elements:
                    if spatial_element.is_point():
                        _points.append(Point(spatial_element.xy()))
                    elif spatial_element.is_line():
                        _lines.append(LineString(spatial_element.xy()))
                    else:
                        _polygons.append(Polygon(spatial_element.xy()))
                if _points and not _lines and not _polygons:
                    return MultiPoint(_points)
                elif _lines and not _points and not _polygons:
                    return MultiLineString(_lines)
                elif _polygons and not _points and not _lines:
                    return Polygon(_polygons[0], _polygons[1:])
                else:
                    return GeometryCollection([MultiPoint(_points), MultiLineString(_lines), MultiPolygon(_polygons)])

        if not self._has_geom():
            return

        # Одноконтурный земельный участок
        if len(self.contours) == 1:
            return __contour_to_geom(self.contours[0])
        # Многоконтурный земельный участок
        else:
            _geoms = []
            for contour in self.contours:
                _geom = __contour_to_geom(contour)
                if not _geoms:
                    _geoms = _geom
                else:
                    _geoms = _geoms.union(_geom)

    def _to_geometry(self):
        if not self._has_geom():
            return

        if self._geom:
            return self._geom

        if len(self.contours) == 1:
            self._geom = self.contours[0].geometry
        # Многоконтурный земельный участок
        else:
            for contour in self.contours:
                if not self._geom:
                    self._geom = contour.geometry
                else:
                    self._geom = self._geom.union(contour.geometry)

        return self._geom

    @property
    def geometry(self):
        """Геометрия объекта"""
        return self._to_geometry()

    @property
    def wkt(self):
        """
        Геометрия в wkt-формате

        :return: координаты точки в формате WKT
        :rtype: str
        """
        return geometry2wkt(self.geometry) if self.geometry else None

    @property
    def wkb(self):
        """
        Геометрия в wkb-формате

        :return: координаты точки в формате WKT
        :rtype: str
        """
        return geometry2wkb(self.geometry) if self.geometry else None


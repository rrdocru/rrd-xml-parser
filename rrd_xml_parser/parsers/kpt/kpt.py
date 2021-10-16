import logging
from lxml.etree import QName

from rrd_xml_parser.models import Feature
from rrd_xml_parser.parsers.base import BaseParser
from rrd_xml_parser.parsers.kpt import kpt_names, extract_names
from rrd_xml_parser.parsers.mixins import BaseMixin
from rrd_xml_parser.parsers.names import NAMES
from rrd_xml_parser.parsers.utils import node2feature

logger = logging.getLogger(__name__)


class ParserKPT10(BaseParser):
    NAMESPACE = r'urn://x-artefacts-rosreestr-ru/outgoing/kpt/10.0.1'
    GROUPS = kpt_names.KPT10_GroupList
    LEVELS = dict(
        KPT=dict(
            CadastralBlocks=dict(
                CadastralBlock=dict(
                    Parcels=dict(
                        Parcel=None
                    ),
                    ObjectsRealty=dict(
                        ObjectRealty=dict(
                            Building=None,
                            Construction=None,
                            Uncompleted=None
                        )
                    ),
                    OMSPoints=dict(
                        OMSPoint=None
                    ),
                    SpatialData=None,
                    Bounds=dict(
                        Bound=None
                    ),
                    Zones=dict(
                        Zone=None
                    )
                )
            )
        )
    )
    NAMESPACES = dict(
        # a можно заменить на root, например, но тогда придётся менять все xpath-выражения
        a="urn://x-artefacts-rosreestr-ru/outgoing/kpt/10.0.1",
        adrs="urn://x-artefacts-rosreestr-ru/commons/complex-types/address-output/4.0.1",
        spa="urn://x-artefacts-rosreestr-ru/commons/complex-types/entity-spatial/5.0.1",
        param="urn://x-artefacts-rosreestr-ru/commons/complex-types/parameters-oks/2.0.1",
        doc="urn://x-artefacts-rosreestr-ru/commons/complex-types/document-output/4.0.1",
        cer="urn://x-artefacts-rosreestr-ru/commons/complex-types/certification-doc/1.0",
        smev="urn://x-artefacts-smev-gov-ru/supplementary/commons/1.0.1",
    )

    @classmethod
    def _node2feature(cls, context, tag_exit, xpaths, check_object):
        """
        Функция преобразования xml-элемента в Feature

        :param context: итератор по xml-документу
        :param str tag_exit: имя xml-элемента для выхода из функции
        :param dict xpaths: словарь xpath-выражений для извлечения атрибутов
        :param check_object: функция проверки типа геометрии объекта
        """
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element=element,
                    xpaths=xpaths,
                    feature_type=NAMES[tag_exit],
                    namespaces=cls.NAMESPACES,
                    check_object_subtype=check_object
                )

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2Parcel(cls, context, tag_exit):
        logger.debug('Обработка КПТ 10 Участков')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_PARCEL_XPATHS,
                                     lambda feature, element: int(getattr(feature, 'subtype_code', 1)))

    @classmethod
    def _el2Building(cls, context, tag_exit):
        """
        Функция разбора объекта капительного строительства
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Зданий')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_OBJECTSREALTY_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2Construction(cls, context, tag_exit):  # TODO: не работает парсинг координат
        """
        Функция разбора объекта капительного строительства
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Сооружений')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_OBJECTSREALTY_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2Uncompleted(cls, context, tag_exit):
        """
        Функция разбора объекта капительного строительства
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Объектов незавершённого строительства')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_OBJECTSREALTY_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2OMSPoint(cls, context, tag_exit):
        """
        Функция разбора пункта ОМС
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 ОМС')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_OMS_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2SpatialData(cls, context, tag_exit):
        """
        Функция разбора границы кадастрового квартала
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Квартала')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_SPATIALDATA_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2Bound(cls, context, tag_exit):
        """
        Функция разбора границы муниципального образования
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Границ')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_BOUND_XPATHS,
                                     lambda feature, element: False)

    @classmethod
    def _el2Zone(cls, context, tag_exit):
        """
        Функция разбора зоны с особыми условиями испльзования
        :param context: объект возвращаемый функцией etree.iterparse из библиотеки lxml
        :param tag_exit: тег по которму выходить из процедуры
        :return: Feature
        """
        logger.debug('Обработка КПТ 10 Зон')
        yield from cls._node2feature(context, tag_exit, kpt_names.KPT10_ZONE_XPATHS,
                                     lambda feature, element: False)


class ParserExtractCadastralPlanTerriroty(BaseParser, BaseMixin):
    NAMESPACE = 'extract_cadastral_plan_territory'
    GROUPS = extract_names.KPT11_GroupList
    LEVELS = dict(
        extract_cadastral_plan_territory=dict(
            cadastral_blocks=dict(
                cadastral_block=dict(
                    record_data=dict(
                        base_data=dict(
                            land_records=dict(
                                land_record=None
                            ),
                            build_records=dict(
                                build_record=None
                            ),
                            construction_records=dict(
                                construction_record=None
                            ),
                            object_under_construction_records=dict(
                                object_under_construction_record=None
                            )
                        )
                    ),
                    spatial_data=None,
                    subject_boundaries=dict(
                        subject_boundary_record=None
                    ),
                    municipal_boundaries=dict(
                        municipal_boundary_record=None
                    ),
                    inhabited_locality_boundaries=dict(
                        inhabited_locality_boundary_record=None
                    ),
                    coastline_boundaries=dict(
                        coastline_record=None
                    ),
                    zones_and_territories_boundaries=dict(
                        zones_and_territories_record=None
                    ),
                    surveying_project=dict(
                        surveying_project_record=None
                    ),
                    oms_points=dict(
                        oms_point=None
                    )
                )
            )
        )
    )

    @classmethod
    def _node2feature(cls, context, tag_exit, xpaths, check_geometry_callback):
        """
        Функция преобразования xml-элемента в Feature

        :param context: итератор по xml-документу
        :param str tag_exit: имя xml-элемента для выхода из функции
        :param dict xpaths: словарь xpath-выражений для извлечения атрибутов
        :param check_geometry_callback: функция проверки типа геометрии объекта
        """
        for event, element in context:
            # event == start
            element_tag = QName(element.tag).localname

            # Если дошли до тега выхода, то выходим из цикла по context
            if element_tag == tag_exit and event == 'end':
                yield from node2feature(
                    element=element,
                    xpaths=xpaths,
                    feature_type=NAMES[tag_exit],
                    namespaces=cls.NAMESPACES,
                    check_object_subtype=check_geometry_callback
                )

                # Очистка ветки xml
                element.clear()
                while element.getprevious() is not None:
                    del element.getparent()[0]
                return
            else:
                cls._pass(context, element_tag)

    @classmethod
    def _el2land_record(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_land_record_names,
                                     lambda feature, element: int(getattr(feature, 'subtype_code', 1) or 1))

    @classmethod
    def _el2build_record(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_building_names,
                                     lambda feature, element: False)

    @classmethod
    def _el2construction_record(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_construction_names,
                                     lambda feature, element: False)

    @classmethod
    def _el2object_under_construction_record(cls, context, tag_exit):
        """
        Функция преобразования элемента `объект незавершенного строительства`

        :param context:
        :param tag_exit:
        :return:
        """
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_under_construction_names,
                                     lambda feature, element: False)

    @classmethod
    def _el2spatial_data(cls, context, tag_exit):
        """
        Функция преобразования элемента `местоположение квартала`

        :param context:
        :param tag_exit:
        :return:
        """

        def check_geometry_type(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return False

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_spatial_data_names, check_geometry_type)

    @classmethod
    def _el2subject_boundary_record(cls, context, tag_exit):
        def is_multi(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return not (len(element.xpath('.//contours/contour')) == 1)

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_subject_boundaries_names, is_multi)

    @classmethod
    def _el2municipal_boundary_record(cls, context, tag_exit):

        def is_multi(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return not (len(element.xpath('.//contours/contour')) == 1)

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_municipal_boundary_record_names, is_multi)

    @classmethod
    def _el2inhabited_locality_boundary_record(cls, context, tag_exit):

        def is_multi(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return not (len(element.xpath('.//contours/contour')) == 1)

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_inhabited_locality_boundary_record_names,
                                     is_multi)

    @classmethod
    def _el2coastline_record(cls, context, tag_exit):

        def is_multi(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return not (len(element.xpath('.//contours/contour')) == 1)

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_coastline_record_names, is_multi)

    @classmethod
    def _el2zones_and_territories_record(cls, context, tag_exit):

        def is_multi(feature, element):
            """
            Функция проверки типа геометри объекта

            :param Feature feature: созданный
            :param kwargs:
            :return:
            """
            return not (len(element.xpath('.//contours/contour')) == 1)

        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_zones_and_territories_record_names,
                                     is_multi)

    @classmethod
    def _el2surveying_project_record(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_surveying_project_record_names,
                                     lambda feature, element: False)

    @classmethod
    def _el2oms_point(cls, context, tag_exit):
        yield from cls._node2feature(context, tag_exit, extract_names.KPT11_oms_point,
                                     lambda feature, element: False)


setting_pars = {
    'kpt': {
        'versions': {
            ParserKPT10.NAMESPACE: ParserKPT10
        }
    },
    'extract_cadastral_plan_territory': {
        'versions': {
            ParserExtractCadastralPlanTerriroty.NAMESPACE: ParserExtractCadastralPlanTerriroty
        }
    }
}

# coding: utf-8
import re
from copy import deepcopy

from lxml.etree import _Element
from rrd_xml_parser.coord.es2wkt import node2coord
from rrd_xml_parser.models import *

logger = logging.getLogger(__name__)


def nodes2str(nodes):
    """
    Функция извлечения из списка(элемента) текстового значения

    :param nodes:
    :type: list, str
    :return: строковое значение
    """
    if (type(nodes) == list and len(nodes) == 0) or (nodes is None):
        return

    if type(nodes) == list:
        if len(nodes) == 1:
            value = nodes2str(nodes[0])
        else:
            value_list = [nodes2str(node) for node in nodes]
            value = ', '.join([val for val in value_list if val])
    elif type(nodes) == _Element:
        value = nodes.text
    else:
        value = nodes

    # NOTE: Дополнительная проверка. Т.к. в одном месте наткнулись на то, что элемент есть, то возвращает None
    if value is not None:
        value = re.sub(r'[\r\n\t]', ' ', value).strip()
        value = re.sub(r'^[\-]', '', value)  # удалиние дефисов в начале строки
        value = re.sub(r'&quot;', '', value)
        value = re.sub(r'\(\)', '', value)  # удаление пустых скобок в конце номера
    # NOTE: пусты скобки появляются в выписках из ЕГРН для многоконтурных участков если в контуре не задан его номер
    return value or None


def nodes2model(model, elements, xpaths, namespaces=None):
    """
    Функция преобразования элемента в экземпляр модели

    :param class model: класс модели
    :param _Element elements: cписок xml-элементов, но берётся всегда первый если он есть
    :param dict xpaths: спиосок xpath-выражений
    :param dict namespaces: словарь namespaces

    :return: instance
    :rtype: object
    """
    if len(elements) == 0:
        return None
    element = elements[0]
    instance = model()
    for k, v in xpaths.items():
        nodes = element.xpath(v, namespaces=namespaces)
        value = nodes2str(nodes)
        # В поле `адрес` мун.обр может прийти `.`. Это не недо писать в объект
        if value:
            value = value.strip('.')
        # Вторая проверка для того чтобы не записывать пустые строки в объект после первой проверки
        if value:
            setattr(instance, k, value)
    return instance


def node2attributes(element, xpaths, context, namespaces=None, feature=None):
    """
    Получение атрибутивной информации об объекте

    :param element: xml-элемент
    :param dict xpaths: спиосок xpath-выражений
    :param str context: тип объекта
    :param dict namespaces: словарь namespaces
    :param Feature feature: возвращаемый объект
    :return:
    """
    if feature is None:
        feature = Feature()
        feature.type = context

    # Обработка семантики
    for k, v in xpaths.items():
        try:
            if k == 'geometry':
                # NOTE: геометрия обрабатывается отдельно
                continue
            if isinstance(v, AttributeModel):
                nodes = element.xpath(v.base, namespaces=namespaces)
                value = nodes2model(v.model, elements=nodes, xpaths=v.xpath, namespaces=namespaces)
            elif isinstance(v, AttributeDict):
                if not hasattr(feature, k):
                    cls = feature.__class__
                    setattr(cls, k, DictionaryFeatureDescriptor(v.dict))
                nodes = element.xpath(v.xpath, namespaces=namespaces)
                value = nodes2str(nodes)
            else:
                nodes = element.xpath(v, namespaces=namespaces)
                value = nodes2str(nodes)
            setattr(feature, k, value)
        except Exception as e:
            logger.error('Ошибка обработки элемента. Ключ: {}. Значение: {}'.format(k, v))
            logger.exception(e)
    return feature


def node2feature(element, xpaths, feature_type, namespaces=None, check_object_subtype=None):
    """

    :param element: xml-элемент
    :param dict xpaths: словарь xpath-выражений для извлечения атрибутов
    :param str feature_type: тип создаваемой Feature
    :param dict namespaces: словарь namespaces
    :param check_object_subtype: функция проверки типа геометрии объекта
    :return:
    :rtype: Feature
    """
    # Заполнение атрибутивной информации
    try:
        feature = node2attributes(element, xpaths, feature_type, namespaces)  # type: Feature
    except Exception as e:
        logger.error(str(e))
        logger.error('Ошибка в разборе атрибутивной информации')
        feature = None
    # Получение вида земельного участка для определения вида геометрии
    feature_subtype = None
    if check_object_subtype:
        feature_subtype = check_object_subtype(feature, element)
    if feature_subtype is None:
        logger.error('Не удалось определить подтип объекта недвижимости')
        yield feature
        del feature
        return

    # Получение xpath-выражения для извлечения геометрии и контекста запроса геометрии по виду участка
    geometry_xpaths = xpaths['geometry'].get(feature_subtype, None)
    if geometry_xpaths is None:
        logger.error('Не удалось определить дополнительные атрибуты и геометрию по подтипу объекта недвижимости: {}'
                     .format(feature_subtype))
        yield feature
        del feature
        return

    geometry_xpath = geometry_xpaths['geometry']
    geometry_type = geometry_xpaths['geometry_type']
    additional_xpath = geometry_xpaths.get('xpaths', None)

    # У объекта недвижимости нет геометрии
    contours = element.xpath(geometry_xpath, namespaces=namespaces)
    if len(contours) == 0:
        yield feature
        del feature
        return

    for contour in contours:
        feature_new = deepcopy(feature)
        if additional_xpath:
            feature_new = node2attributes(contour, additional_xpath, feature_type, namespaces, feature_new)

        geometrys = node2coord(contour, geometry_type, namespaces=namespaces).wkt()
        if len(geometrys) == 0:
            yield feature_new
            del feature_new
        else:
            for geometry in geometrys:
                feature_new.geometry = geometry
                yield feature_new
    del feature

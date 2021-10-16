# coding: utf-8
import datetime
import logging

from collections import namedtuple

from rrd_xsd_dict.xds import XSDDict
from rrd_xml_parser.parsers.names import ADDRESS_NAMES, ADDRESS_CODE

logger = logging.getLogger(__name__)

AttributeDict = namedtuple('attribute', 'dict, xpath')

AttributeModel = namedtuple('model', 'model, base, xpath')


class FeatureDescriptor:
    """
    Дескриптор для свойств моделей объектов недвижимости
    """
    __counter = 0

    def __init__(self):
        """
        Конструктор дескриптора свойства
        """
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.field_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, instance_class):
        """Получение значения атрибута из объекта"""
        if instance is None:
            return self
        else:
            return getattr(instance, self.field_name, None)

    def __set__(self, instance, value):
        """
        Установка значения атрибута

        :param self: экземпляр дескриптора
        :param instance: управляемых экземплряр в который нужно записать значение
        :param value: значение которое нужно записать
        """
        if isinstance(value, str):
            value = value.strip()
        setattr(instance, self.field_name, value)


class DateFeatureDescriptor(FeatureDescriptor):
    """
    Дескриптор для описания свойства модели типа Date
    """

    def __set__(self, instance, value):
        if not value:
            super(DateFeatureDescriptor, self).__set__(instance, value)
            return

        index = value.rfind(':')
        if index == -1:
            super(DateFeatureDescriptor, self).__set__(instance, value)
            return

        reg_date = value[:index] + value[index + 1:]
        try:
            value = datetime.datetime.strptime(reg_date, '%Y-%m-%dT%H:%M:%S%z')
        except ValueError:
            logger.warning('Неопознанный формат даты. {}'.format(value))
        else:
            value = value.strftime('%Y-%m-%d')
        super(DateFeatureDescriptor, self).__set__(instance, value)


class DictionaryFeatureDescriptor(FeatureDescriptor):
    """Дескриптор для получения текстового значения из словаря"""
    __dicts = dict()

    def __init__(self, dict_name):
        super(DictionaryFeatureDescriptor, self).__init__()
        self.dict_name = dict_name

    @classmethod
    def get_dict(cls, dict_name):
        """
        Загрузка словаря из файла
        
        :param str dict_name: имя словаря
        :return объект словаря
        :rtype XSDDict
        """
        if dict_name not in cls.__dicts:
            cls.__dicts[dict_name] = XSDDict(dict_name)
        return cls.__dicts[dict_name]

    def __set__(self, instance, value_code):
        xsd_dict = self.get_dict(self.dict_name)  # type: XSDDict
        value_text = xsd_dict.code2value(value_code)
        super(DictionaryFeatureDescriptor, self).__set__(instance, value_text)


class FeatureMeta(type):
    """Metaclass для моделей"""

    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)  # <1>
        for key, attr in attr_dict.items():  # <2>
            if isinstance(attr, FeatureDescriptor):
                type_name = type(attr).__name__
                attr.field_name = '_{}#{}'.format(type_name, key)


class FeatureBase(metaclass=FeatureMeta):
    """Базовый класс для моделей"""
    pass


class Feature(FeatureBase):
    """
    Модель представления объекта недвижимости
    """
    # тип объекта недвижимости
    type = FeatureDescriptor()

    # дата постановки на учёт
    registration_date = DateFeatureDescriptor()

    # номер объекта недвижимости (кадастровый, номер зоны и др.)
    registration_number = FeatureDescriptor()

    # описание местоположения объекта
    address = FeatureDescriptor()

    # описаниее местоположения в границах
    elaboration = FeatureDescriptor()

    # геометрия объекта
    geometry = FeatureDescriptor()

    # код проекции
    srid = FeatureDescriptor()

    def __str__(self):
        return '{0.type} {0.registration_number} {0.registration_date} {0.address} {0.geometry}'.format(self)


class Elaboration(FeatureBase):
    """Уточнение местоположения и адрес (описание местоположения) земельного участка"""
    referance_mark = FeatureDescriptor()
    distance = FeatureDescriptor()
    direction = FeatureDescriptor()
    in_bounds = FeatureDescriptor()

    value_referance_mark = ' Ориентир {}.'
    value_distance = ' Участок находится примерно в {}'
    value_direction = ' по направлению на {}.'
    value_bounds = {
        '1': 'установлено относительно ориентира, расположенного в границах участка.{}{}{}'
             ' Почтовый адрес ориентира: ',
        '0': 'установлено относительно ориентира, расположенного за пределами участка.{}{}{}'
             ' Почтовый адрес ориентира:'
    }

    def __str__(self):
        _bounds = self.value_bounds.get(self.in_bounds, '')
        text_referance = self.value_referance_mark.format(self.referance_mark) if self.referance_mark else ''
        text_distance = self.value_distance.format(self.distance) if self.distance else ''
        text_direction = self.value_direction.format(self.direction) if self.direction else ''
        if _bounds:
            _bounds = _bounds.format(text_referance, text_distance, text_direction)
        return _bounds


class Address(FeatureBase):
    # код ОКАТО
    okato = FeatureDescriptor()
    # код КЛАДР
    kladr = FeatureDescriptor()
    # код ОКТМО
    oktmo = FeatureDescriptor()
    # почтовый индекс
    postal_code = FeatureDescriptor()
    # регион
    region = DictionaryFeatureDescriptor('dRegionsRF_v01.xsd')
    # район
    district = FeatureDescriptor()
    # мун. обр
    city = FeatureDescriptor()
    # городской район
    urbandistrict = FeatureDescriptor()
    # сельсовет
    sovietvillage = FeatureDescriptor()
    # населенный пункт
    locality = FeatureDescriptor()
    # улица
    street = FeatureDescriptor()
    # дом
    level1 = FeatureDescriptor()
    # корпус
    level2 = FeatureDescriptor()
    # строение
    level3 = FeatureDescriptor()
    # квартира
    apartment = FeatureDescriptor()
    # иное
    other = FeatureDescriptor()
    # неформализованное описание
    note = FeatureDescriptor()
    # собранный адрес. Бывает в новых выписках
    readable_address = FeatureDescriptor()

    def address_code(self):
        return ', '.join(
            [getattr(self, name) for name in ADDRESS_CODE if getattr(self, name, None)]).strip()

    def __str__(self):
        if self.readable_address and self.readable_address.strip('-'):
            return self.readable_address.strip('-')
        elif self.note and self.note.strip('-'):
            return self.note.strip('-')
        else:
            collocation_location = ', '.join([getattr(self, name) for name in ADDRESS_NAMES if getattr(self, name, None)])
            return collocation_location

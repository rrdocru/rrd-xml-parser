from rrd_xml_sniffer.sniffer import Sniffer
from rrd_xml_parser.parsers import setting_pars
from rrd_xml_parser.exceptions import NotImplementedTypeError, NotImplementedValueError


class ParserXML:
    """
    Класс получателя данных
    """
    def __init__(self, levels=None):
        if levels:
            self.levels = levels
        else:
            self.levels = None

    def parse(self, xml, **kwargs):
        """
        Парсинг xml-файла. Тип парсера определяется по типу xml-документа и его namespace

        :param str xml: полный путь к xml-документу
        :param kwargs: дополнительные именованные аргументы
        :keyword type_xml: тип xml-документа (KPT, KPZU, KVZU, KPOKS, KVOKS, MP, TP)
        :keyword version_xml: версия xml-документа (namespace или version=05, 06, и др.)
        :keyword includes: возвращаемых объектов недвижимости при разборе
        :keyword excludes: список пропускаемых элементов при разборе (координаты, адреса и др.)

        :return: разобранный объект
        :raises NotImplementedTypeException: неподдерживаемый тип документа
        :raises NotImplementedValueException: неподдерживаемая версия документа

        """
        # Определение типа и кода xml-документа
        snf = Sniffer(xml)
        _type_xml = kwargs.pop('type_xml', None) or snf.get_type()
        _version_xml = kwargs.pop('version_xml', None) or snf.get_version()

        # Получени типа парсера и парсинг документа во внутреннюю структуру
        if _type_xml not in setting_pars.keys():
            raise NotImplementedTypeError(
                "Неподдерживаемый тип документа {}. Версия {}".format(_type_xml, _version_xml)
            )
        dict_codes = setting_pars[_type_xml]['versions']

        if _version_xml not in dict_codes.keys():
            raise NotImplementedValueError(
                "Неподдерживаемая версия документа {}. Версия {}".format(_type_xml, _version_xml)
            )
        getter_parser = dict_codes[_version_xml]
        _parser = getter_parser(xml)

        if self.levels and _type_xml == 'mp':
            _parser.LEVELS = self.levels

        try:
            for feature in _parser.get_features(**kwargs):
                yield feature
        except Exception as e:
            print(e)
        finally:
            del _parser

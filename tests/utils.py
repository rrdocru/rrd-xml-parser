# -*- coding: utf-8 -*-
"""
Модуль с дополнительными утилитами для тестов
"""
import logging
from json import loads, JSONDecodeError
from os import remove
from os.path import extsep, splitext
from ftplib import FTP
from typing import Iterator
from tempfile import mktemp
from shapely.wkt import loads as wkt_loads
from rrd_utils.utils import rrd_file_iterator
from rrd_xml_parser.parser import ParserXML

logger = logging.getLogger(__name__)

DEFAULT_SAMPLE_DIR = 'rrd-data-sample'

DEFAULT_PARSE_DIR = 'rrd-data-parse'


def ftp_file_iterarot(ftpobj: FTP, dirname: str) -> Iterator[str]:
    """
    Навигация по каталогу на FTP-сервере
    :param FTP ftpobj: инстанс класса FTP
    :param str dirname: имя директории
    :return: генератор по именам файлов
    :rtype: Generator[str]
    """
    data = ftpobj.mlsd(dirname)
    for name, params in data:
        if params['type'] == 'dir':
            yield from ftp_file_iterarot(ftpobj, '/'.join((dirname, name)))
        elif params['type'] == 'file':
            yield '/'.join((dirname, name))
        else:
            continue


def ftp_get_file(ftpobj: FTP, dirname: str, filename: str) -> str:
    """
    Поиск файла на FTP-сервере по имени

    :param FTP ftpobj: инстанс класса FTP
    :param str dirname: полный путь к директории в которой следует искать
    :param str filename: имя директории
    :return: полный путь к файлу
    :rtype: str
    """
    data = ftpobj.mlsd(dirname)
    list_dir = list(data)
    return '/'.join([dirname, filename]) if filename in [key[0] for key in list_dir] else None


def ftp_compare_files(ftp_connection: FTP, identifier: str, includes: list = None, excludes: list = None) -> None:
    """
    Фунция сравнения наборов тестовых и контрольных данных

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных
    :param str identifier: идентификатор из таблицы поддерживаемыъх документов РР
    :param list includes: список обрабатываемых типов объектов землеустройства
    :param list excludes: список исключенных из обработки типов объектов землеустройства
    """
    parser = ParserXML()
    path_to_tests = '/'.join((DEFAULT_SAMPLE_DIR, identifier))
    for ftp_file_test in ftp_file_iterarot(ftp_connection, path_to_tests):
        split_ftp_file_test = splitext(ftp_file_test)[0].split('/')
        path_to_control = '/'.join(
            [DEFAULT_PARSE_DIR, ] +
            split_ftp_file_test[1: -1])
        ftp_file_control = ftp_get_file(ftp_connection, path_to_control, extsep.join((split_ftp_file_test[-1], 'json')))

        assert ftp_file_control is not None, ('Не найден файл с проверяемым набором данных',
                                              'Проверяемый файл: {}'.format(ftp_file_test),
                                              )
        # Сохранение найденных файлов
        temp_file_test = mktemp(prefix='rrd_')
        temp_file_control = mktemp(prefix='rrd_')

        with open(temp_file_test, mode='w+b', buffering=0) as ftest:
            ftp_connection.retrbinary('RETR ' + ftp_file_test, ftest.write)
        with open(temp_file_control, mode='w+b', buffering=0) as fcontrol:
            ftp_connection.retrbinary('RETR ' + ftp_file_control, fcontrol.write)
        try:
            for xml in rrd_file_iterator(ftest.name):
                compare_two_file(parser, xml, temp_file_control, includes=includes, excludes=excludes)
                break
        finally:
            remove(temp_file_test)
            remove(temp_file_control)


def compare_two_file(parser: ParserXML, test_file: str, control_file: str,
                     includes: list = None, excludes: list = None) -> None:
    """
    Сравнение двух файлов

    :param AnalyzerXML parser: экземпляр класса ParserXML
    :param str test_file: путь к файлу проверяемых данных
    :param str control_file: путь к файлу контрольных данных
    :param list includes: список обрабатываемых типов объектов землеустройства
    :param list excludes: список исключенных из обработки типов объектов землеустройства
    :return:
    """

    def _get_next_control_data():
        with open(control_file, mode='r', encoding='utf-8') as f:
            for line in f:
                try:
                    data = loads(line)
                except JSONDecodeError:
                    assert False, ('Ошибка разбора контрольных данных',
                                   'Контрольные данные: {}'.format(line))
                if includes and data['type'] not in includes:
                    continue

                if excludes and data['type'] in excludes:
                    continue
                yield data

        data_test_generator = parser.parse(test_file, includes=includes, excludes=excludes)
        data_control_generator = _get_next_control_data()
        for i, feature_data_test in enumerate(data_test_generator):
            feature_data_control = next(data_control_generator)
            compare_data(
                test_data={
                    key: getattr(feature_data_test, key, None)
                    for key in dir(feature_data_test)
                    if not key.startswith('_') and not callable(getattr(feature_data_test, key))
                },
                control_data=feature_data_control
            )


def compare_data(test_data: dict, control_data: dict) -> None:
    """
    Функция сравнения двух наборов данных представленных в виде словаря
    :param dict test_data: набор проверяемых данных
    :param dict control_data: набор контрольных данных
    """
    # Проверка на одинаковое количества имён в наборах данных
    for key in test_data.keys():
        control_value = control_data.get(key, None)
        if key == 'address':
            test_value = {k: getattr(test_data[key], k, None) for k in dir(test_data[key]) if
                          not k.startswith('_') and not callable(getattr(test_data[key], k))} if test_data[
                key] else None
        elif key == 'geometry':
            test_value = wkt_loads(test_data[key]) if test_data[key] else None
            control_value = wkt_loads(control_value) if control_value else None
        else:
            test_value = test_data.get(key, None)
        compare_value(key, test_data['registration_number'], test_value, control_value)


def compare_value(key, reg_number, test_value, control_value) -> None:
    if isinstance(test_value, dict):
        for k, v in test_value.items():
            compare_value(k, reg_number, v, control_value.get(k, None))
    else:
        assert test_value == control_value, ('Различные значения ключа "{}"'.format(key),
                                             'Объект: {}'.format(reg_number),
                                             'Проверяемые данные: {}'.format(test_value),
                                             'Контрольные данные: {}'.format(control_value)
                                             )

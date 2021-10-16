from ftplib import FTP
from tests.utils import ftp_compare_files


# 1 ЗУ
def test_kpt_10_parcel(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 участки

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/1 участки', includes=['Parcel', ])


# 2 Здания
def test_kpt_10_building(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 здания

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/2 здания', includes=['Building', ])


# 3 Сооружения
def test_kpt_10_construction(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 сооружения

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/3 сооружения', includes=['Construction', ])


# 4 Объекты незавершенного строительства
def test_kpt_10_uncompleted(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 объекты незавершенного строительства

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/4 объекты незавершенного строительства', includes=['Uncompleted', ])


# 5 ОМС
def test_kpt_10_oms(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 квартал

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/5 омс', includes=['OMSPoint', ])


# 6 Квартал
def test_kpt_10_spatialdata(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 квартал

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/6 квартал', includes=['SpatialData', ])


# 7 Границы
def test_kpt_10_bound(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 границ

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/7 границы', includes=['Bound', ])


# 8 Зоны
def test_kpt_10_zone(ftp_connection: FTP) -> None:
    """
    Тест для KPT 10 зон

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_10/8 зоны', includes=['Zone', ])

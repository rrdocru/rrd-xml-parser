from ftplib import FTP
from tests.utils import ftp_compare_files


# 1 ЗУ
def test_kpt_11_land_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/1 участки', includes=['land_record', ])


# 2 Здания
def test_kpt_11_building_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/2 здания', includes=['building_record', ])


# 3 Сооружения
def test_kpt_11_construction_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/3 сооружения', includes=['construction_record', ])


# 4 Объекты незавершенного строительства
def test_kpt_11_object_under_construction_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/4 объекты незавершенного строительства', includes=['object_under_construction_record', ])


# 5 Квартал
def test_kpt_11_spatial_data(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/5 квартал', includes=['spatial_data', ])


# 6 Границы между субъектами РФ
def test_kpt_11_subject_boundary_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/6 границы между субъектами РФ', includes=['subject_boundary_record', ])


# 7 Границы муниципальных образований
def test_kpt_11_municipal_boundary_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/7 границы муниципальных образований', includes=['municipal_boundary_record', ])


# 8 Границы населённый пунктов
def test_kpt_11_inhabited_locality_boundary_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/8 границы населённый пунктов', includes=['inhabited_locality_boundary_record', ])


# 9 Границы береговых линий
def test_kpt_11_coastline_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/9 границы береговых линий', includes=['coastline_record', ])


# 10 Границы зон
def test_kpt_11_zones_and_territories_record(ftp_connection: FTP) -> None:
    """
    Тест для EAPL_01_XPaths

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kpt_11/10 границы зон', includes=['zones_and_territories_record', ])

from ftplib import FTP
from tests.utils import ftp_compare_files


# 2
def test_kvbound_municipal(ftp_connection: FTP) -> None:
    """
    Тест для Границы муниципальных образований

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kvbound_01/02 Границы муниципальных образований', includes=['KVBound', 'MunicipalBoundary', ])

#3
def test_kvbound_inhabited(ftp_connection: FTP) -> None:
    """
    Тест для Границы населенных пунктов

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kvbound_01/03 Границы населенных пунктов', includes=['KVBound', 'InhabitedLocalityBoundary', ])

from ftplib import FTP
from tests.utils import ftp_compare_files


# 2
def test_eab_municipal(ftp_connection: FTP) -> None:
    """
    Тест для Границы муниципальных образований

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'eab_01/02 Границы муниципальных образований', includes=['extract_about_boundary', 'municipal_boundary', ])

#3
def test_eab_inhabited(ftp_connection: FTP) -> None:
    """
    Тест для Границы населенных пунктов

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'eab_01/03 Границы населенных пунктов', includes=['extract_about_boundary', 'inhabited_locality_boundary', ])
from ftplib import FTP
from tests.utils import ftp_compare_files


def test_eaz(ftp_connection: FTP) -> None:
    """
    Тест для Зона (extract_about_zone)

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'eaz_01', includes=['extract_about_zone', ])

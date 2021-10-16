from ftplib import FTP
from tests.utils import ftp_compare_files


def test_schemaparcels_01(ftp_connection: FTP) -> None:
    """
    Тест для SchemaParcels 01

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, 'schemaparcels_01')

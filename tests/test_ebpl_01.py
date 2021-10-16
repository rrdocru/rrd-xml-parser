from ftplib import FTP
from tests.utils import ftp_compare_files


def test_ebpl_01(ftp_connection: FTP) -> None:
    """
    Тест для EBPL_01

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, 'ebpl_01')

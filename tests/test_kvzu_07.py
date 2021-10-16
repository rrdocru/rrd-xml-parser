from ftplib import FTP
from tests.utils import ftp_compare_files


def test_kvzu_07(ftp_connection: FTP) -> None:
    """
    Тест для KVZU_07

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, 'kvzu_07')

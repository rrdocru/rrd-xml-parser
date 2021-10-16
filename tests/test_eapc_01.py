from ftplib import FTP
from tests.utils import ftp_compare_files


def test_eapc_01(ftp_connection: FTP) -> None:
    """
    Тест для EAPC_01

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, 'eapc_01', includes=['extract_about_property_construction', ])
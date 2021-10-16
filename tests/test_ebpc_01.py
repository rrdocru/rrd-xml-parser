from ftplib import FTP
from tests.utils import ftp_compare_files


def test_ebpc_01(ftp_connection: FTP) -> None:
    """
    Тест для EBPC_01

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, 'ebpc_01/1 линейные', includes=['extract_base_params_construction', ])

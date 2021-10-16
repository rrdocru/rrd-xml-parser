from ftplib import FTP
from tests.utils import ftp_compare_files


# 1
def test_kvzone_special(ftp_connection: FTP) -> None:
    """
    Тест для Зоны с особыми условиями использования

    :param FTP ftp_connection: экземпляр класса FTP для получения тестовых данных

    :return:
    """
    ftp_compare_files(ftp_connection, r'kvzone_01/01 Зона с особыми условиями спользования', includes=['KVZone', ])

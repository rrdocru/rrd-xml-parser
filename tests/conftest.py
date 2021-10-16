import pytest
from ftplib import FTP
from os import environ as env
from six.moves.urllib.parse import urlparse, ParseResult
from typing import Iterator


@pytest.fixture(scope='session')
def ftp_connection(base_url: str) -> Iterator[FTP]:
    """
    Загружает файл по ftp

    :param str base_url: адрес подключения к FTP-серверу
    :return: экземпляр подключения к FTP-серверу
    :rtype: Iterator[FTP]
    """
    parse = urlparse(base_url)  # type: ParseResult
    ftp = FTP()
    ftp.encoding = 'utf-8'
    ftp.connect(host=parse.hostname or '127.0.0.1', port=parse.port or 21)
    ftp.login(user=env.get('FTP_USER', None), passwd=env.get('FTP_PASS', None))
    # `with` используется для того, чтобы после того как управление вернулось в фикстуру подключение закрылось
    with ftp as _f:
        yield ftp

# coding: utf-8
import logging

from rrd_xml_parser.exceptions import NotImplementedTypeError, NotImplementedValueError
from rrd_xml_parser.parser import ParserXML
from rrd_xml_parser.parsers.names import ATTRIBUTES

logger = logging.getLogger(__name__)


def createParser():
    """
    Объявление параметров командной строки

    :return: объект с определенными параметрами
    :rtype: argparse.ArgumentParser
    """
    import argparse
    parser = argparse.ArgumentParser()

    parser.add_argument('-i', '--input',
                        help='Шаблон пути для поиска файлов',
                        type=str,
                        required=True
                        )
    parser.add_argument('-o', '--output',
                        help='Файл для вывода данных',
                        type=argparse.FileType(mode='w', encoding='utf-8'),
                        default='-'
                        )
    parser.add_argument('-f', '--format',
                        help='Формат выгружаемых данных',
                        type=str,
                        default='csv',
                        choices=['csv', 'json']
                        )
    parser.add_argument('-s', '--split',
                        help='Разделять результат по отедельным файлам',
                        action='store_true'
                        )
    parser.add_argument('--replace',
                        help='Имена директорий которые нужно заменить при выгрузке',
                        type=str,
                        nargs='*')
    parser.add_argument('--includes',
                        help='Включаемые типы объектов',
                        type=str,
                        nargs='*')
    parser.add_argument('--excludes',
                        help='Включаемые типы объектов',
                        type=str,
                        nargs='*')
    return parser


def parse(xml, **kwargs):
    parser = ParserXML()
    try:
        yield from parser.parse(xml, **kwargs)
    except (NotImplementedTypeError, NotImplementedValueError) as e:
        logger.error(str(e))
    finally:
        del parser


def main():
    import csv
    import json
    import os
    from rrd_utils.classes import ITT
    from rrd_utils.utils import rrd_file_iterator_with_origin_name

    csv.register_dialect('itt', ITT)

    logging.basicConfig(level=logging.DEBUG)
    parser = createParser()
    args = parser.parse_args()

    logger.info('Начало обработки документов')
    for filename, filename_origin in rrd_file_iterator_with_origin_name(args.input):
        logger.debug(filename_origin)
        if args.split:
            filename_output = os.path.extsep.join([os.path.splitext(filename_origin)[0], args.format])
            if args.replace and len(args.replace) == 2:
                filename_output = filename_output.replace(args.replace[0], args.replace[1])
            os.makedirs(os.path.dirname(filename_output), exist_ok=True)
            fileobj_output = open(filename_output, mode='w', encoding='utf-8')
        else:
            fileobj_output = args.output

        if args.format == 'csv':
            writer = csv.DictWriter(fileobj_output, dialect='itt', fieldnames=ATTRIBUTES)
            writer.writeheader()

            for feature in parse(filename, includes=args.includes, excludes=args.excludes):
                try:
                    writer.writerow({key: getattr(feature, key) for key in ATTRIBUTES if getattr(feature, key, None)})
                except Exception as e:
                    logger.exception(e)

        else:
            for feature in parse(filename, includes=args.includes, excludes=args.excludes):
                try:
                    json.dump(feature, fileobj_output, ensure_ascii=False,
                              default=lambda x: {key: getattr(x, key, None)
                                                 for key in dir(x)
                                                 if not key.startswith('_') and not callable(getattr(x, key))})
                    fileobj_output.write('\n')
                except Exception as e:
                    logger.exception(e)

    logger.info('Завершение обработки документов')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()

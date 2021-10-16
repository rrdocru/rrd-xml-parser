# rrd-xml-parser

## Описание
Утилита предназначена для преобразования содержимого xml-документа во внутреннюю структуру RRDoc

## Использование
Утилита rrd-xml-parser содержит модуль `parser` реализующий класс ParserXML.
В нём реализована функция преобразования содержимого xml-документов получаемых из Росреестра во внутреннюю структуру 
RRDoc. 

```python
from rrd_xml_parser.parser import ParserXML
parser = ParserXML()
for feature in parser.parse('<полный путь к xml-документу>', type_xml='<тип документа>', version_xml='<версия xml-документа>'):
    print(feature)
```

## Локализация
```cmd
pygettext.py rrd_xml_parser\locale\ru_RU\rrd_xml_parser.po
```

## Распространение
1. Увеличиваем версию пакаета в файла **rrd_xml_parser/\_\_init\_\_.py**
2. Собираем новую версию пакета
    ```cmd
    python setup.py sdist bdist_wheel
    ```
    В директории **dist** появятся новые версии пакетов *.tar.gz и *.whl
3. Отправляем новые версии пакетов в PyPI
    ```cmd
    twine upload --repository-url=https://pypi.it-thematic.ru -u <имя пользователя> -p <пароль>
    ```

## Поддерживаемые типы и версии документов
* Кадастровая выписка о земельном участке (**тип**: версия):
    * **KVZU**: urn://x-artefacts-rosreestr-ru/outgoing/kvzu/7.0.1

* Кадастровый план территории: 
    * **KPT**: urn://x-artefacts-rosreestr-ru/outgoing/kpt/10.0.1
    * **extract_cadastral_plan_territory**: extract_cadastral_plan_territory 

* Выписка из ЕГРН об объекте недвижимости:
    * **extract_about_property_land**: extract_about_property_land

* Выписка из ЕГРН об основных характеристиках и зарегистрированных правах на объект недвижимости:
    * **extract_base_params_land**: extract_base_params_land

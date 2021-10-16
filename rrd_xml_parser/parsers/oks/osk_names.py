# -*- coding=utf-8
from rrd_xml_parser.models import Address, AttributeDict, AttributeModel
from rrd_xml_parser.parsers.names import ADDRESS

KVOKS_03_GroupList = [
    # Здание
    'Building',
    # Сооружение
    'Construction',
    # Объект незавершенного строительства
    'Uncompleted'
]

KPOKS_04_GroupList = [
    # Здание
    'Building',
    # Сооружение
    'Construction',
    # Объект незавершенного строительства
    'Uncompleted',
    # Поммещение
    'Flat'
]

KVOKS_03_REALTY_XPATHS = dict(
    registration_number='./@CadastralNumber',
    registration_date='./@DateCreated',
    address=AttributeModel(
        model=Address,
        base='./a:Address',
        xpath=ADDRESS
    ),
    assignation='./a:AssignationBuilding/text() | ./a:AssignationName/text() | ./a:Assignation/flat:AssignationCode/text()',
    subtype_code='./a:ObjectType/text()',
    # Дополнительные атрибуты
    area='./a:Area/text()',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 2))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial/spa:SpatialElement',
            geometry_type='entityspatialoskout'
        )
    }

)
"""Описание веток X-Path для получения атрибутивной информации об объектах недвижимости"""

KVOKS_03_XPath_SubBuilding = './a:SubBuildings/a:SubBuilding'
"""X-Path для поиска частей здания"""
KVOKS_03_XPath_SubConstruction = './a:SubBuildings/a:SubBuilding'
"""X-Path для поиска частей сооружения"""
KVOKS_03_XPath_SubFlat = './a:SubFlats/a:SubFlat'
"""X-Path для поиска частей помещения"""

KVOKS03_PART_XPATHS = dict(
    registration_number='concat(./../../@CadastralNumber, "/", ./@NumberRecord)',
    srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 2))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialoskout'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о частях объектов недвижимости"""

# -*- coding: utf-8 -*-
from rrd_xml_parser.models import AttributeDict, AttributeModel
from rrd_xml_parser.models import Address, Elaboration
from rrd_xml_parser.parsers.names import ADDRESS, ELABORATION

KPZU06_GroupList = [
    # Земельный участок
    'Parcel',
]

KVZU07_GroupList = [
    # Земельный участок
    'Parcel',
    # Временные земельные участки

]

KVZU_07_names = dict(
    # Кадастровый или иной номер
    registration_number='./@CadastralNumber',
    # Дата постановки на учёт
    registration_date='./@DateCreated',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./a:Location/a:Address',
        xpath=ADDRESS
    ),
    # Местоположение относительно ориентира
    elaboration=AttributeModel(
        model=Elaboration,
        base='./a:Location/a:Elaboration',
        xpath=ELABORATION
    ),
    # # Дополнительные атрибуты
    # Вид земельного участка
    subtype=AttributeDict('dParcels_v01.xsd', './a:Name'),
    # Код справочника вида земельного участка
    subtype_code='./a:Name',
    # Ранее присвоенные номера
    old_cadastralnumbers='./a:OldNumbers/num:OldNumber/@Number',
    # Земельные участки из которых образован земельный участок
    prev_cadastralnumbers='./a:PrevCadastralNumbers/a:CadastralNumber',
    # Объекты недвижимости расположенные в пределах данного участка
    inner_cadastralnumbers='./a:InnerCadastralNumbers/a:CadastralNumber',
    # Площадь
    area='./a:Area/a:Area',
    # Категория.Текст
    category=AttributeDict('dCategories_v01.xsd', './a:Category'),
    # Категория.Код
    category_code='./a:Category',
    # Использование.Текст
    utilization=AttributeDict('dUtilizations_v01.xsd', './a:Utilization/@Utilization'),
    # Использование.Код
    utilization_code='./a:Utilization/@Utilization',
    # Использование.По документу
    utilization_bydoc='./a:Utilization/@ByDoc',
    # Использование.Новое.Текст Минэкономразвития от 01.09.2014 № 540
    utilization_landuse=AttributeDict('dAllowedUse_v02.xsd', './a:Utilization/@LandUse'),
    # Использование.Новое.Код Минэкономразвития от 01.09.2014 № 540
    utilization_landuse_code='./a:Utilization/@LandUse',
    # Кадастровая стоимость
    cost='./a:CadastralCost/@Value',
    # Номера смежных участков
    neighbour_cadastralnumbers='./a:ParcelNeighbours/a:ParcelNeighbour/@CadastralNumber',
    # Номера образованных участков
    offspring_cadastralnumbers='./a:AllOffspringParcel/a:CadastralNumber',
    # Особые отметки
    notes='./a:SpecialNote',
    # Код системы координат. Дополнительное полу
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 2))',
    # Геометрия объекта
    # Ключ - наименование участка. Элемент Parcel - Name/text()
    geometry={
        # Землепользование
        1: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout',
            xpaths=dict(),
        ),
        # Единое землепользование
        2: dict(
            geometry='./a:CompositionEZ/a:EntryParcel',
            geometry_type='entityspatialzuout_ez',
            xpaths=dict(
                registration_number='concat(./../../@CadastralNumber, "(", ./@CadastralNumber ,")")',
                area='./a:Area/a:Area/text()'
            )
        ),
        # Обособленный участок
        3: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        ),
        # Условный участок
        4: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        ),
        # Многоконтурный участок
        5: dict(
            geometry='./a:Contours/a:Contour/a:EntitySpatial',
            geometry_type='entityspatialzuout',
            xpaths=dict(
                registration_number='concat(./../../../@CadastralNumber, "(", ./../@NumberRecord ,")")',
                area='./../a:Area/a:Area/text()'
            )
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о земельном участке"""

KVZU_XPath_SubParcel = './a:SubParcels/a:SubParcel'
"""X-Path для поиска частей"""

KVZU_07_part_names = dict(
    registration_number='concat(./../../@CadastralNumber, "/", ./@NumberRecord)',
    area='./a:Area/a:Area/text()',
    srid='concat("77", substring(../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 2))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о частях земельного участка"""

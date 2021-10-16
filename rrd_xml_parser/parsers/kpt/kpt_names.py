# -*- coding: utf-8 -*-
from rrd_xml_parser.models import AttributeModel, Address, AttributeDict
from rrd_xml_parser.parsers.names import ADDRESS

KPT10_GroupList = (
    # Сведения о земельных участках
    'Parcel',
    # Сведения о зданиях
    'Building',
    # Сведения о сооружениях
    'Construction',
    # Сведения об объектах незавершенного строительства
    'Uncompleted',
    # Сведения о пунктах ОМС
    'OMSPoint',
    # Местоположение квартала
    'SpatialData',
    # Границы между субъектами РФ, границы населенных пунктов, муниципальных образований разположенных в квартале
    'Bound',
    # Зоны
    'Zone'
)

KPT10_PARCEL_XPATHS = dict(
    # Кадастровый или иной номер
    registration_number='./@CadastralNumber',
    # Дата постановки на учёт
    registration_data='./@DateCreated',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./a:Location/a:Address',
        xpath=ADDRESS
    ),
    subtype=AttributeDict('dParcels_v01.xsd', './a:Name'),
    subtype_code='./a:Name',
    # # # Дополнительные атрибуты
    area='./a:Area/a:Area/text()',
    category=AttributeDict('dCategories_v01.xsd', './a:Category'),
    category_code='./a:Category/text()',
    utilization=AttributeDict('dUtilizations_v01.xsd', './a:Utilization/@Utilization'),
    utilization_code='./a:Utilization/@Utilization',
    utilization_bydoc='./a:Utilization/@ByDoc',
    utilization_landuse=AttributeDict('dAllowedUse_v02.xsd', './a:Utilization/@LandUse'),
    utilization_landuse_code='./a:Utilization/@LandUse',
    cost='./a:CadastralCost/@Value',
    parent_cadastralnumbers='./a:ParentCadastralNumbers/a:CadastralNumber/text()',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    geometry={
        # Землепользование
        1: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout',
        ),
        # Единое землепользование
        2: dict(
            geometry='./a:Contours/a:Contour',
            geometry_type='entityspatialzuout',
        ),
        # Обособленный участок
        3: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout',
        ),
        # Условный участок
        4: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout',
        ),
        # Многоконтурный участок
        5: dict(
            geometry='./a:Contours/a:Contour',
            geometry_type='entityspatialzuout_ez',
            xpaths=dict(
                registration_number='concat(./../../@CadastralNumber, "(", ./@NumberRecord, ")")'
            )
        )
    }

)
"""Описание веток X-Path для получения атрибутивной информации о земельном участке"""

KPT10_OBJECTSREALTY_XPATHS = dict(
    registration_number='./@CadastralNumber',
    address=AttributeModel(
        model=Address,
        base='./a:Address',
        xpath=ADDRESS
    ),
    subtype_code='./a:ObjectType/text()',
    cost='./a:CadastralCost/@Value',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial/spa:SpatialElement',
            geometry_type='entityspatialoskout',
            xpaths=dict(
                level='./@Underground'
            )
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации об объектах капитального строительства"""

KPT10_SPATIALDATA_XPATHS = dict(
    registration_number='./../@CadastralNumber',
    srid='concat("77", substring(./../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о границе квартала"""

KPT10_BOUND_XPATHS = dict(
    registration_number='./a:AccountNumber',
    description='./a:Description',
    srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    geometry={
        False: dict(
            geometry='.//a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о границах"""

KPT10_ZONE_XPATHS = dict(
    registration_number='./a:AccountNumber',
    description='./a:Description',
    srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о зонах"""

KPT10_OMS_XPATHS = dict(
    registration_number='concat(./a:PKlass, " ", ./a:PName, " ", ./a:PNmb)',
    p_nmb='./a:PNmb',
    p_name='./a:PName',
    p_klass='./a:PKlass',
    srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(./a:OrdY/text(), 1, 1))',
    geometry={
        False: dict(
            geometry='.',
            geometry_type='entityspatialoms'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о точках ОМС"""

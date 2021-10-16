# coding: utf-8
from rrd_xml_parser.models import AttributeDict, AttributeModel, Address
from rrd_xml_parser.parsers.names import ADDRESS_NEW

EAPL_GroupList = [
    'land_record',
]

EAPC_GroupList = [
    'construction_record'
]

EAPR_GroupList = [
    'room_record'
]

# Все элементы X-Path расчитываются от элемента land_record
EAPL_01_XPATHS = dict(
    # Кадастровый или иной номер
    registration_number='./object/common_data/cad_number/text()',
    # Дата постановки на учёт
    registration_date='./record_info/registration_date/text()',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./address_location/address',
        xpath=ADDRESS_NEW
    ),
    # # Дополнительные атрибуты
    # Вид земельного участка
    subtype='./object/subtype/value/text()',
    # Код справочника вида земельного участка
    subtype_code='./object/subtype/code/text()',
    # Ранее присвоенные номера
    old_cadastralnumbers='.//old_number/number/text()',
    # Земельные участки из которых образован земельный участок
    prev_cadastralnumbers='.//ascendant_cad_number/cad_number/text()',
    # Объекты недвижимости расположенные в пределах данного участка
    inner_cadastralnumbers='.//included_object/cad_number/text()',
    # Кадастровый номер предприятия как имущественного комплекса, в состав которого входит земельных участок
    facility_cad_number='.//facility_cad_number/cad_number/text()',
    # Площадь
    area='./params/area/value/text()',
    # Категория.Текст
    category=AttributeDict('dCategories_v01.xsd', './params/category/type/value/text()'),
    # Категория.Код
    category_code='./params/category/type/code/text()',
    # Использование.Текст
    utilization=AttributeDict('dUtilizations_v01.xsd', './/permitted_use_established/land_use/code/text()'),
    # Использование.Код
    utilization_code='.//permitted_use_established/land_use/code/text()',
    # Использование.По документу
    utilization_bydoc='.//permitted_use_established/by_document/text()',
    # Использование.Новое.Текст Минэкономразвития от 01.09.2014 № 540
    utilization_landuse=AttributeDict('dAllowedUse_v02.xsd', './/permitted_use_established/land_use_mer/code/text()'),
    # Использование.Новое.Код Минэкономразвития от 01.09.2014 № 540
    utilization_landuse_code='.//permitted_use_established/land_use_mer/code/text()',
    # Кадастровая стоимость
    cost='./cost/value/text()',
    # Номера смежных участков: отсутствуют
    # neighbour_cadastralnumbers=None
    # Земельные участки образонанные из данного участка
    offspring_cadastralnumbers='.//descendant_cad_number/cad_number/text()',
    # Особые отметки
    notes='./special_notes/text()',
    # Номер единого землепользования: отсутствует
    # parent_cadastralnumbers=None
    # Номера входящих в единое землепользование
    entry_cadastralnumbers='.//included_cad_number/cad_number/text()',
    # Код системы координат
    srid='concat("77", substring(./object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    # Геометрия объекта
    # Ключ вид объекта: землпепользование, единое, обособленный, условный, многоконтурный, иное
    geometry={
        # Землепользование
        1: dict(
            geometry='./contours_location/contours/contour',
            geometry_type='entityspatialzu'
        ),
        # Единое землепользование
        2: dict(
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour',
            xpath=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./number_pp/text() | ./cad_number/text(), ")")',
                area='./area/value/text()'
            )
        ),
        # Обособленный участок
        3: dict(
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Условный участок
        4: dict(
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Многоконтурный участок
        5: dict(
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour',
            xpath=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./cad_number/text() | ./number_pp/text(), ")")',
                area='./area/value/text()',
            )
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о земельном участке"""

EAPL_01_XPATH_PART = './object_parts/object_part'
"""X-Path для поиска частей"""

# Все элементы X-Path для частей расчитываются от элемента *object_part*
EAPL_01_PART_XPATHS = dict(
    # порядковый номер части
    registration_number='concat(./../../object/common_data/cad_number/text(), "/", ./part_number/text())',
    # Площадь
    area='./area/value/text()',
    # Примечания
    notes='./footnote/text()',
    # Код системы координат
    srid='concat("77", substring(./../../object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text() , 1, 2))',
    # Геометрия объекта
    # Часть многоконтурная (True, False)
    geometry={
        True: dict(
            geometry_type='entityspatialzu',
            geometry='./contours/contour',
            xpath=dict(
                registration_number='concat(./../../../../object/common_data/cad_number/text(), "/", ./../../part_number/text(), "(", ./number_pp/text(), ")")',
            )
        ),
        False: dict(
            geometry_type='entityspatialzu',
            geometry='./contours/contour',
        )
    }
)
"""X-Path для частей участка"""

# Сооружения
EAPC_01_XPATHS = dict(
    # Кадастровый номер
    registration_number='./object/common_data/cad_number/text()',
    # Дата постановки на учёт
    registration_date='./record_info/registration_date/text()',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./address_location/address',
        xpath=ADDRESS_NEW
    ),
    # геометрия объекта в формате WKT
    geometry={
        False: dict(
            geometry_type='entityspatialoks',
            geometry='./contours/contour/entity_spatial/spatials_elements/spatial_element',
            xpaths=dict(
                registration_number='concat(./../../../../../object/common_data/cad_number/text(), "(", ./number_pp/text(), ")")',
                level_code='./level_contour/code/text()',
                level='./level_contour/value/text()'
            )
        )
    },
    # код системы координат
    srid='concat("77", substring(./object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    # вид сооружения
    subtype='./object/subtype/value/text()',
    # вид сооружения(код)
    subtype_code='./object/subtype/code/text()',
    # ранее присвоенные номера
    old_cadastralnumbers='.//old_number/number/text()',
    # номера окс из которых образован
    prev_cadastralnumbers='.//ascendant_cad_number/cad_number/text()',
    # номера ЗУ в пределах сооружения
    inner_cadastralnumbers='.//land_cad_number/cad_number/text()',
    # номера предприятия ИК в который входи окс
    facility_cadastralnumber='.//facility_cad_number/cad_number/text()',
    # площадь
    area='./params/base_parameters/base_parameter/area/text()',
    # площадь застройки
    built_up_area='./params/base_parameters/base_parameter/built_up_area/text()',
    # протяженность
    extension='./params/base_parameters/base_parameter/extension/text()',
    # глубина
    depth='./params/base_parameters/base_parameter/depth/text()',
    # глубина залегания
    occurence_depth='./params/base_parameters/base_parameter/occurence_depth/text()',
    # объем
    volume='./params/base_parameters/base_parameter/volume/text()',
    # высота
    height='./params/base_parameters/base_parameter/height/text()',
    # категория
    category='./params/purpose/text()',
    # наименование сооружения
    description='./params/name/text()',
    # разрешенное использование
    utilization='./params//permitted_use/name/text()',
    # Год завершения строительства
    year_built='./params/year_built/text()',
    # Год ввода в эксплуатацию
    year_commisioning='./params/year_commisioning/text()',
    # Кадастровая стоимость
    cost='./cost/value/text()',
    # Особые отметки
    notes='./special_notes/text()'
)

# Все элементы X-Path для частей расчитываются от элемента *object_part*
EAPC_01_PART_XPATHS = dict(
    # кадастровый номер
    registration_number='concat(./../../object/common_data/cad_number/text(), "/", ./part_number/text())',
    # геометрия объекта в формате WKT
    geometry={
        False: dict(
            geometry_type='entityspatialoks',
            geometry='./contours/contour/entity_spatial/spatials_elements/spatial_element',
            xpaths=dict(
                registration_number='concat(./../../../../../object/common_data/cad_number/text(), "(", ./number_pp/text(), ")")',
                level_code='./level_contour/code/text()',
                level='./level_contour/value/text()'
            )
        )
    },
    # код системы координат
    srid='concat("77", substring(./../../object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    ## Дополнительные реквизиты
    # площадь
    area='./base_parameters/base_parameter/area/text()',
    # площадь застройки
    built_up_area='./base_parameters/base_parameter/built_up_area/text()',
    # протяженность
    extension='./base_parameters/base_parameter/extension/text()',
    # глубина
    depth='./base_parameters/base_parameter/depth/text()',
    # глубина залегания
    occurence_depth='./base_parameters/base_parameter/occurence_depth/text()',
    # объем
    volume='./base_parameters/base_parameter/volume/text()',
    # высота
    height='./base_parameters/base_parameter/height/text()',
    # особые отметки
    notes='./footnote/text()'
)

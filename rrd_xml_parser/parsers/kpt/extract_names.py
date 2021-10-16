# coding: utf-8
from rrd_xml_parser.models import AttributeModel, Address
from rrd_xml_parser.parsers.names import ADDRESS_NEW
from copy import deepcopy

KPT11_GroupList = [
    'land_record',
    'build_record',
    'construction_record',
    'object_under_construction_record',
    'spatial_data',
    'subject_boundary_record',
    'municipal_boundary_record',
    'inhabited_locality_boundary_record',
    'coastline_record',
    'zones_and_territories_record',
    'surveying_project_record',
    'oms_point'
]

# Земельные участки
KPT11_land_record_names = dict(
    # Дата постановки на учёт. Отсутствует
    # registration_date='./record_info/registration_date/text()',
    # Кадастровый или иной номер
    registration_number='./object/common_data/cad_number/text()',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./address_location/address',
        xpath=ADDRESS_NEW
    ),
    # # # Дополнительные атрибуты
    # Вид земельного участка
    subtype='./object/subtype/value/text()',
    # Код справочника вида земельного участка
    subtype_code='./object/subtype/code/text()',
    # ранее присвоенные номера. Отсутствуют
    # old_cadastralnumbers='.//old_number/number/text()',
    # Земельные участки из которых образован земельный участок
    # prev_cadastralnumbers='.//ascendant_cad_number/cad_number/text()',
    # Объекты недвижимости расположенные в пределах данного участка
    # inner_cadastralnumbers='.//included_object/cad_number/text()',
    # Кадастровый номер предприятия как имущественного комплекса, в состав которого входит земельных участок
    # facility_cad_number='.//facility_cad_number/cad_number/text()',
    # Площадь
    area='./params/area/value/text()',
    # Категория.Текст
    category='./params/category/type/value/text()',
    # Категория.Код
    category_code='./params/category/type/code/text()',
    # Использование.Текст
    utilization='.//permitted_use_established/land_use/value/text()',
    # Использование.Код
    utilization_code='.//permitted_use_established/land_use/code/text()',
    # Использование.По документу
    utilization_bydoc='.//permitted_use_established/by_document/text()',
    # Использование.Новое.Текст Минэкономразвития от 01.09.2014 № 540
    utilization_landuse='.//permitted_use_established/land_use_mer/value/text()',
    # Использование.Новое.Код Минэкономразвития от 01.09.2014 № 540
    utilization_landuse_code='.//permitted_use_established/land_use_mer/code/text()',
    # Кадастровая стоимость
    cost='./cost/value/text()',
    # Номера смежных участков. Отсутствуют
    # neighbour_cadastralnumbers=None
    # Земельные участки образонанные из данного участка
    # offspring_cadastralnumbers='.//descendant_cad_number/cad_number/text()',
    # Особые отметки. Отсутствуют
    # notes='./special_notes/text()',
    # Номер единого землепользовани
    parent_cadastralnumbers='.//common_land_cad_number/cad_number/text()',
    # Номера входящих в единое землепользование. Отсутствуют
    # entry_cadastralnumbers='.//included_cad_number/cad_number/text()',
    # Код системы координат
    srid='concat("77", substring(./object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    # Геометрия объекта
    # Ключ вид объекта: землпепользование, единое, обособленный, условный, многоконтурный, иное
    geometry={
        # Землепользование
        1: dict(
            xpaths=dict(),
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Единое землепользование
        2: dict(
            xpaths=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./cad_number/text() | ./number_pp/text(), ")")',
            ),
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Обособленный участок
        3: dict(
            xpaths=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./cad_number/text() | ./number_pp/text(), ")")',
            ),
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Условный участок
        4: dict(
            xpaths=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./cad_number/text() | ./number_pp/text(), ")")',
            ),
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        ),
        # Многоконтурный участок
        5: dict(
            xpaths=dict(
                registration_number='concat(./../../../object/common_data/cad_number/text(), "(", ./number_pp/text() | ./cad_number/text(), ")")',
            ),
            geometry_type='entityspatialzu',
            geometry='./contours_location/contours/contour'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о земельном участке"""

# Здания
KPT11_building_names = dict(
    # Дата постановки на учёт. Отсутствует
    # registration_date='./record_info/registration_date/text()',
    # Кадастровый или иной номер
    registration_number='./object/common_data/cad_number/text()',
    # Адрес
    address=AttributeModel(
        model=Address,
        base='./address_location/address',
        xpath=ADDRESS_NEW
    ),
    # # # Дополнительные атрибуты
    # Вид земельного участка
    subtype='./object/subtype/value/text()',
    # Код справочника вида земельного участка
    subtype_code='./object/subtype/code/text()',
    # ранее присвоенные номера. Отсутствуют
    # old_cadastralnumbers='.//old_number/number/text()',
    # Земельные участки из которых образован земельный участок
    # prev_cadastralnumbers='.//ascendant_cad_number/cad_number/text()',
    # Объекты недвижимости расположенные в пределах данного участка
    # inner_cadastralnumbers='.//included_object/cad_number/text()',
    # Кадастровый номер предприятия как имущественного комплекса, в состав которого входит земельных участок
    # facility_cad_number='.//facility_cad_number/cad_number/text()',
    # Площадь
    area='./params/area/text()',
    # Категория.Текст. В данном случае НАЗНАЧЕНИЕ
    category='./params/purpose/value/text()',
    # Категория.Код. В данном случае НАЗНАЧЕНИЕ
    category_code='./params/purpose/code/text()',
    # Использование.Текст
    utilization='.//permitted_uses/permitted_use/name/text()',
    # Использование.Код. Отсутствуют
    # utilization_code='.//permitted_use_established/land_use/code/text()',
    # Использование.По документу. Отсутствуют
    # utilization_bydoc='.//permitted_use_established/by_document/text()',
    # Использование.Новое.Текст Минэкономразвития от 01.09.2014 № 540. Отсутствуют
    # utilization_landuse='.//permitted_use_established/land_use_mer/value/text()',
    # Использование.Новое.Код Минэкономразвития от 01.09.2014 № 540. Отсутствуют
    # utilization_landuse_code='.//permitted_use_established/land_use_mer/code/text()',
    # Кадастровая стоимость
    cost='./cost/value/text()',
    # Номера смежных участков. Отсутствуют
    # neighbour_cadastralnumbers=None
    # Земельные участки образонанные из данного участка
    # offspring_cadastralnumbers='.//descendant_cad_number/cad_number/text()',
    # Особые отметки. Отсутствуют
    # notes='./special_notes/text()',
    # Номер единого землепользования. В данном случае единого нежвижимого комплекса
    parent_cadastralnumbers='.//united_cad_number/cad_number/text()',
    # Номера входящих в единое землепользование. Отсутствуют
    # entry_cadastralnumbers='.//included_cad_number/cad_number/text()',
    # Код системы координат
    srid='concat("77", substring(./object/common_data/cad_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    # Геометрия объекта
    # Ключ: bool от количества контуров
    geometry={
        False: dict(
            xpaths=dict(
                registration_number='concat(./../../../../../object/common_data/cad_number/text(), "(", ./../../../number_pp/text(), ")")',
                level_code='./level_contour/code/text()',
                level='./level_contour/value/text()'
            ),
            geometry_type='entityspatialoks',
            geometry='./contours/contour/entity_spatial/spatials_elements/spatial_element'
        ),
    }
)
"""Описание веток X-Path для получения атрибутивной информации о здании"""

# Сооружения
KPT11_construction_names = deepcopy(KPT11_building_names)
KPT11_construction_names['area'] = './params/base_parameters/base_parameter/area/text()'
KPT11_construction_names['built_up_area'] = './params/base_parameters/base_parameter/built_up_area/text()'
KPT11_construction_names['built_up_area'] = './params/base_parameters/base_parameter/built_up_area/text()'
KPT11_construction_names['extension'] = './params/base_parameters/base_parameter/extension/text()'
KPT11_construction_names['depth'] = './params/base_parameters/base_parameter/depth/text()'
KPT11_construction_names['occurence_depth'] = './params/base_parameters/base_parameter/occurence_depth/text()'
KPT11_construction_names['volume'] = './params/base_parameters/base_parameter/volume/text()'
KPT11_construction_names['height'] = './params/base_parameters/base_parameter/height/text()'
KPT11_construction_names['category'] = './params/purpose/text()'
"""Описание веток X-Path для получения атрибутивной информации о сооружении"""

# объекты незавершенного строительства
KPT11_under_construction_names = deepcopy(KPT11_construction_names)
"""Описание веток X-Path для получения атрибутивной информации об объекте незавершенного строительства"""

# граница квартала
KPT11_spatial_data_names = dict(
    registration_number='./../cadastral_number/text()',
    srid='concat("77", substring(./../cadastral_number/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    geometry={
        False: dict(
            xpaths=dict(),
            geometry_type='entityspatialzu',
            geometry='../spatial_data'
        ),
        True: dict(
            geometry_type='entityspatialzu',
            geometry='../spatial_data'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о границе квартала"""

# Сведения о границе между субъектами РФ
KPT11_subject_boundaries_names = dict(
    # Реестровый номер границы
    registration_number='.//b_object//reg_numb_border/text()',
    # Дата постановки на учёт
    registration_date='./record_info/registration_date/text()',
    # Вид объекта границы
    subtype='.//b_object/type_boundary/value/text()',
    # Код справочника вида земельного участка
    subtype_code='.//b_object/type_boundary/code/text()',
    # Смежные субъекты РФ
    neighbour_cadastralnumbers='.//name_neighbour_region/value/text()',
    # Наименование объекта землеустройства
    description='./description/text()',
    # Код системы координат
    srid='concat("77", substring(.//b_object//reg_numb_border/text(), 1, 2), "0", substring(.//y/text() | .//_y/text(), 1, 2))',
    # Геометрия
    geometry={
        False: dict(
            xpaths=dict(),
            geometry_type='entityspatialzu',
            geometry='.//contours/contour'
        ),
        True: dict(
            xpaths=dict(
                registration_number='concat(./../../../b_object_subject_boundary/b_object//reg_numb_border/text(), "(", ./number_pp/text(), ")")'
            ),
            geometry_type='entityspatialzu',
            geometry='.//contours/contour'
        )
    }
)
"""Описание веток X-Path для получения атрибутивной информации о границе между субъектами РФ"""

# Границы муниципальных образований
KPT11_municipal_boundary_record_names = deepcopy(KPT11_subject_boundaries_names)
# KPT11_municipal_boundary_record_names['address'] = './address'
del KPT11_municipal_boundary_record_names['neighbour_cadastralnumbers']

# Границы населенных пунктов
KPT11_inhabited_locality_boundary_record_names = KPT11_municipal_boundary_record_names

# Границы водных объектов
KPT11_coastline_record_names = deepcopy(KPT11_municipal_boundary_record_names)
KPT11_coastline_record_names['category'] = './/water/water_object_type/value/text()'
KPT11_coastline_record_names['category_code'] = './/water/water_object_type/code/text()'

# Границы зон
KPT11_zones_and_territories_record_names = deepcopy(KPT11_municipal_boundary_record_names)
KPT11_zones_and_territories_record_names['category'] = './/type_zone/value/text()'
KPT11_zones_and_territories_record_names['category_code'] = './/type_zone/code/text()'
KPT11_zones_and_territories_record_names['p_nmp'] = './/number/text()'
KPT11_zones_and_territories_record_names['p_name'] = './/name_by_doc/text()'
KPT11_zones_and_territories_record_names['index'] = './/index/text()'
KPT11_zones_and_territories_record_names['notes'] = './/other/text()'

# Образуемые участки проекта межевания
KPT11_surveying_project_record_names = dict(
    # Учётный номер проекта межевания территории
    registration_number='./b_object_surveying_project//survey_project_num/text()',
    # Дата постановки на учёт
    registration_date='./record_info/registration_date/text()',
    # Вид объекта реестра границ
    subtype='./b_object_surveying_project/type_boundary/value/text()',
    # Код справочника вида объекта реестра границ
    subtype_code='./b_object_surveying_project/type_boundary/code/text()',
    # Геометрия
    geometry={
        False: dict(
            geometry='./forming_parcels/forming_parcel/zu_contours_location/contours/contour',
            geometry_type='entityspatialzu',
            xpaths=dict(
                registration_number='concat(./../../../nominal_number/text(), "(", ./number_pp/text(), ")")'
            )
        )
    }
)

# Сведения о пунктах ОМС
KPT11_oms_point = dict(
    registration_number='concat(./p_klass/text(), " ", ./p_name/text(), " ", ./p_nmb/text())',
    p_nmb='./p_nmb/text()',
    p_name='./p_name/text()',
    p_klass='./p_klass/text()',
    srid='concat("77", substring(./../../cadastral_number/text(), 1, 2), "0", substring(.//ord_y/text(), 1, 2))',
    geometry={
        False: dict(
            geometry='.',
            geometry_type='entityspatialoms'
        )
    }
)

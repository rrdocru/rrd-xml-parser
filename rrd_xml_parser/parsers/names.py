# coding: utf-8
from rrd_xml_parser.utils import gettext as _

NAMES = dict(
    Parcel=_('Parcel'),
    SubParcel=_('SubParcel'),
    Building=_('Building'),
    Construction=_('Construction'),
    Uncompleted=_('Uncompleted'),
    SubBuilding=_('SubBuilding'),
    SubConstruction=_('SubConstruction'),
    OMSPoint=_('OMSPoint'),
    SpatialData=_('SpatialData'),
    Bound=_('Bound'),
    Zone=_('Zone'),
    zone_territory_coastline_surveying=_('Zone'),
    land_record=_('Parcel'),
    NewParcel=_('NewParcel'),
    object_part=_('SubParcel'),
    build_record=_('Building'),
    construction_record=_('Construction'),
    object_under_construction_record=_('Uncompleted'),
    spatial_data=_('SpatialData'),
    subject_boundary_record=_('Bound'),
    municipal_boundary_record=_('Bound'),
    boundary_record=_('Bound'),
    inhabited_locality_boundary_record=_('Bound'),
    coastline_record=_('Bound'),
    surveying_project_record=_('FormingParcel'),
    zones_and_territories_record=_('Zone'),
    forming_parcel=_('FormingParcel'),
    oms_point=_('OMSPoint'),
    Flat=_('Flat'),
    SubFlat=_('SubFlat'),
    # Дополнительные элементы для межевого плана. Не корневые элементы, а имена веток с координатами
)

ATTRIBUTES = [
    # Тип объекта недвижимости задаётся константой
    'type',
    # Кадастровый или иной нмоер
    'registration_number',
    # Дата постановки на учёт
    'registration_date',
    # Описание местоположение
    'address',
    # Уточнение местоположения
    'elaboration',
    # Геометрия объекта
    'geometry',
    # # Дополнительные атрибуты
    # Вид ЗУ
    'subtype',
    # Вид ЗУ.Код
    'subtype_code',
    # Номера из которых образован
    'old_cadastralnumbers',
    # Ранее присвоенные номера
    'prev_cadastralnumbers',
    # Номера объектов недвижимости
    'inner_cadastralnumbers',
    # Площадь
    'area',
    # Категория.Текст
    'category',
    # Категория.Код
    'category_code',
    # Использование.Текст
    'utilization',
    # Использование.Код
    'utilization_code',
    # Использование. По документу
    'utilization_bydoc',
    # Использование.Новое.Текст Минэкономразвития от 01.09.2014 № 540
    'utilization_landuse',
    # Использование.Новое.Код Минэкономразвития от 01.09.2014 № 540
    'utilization_landuse_code',
    # Кадастровая стоимость
    'cost',
    # Номера смежных участков
    'neighbour_cadastralnumbers',
    # Номера образованных из него участков
    'offspring_cadastralnumbers',
    # Особые отметки
    'notes',
    # Номер единого землепользования
    'parent_cadastralnumbers',
    # Номера входящих в единое землепользование
    'entry_cadastralnumbers',
    # Назначение
    'assignation',
    # Назначение.Код
    'assignation_code',
    # Номер
    'p_nmb',
    # Название
    'p_name',
    # Класс
    'p_klass',
    # # build_record
    # площадь застройки
    'built_up_area',
    # протяженность в метрах
    'extension',
    # глубина
    'depth',
    # глубина залегания
    'occurence_depth',
    # объем
    'volume',
    # высота
    'height',
    # # extract_cadastral_plan_territory.zones_and_territories_records
    # Индекс
    'index',
    # Наименование объекта землеустройства
    'description'
]

# для того чтобы вложенный словарь работал, описана модель, как к примеру Elaboration
#  ( название ключа (elaboration)  ==  названию модели (модель вызывает динамически )
#  ( поля модели  идентичны списку ключей  описываемого словаря  elaboration )
ELABORATION = dict(
    in_bounds='parent::*/a:inBounds/text()',
    referance_mark='./a:ReferenceMark/text()',
    distance='./a:Distance/text()',
    direction='./a:Direction/text()'
)

ADDRESS = dict(
    okato='./adrs:OKATO/text()',
    kladr='./adrs:KLADR/text()',
    oktmo='./adrs:OKTMO/text()',
    postal_code='./adrs:PostalCode/text()',
    region='./adrs:Region/text()',
    district='concat(./adrs:District/@Type, ". ", ./adrs:District/@Name)',
    city='concat(./adrs:City/@Type, ". ", ./adrs:City/@Name)',
    urbandistrict='concat(./adrs:UrbanDistrict/@Type, ". ", ./adrs:UrbanDistrict/@Name)',
    sovietvillage='concat(./adrs:SovietVillage/@Type, ". ", ./adrs:SovietVillage/@Name)',
    locality='concat(./adrs:Locality/@Type, ". ", ./adrs:Locality/@Name)',
    street='concat(./adrs:Street/@Type, ". ", ./adrs:Street/@Name)',
    level1='concat(./adrs:Level1/@Type, ". ", ./adrs:Level1/@Value)',
    level2='concat(./adrs:Level2/@Type, ". ", ./adrs:Level2/@Value)',
    level3='concat(./adrs:Level3/@Type, ". ", ./adrs:Level3/@Value)',
    apartment='concat(./adrs:Apartment/@Type, ". ", ./adrs:Apartment/@Value)',
    other='./adrs:Other/text()',
    note='./adrs:Note/text()'
)

ADDRESS_NEW = dict(
    # Код ФИАС
    fias='./address_fias/level_settlement/fias/text()',
    # ОКАТО
    okato='./address_fias/level_settlement/okato/text()',
    # Код КЛАДР
    kladr='./address_fias/level_settlement/kladr/text()',
    # ОКТМО
    oktmo='./address_fias/level_settlement/oktmo/text()',
    # Почтовый индекс
    postal_code='./address_fias/level_settlement/postal_code/text()',
    # Код региона
    region='./address_fias/level_settlement/region/code/text()',
    # Район
    district='concat(./address_fias/level_settlement/district/type_district/text(), " ", ./address_fias/level_settlement/district/name_district/text())',
    # Муниципальное образование
    city='concat(./address_fias/level_settlement/city/type_city/text(), " ", ./address_fias/level_settlement/city/name_city/text())',
    # Городской район
    urbandistrict='concat(./address_fias/level_settlement/urban_district/type_urban_district/text(), " ", ./address_fias/level_settlement/ubban_district/name_urban_district/text())',
    # Сельсовет
    sovietvillage='concat(./address_fias/level_settlement/soviet_village/type_soviet_village/text(), " ", ./address_fias/level_settlement/soviet_village/name_soviet_village/text())',
    # Населённый пункт
    locality='concat(./address_fias/level_settlement/locality/type_locality/text(), " ", ./address_fias/level_settlement/locality/name_locality/text())',
    # Улица
    street='concat(./address_fias/detailed_level/street/type_street/text(), " ", ./address_fias/detailed_level/street/name_street/text())',
    # noqa
    # Дом
    level1='concat(./address_fias/detailed_level/level1/type_level1/text(), " ", ./address_fias/detailed_level/level1/name_level1/text())',
    # noqa
    # Корпус
    level2='concat(./address_fias/detailed_level/level2/type_level2/text(), " ", ./address_fias/detailed_level/level2/name_level2/text())',
    # noqa
    # Строение
    level3='concat(./address_fias/detailed_level/level3/type_level3/text(), " ", ./address_fias/detailed_level/level3/name_level3/text())',
    # Квартира
    apartment='concat(./address_fias/detailed_level/apartment/type_apartment/text(), " ", ./address_fias/detailed_level/apartment/name_apartment/text())',
    # Иное описание местположения
    other='./address_fias/detailed_level/other/text()',  # noqa
    # Неформализованное описание
    note='./note/text()',
    # Адрес в соответствии с ФИАС (Текст)
    readable_address='./readable_address/text()'
)

ADDRESS_CODE = [
    'fias',
    'okato',
    'kladr',
    'oktmo',
    'postal_code',
]

ADDRESS_NAMES = [
    'region',
    'district',
    'city',
    'urbandistrict',
    'sovietvillage',
    'locality',
    'street',
    'level1',
    'level2',
    'level3',
    'apartment',
    'other',
    'note',
    'readable_address',
]

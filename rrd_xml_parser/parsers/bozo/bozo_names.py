KVBound_GroupNames = (
    # Границы между субъектами РФ, границы населенных пунктов, муниципальных образований разположенных в квартале
    'Bound'
)

KVZone_GroupNames = (
    'Zone'
)

EAB_GroupNames = (
    'boundary_record'
)

KVBound_BoundXPaths = dict(
    registration_date='./@DateCreated',
    description='.//a:SubjectsBoundary/a:NameNeighbours|.//a:MunicipalBoundary/a:Name|.//a:InhabitedLocalityBoundary/a:Name',
    geometry={
        # Землепользование
        False: dict(
            geometry='./a:Boundaries/a:Boundary/a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)

KVZone_XPaths = dict(
    registration_date='./@DateCreated',
    registration_number='./a:AccountNumber/text()',
    description='./a:Description/text()',
    subtype_code='./a:CodeZone/text()',
    subtype='./a:CodeZoneDoc/text()',
    notes='./a:SpecialNote/text()',
    geometry={
        False: dict(
            geometry='./a:EntitySpatial',
            geometry_type='entityspatialzuout'
        )
    }
)

# extract_about_boundaries xpaths
EAB_XPaths = dict(
    # кадастровый или иной номер (учётный, зоны и т.п.)
    registration_number='.//reg_numb_border/text()',
    # дата постановки на учёт
    registration_date='.//record_info/registration_date/text()',
    # геометрия объекта
    geometry={
        False: dict(
            geometry='.//contours_location/contours/contour',
            geometry_type='entityspatialzu'
        )
    },
    # вид границы
    subtype='.//type_boundary/value/text()',
    # вид границы(код)
    subtype_code='.//type_boundary/code/text()',
    # особые отметки
    notes='.//special_notes//value/text()'
)

EAZ_XPATHS = dict(
    # кадастровый или иной номер (учётный, зоны и т.п.)
    registration_number='.//reg_numb_border/text()',
    # дата постановки на учёт
    registration_date='.//record_info/registration_date/text()',
    # геометрия объекта
    geometry={
        False: dict(
            geometry='.//contours/contour',
            geometry_type='entityspatialzu'
        )
    },
    # вид границы
    subtype='.//type_boundary/value/text()',
    # вид границы(код)
    subtype_code='.//type_boundary/code/text()',
    # особые отметки
    notes='.//special_notes//value/text()'
)

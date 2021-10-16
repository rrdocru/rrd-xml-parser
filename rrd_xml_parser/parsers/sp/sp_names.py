SP_GroupNames = (
    'NewParcel'
)

SP_XPATHS = dict(
    # Кадастровый номер
    registration_number='./@Definition',
    # геометрия объекта в формате WKT
    geometry={
        # Многоконтурный
        True: dict(
            geometry='.//Entity_Spatial',
            geometry_type='entityspatialzuout',
            xpaths=dict(
                registration_number='concat(./../../@Definition, "(", ./@Definition, ")")'
            )
        ),
        # Одноконтурный
        False: dict(
            geometry='.//Entity_Spatial',
            geometry_type='entityspatialzuout'
        )
    },
    # код системы координат
    srid='concat("77", substring(./CadastralBlock/text(), 1, 2), "0", substring(.//@Y, 1, 2))',
    # номера зу из которых образован
    prev_cadastralnumbers='./Prev_CadastralNumbers/CadastralNumber/text()',
    # Площадь
    area='./Area/Area/text()',
    # Категория (код)
    category_code='./Category/@Category',
    # Разрешенное использование (по документу)
    utilization_bydoc='./Utilization/@ByDoc',
    # Особые отметки
    notes='./Note/text()'
)

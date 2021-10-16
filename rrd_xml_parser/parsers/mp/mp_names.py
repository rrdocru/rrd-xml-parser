MP06_GroupList = [
    'NewParcel',
    'ChangeParcel',
    'SpecifyRelatedParcel',
    'ExistParcel',
    'ExistEZParcels',
    'NewSubParcel',
    'ExistSubParcel',
]

NAMES_MP = dict(
    NewParcel='NewParcel',
    NewSubParcel='NewSubParcel',
    ChangeParcel='ChangeParcel',
    SpecifyRelatedParcel='SpecifyRelatedParcel',
    ExistSubParcel='ExistSubParcel',
    InvariableSubParcel='InvariableSubParcel',
    ExistParcel='ExistParcel',
    ExistEZParcels='ExistEZParcels'

)
Geometry_check = './/EntitySpatial'
NEW_PARCEL = dict(
    registration_number='./@Definition',
    cadastral_block='./CadastralBlock/text()',
    address='./Address',
    srid='concat("77", substring(./CadastralBlock/text(), 1, 2), "0", substring(.//SpelementUnit/Ordinate/@Y, 1, 1))',
    prev_cadastralnumbers='./PrevCadastralNumbers/CadastralNumber/text()',
    inner_cadastralnumbers='./ObjectRealty/InnerCadastralNumbers/CadastralNumber/text()',
    old_cadastralnumbers='./ObjectRealty/OldNumbers/OldNumber/text()',
    area='./Area/Area/text()',
    category_code='./Category/@Category',
    utilization_code='./Utilization/@Utilization',
    utilization_bydoc='./Utilization/@ByDoc',
    utilization_landuse_code='./LandUse/@LandUse',
    notes='./Note/text()',
    neighbour_cadastralnumbers='./RelatedParcels/ParcelNeighbours/ParcelNeighbour/CadastralNumber/text()'
)
NEW_PARCEL_GEOMETRY = dict(
    names=dict(
        EntitySpatial='./EntitySpatial',
        Contours='./Contours/NewContour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat(../../../CadastralBlock/text(), ../../../@Definition, "(", ../@Definition,")")',
        area='../Area/Area/text()',
    )
)

NEW_PARCEL_SUB_PARCELS_GEOMETRY = dict(
    names=dict(
        EntitySpatial='./EntitySpatial',
        Contours='./Contours/Contour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat(./../../../../../CadastralBlock/text(), ./../../../../../@Definition, ./../../../@Definition, "(", ./../@Number, ")")',
        area='./../Area/Area/text()',
    )
)

NEW_PARCEL_SUB_PARCELS = dict(
    name='./SubParcels/NewSubParcel',
    data=dict(
        registration_number='concat(./../../CadastralBlock/text(), ./../../@Definition, ./@Definition)',
        srid='concat("77", substring(./../../CadastralBlock/text(), 1, 2),'
        ' "0", substring(./../..//SpelementUnit/Ordinate/@Y, 1, 1))'
    )
)

ADDRESS = dict(
    okato='./OKATO/text()',
    kladr='./KLADR/text()',
    oktmo='./OKTMO/text()',
    postal_code='./PostalCode/text()',
    region='./Region/text()',
    district='concat(./District/@Type, ". ", ./District/@Name)',
    city='concat(./City/@Type, ". ", ./City/@Name)',
    urbandistrict='concat(./UrbanDistrict/@Type, ". ", ./UrbanDistrict/@Name)',
    sovietvillage='concat(./SovietVillage/@Type, ". ", ./SovietVillage/@Name)',
    locality='concat(./Locality/@Type, ". ", ./Locality/@Name)',
    street='concat(./Street/@Type, ". ", ./Street/@Name)',
    level1='concat(./Level1/@Type, ". ", ./Level1/@Value)',
    level2='concat(./Level2/@Type, ". ", ./Level2/@Value)',
    level3='concat(./Level3/@Type, ". ", ./Level3/@Value)',
    apartment='concat(./Apartment/@Type, ". ", ./Apartment/@Value)',
    other='./Other/text()',
    note='./Note/text()'
)

CHANGE_PARCEL = dict(
    registration_number='./@CadastralNumber',
    inner_cadastralnumbers='./ObjectRealty/InnerCadastralNumbers/CadastralNumber/text()',
    old_cadastralnumbers='./ObjectRealty/OldNumbers/OldNumber/text()',
    notes='./Note/text()'
)
CHANGE_PARCEL_GEOMETRY_SUB = NEW_PARCEL_SUB_PARCELS_GEOMETRY.copy()
CHANGE_PARCEL_NEW_SUB = dict(
    name='./SubParcels/NewSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber), ./@Definition)',
        srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//SpelementUnit/Ordinate/@Y, 1, 1))',
        area='/Area/Area/text()'
    )
)
CHANGE_PARCEL_EXIST_SUB = dict(
    name='./SubParcels/ExistSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber), ./@NumberRecord)',
        srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//SpelementUnit/Ordinate/@Y, 1, 1))',
        area='/Area/Area/text()'
    )
)
CHANGE_PARCEL_INVARIABLE_SUB = dict(
    name='./SubParcels/InvariableSubParcel',
    data=dict(
    registration_number='concat(./../../@CadastralNumber), ./@NumberRecord)',
    area='/Area/Area/text()'
    )
)

SPECIFY_RELATED_PARCELS = dict(
    registration_number='concat(./@CadastralNumber, "(", ./@NumberRecord, ")")',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))'
)
SPECIFY_RELATED_PARCELS_GEOMETRY = dict(
    names=dict(
        EntitySpatial='./AllBorder/EntitySpatial',
        Contours='./Contours/NewContour/EntitySpatial',
        ChangeBorder='./ChangeBorder',
        DeleteAllBorder='./DeleteAllBorder'
    ),
    Contours=dict(
        registration_number='concat(./../../../../../CadastralBlock/text(), ./../../../../../@Definition, ./../../../@Definition, "(", ./../@Number, ")")',
        area='./../Area/Area/text()',
    )
)
SPECIFY_RELATED_SUB_PARCELS = dict(
    name='./ExistSubParcels/ExistSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber, ./@NumberRecord)',
        srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))'
    )
)
SPECIFY_RELATED_SUB_GEOMETRY = dict(
    names=dict(
        EntitySpatial='./EntitySpatial',
        Contours='./Contours/Contour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat(./../../../../../@CadastralNumber),./../../../@NumberRecord),"(" + ./../@Number + ")"',
    )
)

SPECIFY_PARCEL_EXIST = dict(
    registration_number='./@CadastralNumber',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    inner_cadastralnumbers='./ObjectRealty/InnerCadastralNumbers/CadastralNumber/text()',
    old_cadastralnumbers='./ObjectRealty/OldNumbers/OldNumber/text()',
    area='./Area/Area/text()',
    notes='./Note/text()',
    neighbour_cadastralnumbers='./RelatedParcels/ParcelNeighbours/ParcelNeighbour/CadastralNumber/text()',
)
SPECIFY_PARCEL_EZ = dict(
    registration_number='./@CadastralNumber',
    srid='concat("77", substring(./@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
    inner_cadastralnumbers='./ObjectRealty/InnerCadastralNumbers/CadastralNumber/text()',
    old_cadastralnumbers='./ObjectRealty/OldNumbers/OldNumber/text()',
    area='./Area/Area/text()',
    notes='./Note/text()',
    neighbour_cadastralnumbers='./RelatedParcels/ParcelNeighbours/ParcelNeighbour/CadastralNumber/text()',
)
SPECIFY_PARCEL_NEW_SUB = dict(
    name='./SubParcels/NewSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber, ./@Definition)',
        srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
        area='./Area/Area/text()'
    )
)
SPECIFY_PARCEL_EXIST_SUB = dict(
    name='./SubParcels/ExistSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber, ./@NumberRecord)',
        srid='concat("77", substring(./../../@CadastralNumber, 1, 2), "0", substring(.//@Y, 1, 1))',
        area='./Area/Area/text()'
    )
)
SPECIFY_PARCEL_INVARIABLE_SUB = dict(
    name='./SubParcels/InvariableSubParcel',
    data=dict(
        registration_number='concat(./../../@CadastralNumber, ./@NumberRecord)',
        area='./Area/Area/text()'
    ),
    geometry=dict(
        name='./Contours/Contour',
        registration_number='concat(./../../../../@CadastralNumber),./../../@NumberRecord),"(" + ./@Number + ")"',
        area='./Area/Area/text()'
    )
)
SPECIFY_PARCEL_GEOMETRY = dict(
    names=dict(
        CompositionEZ='./CompositionEZ/InsertEntryParcels/InsertEntryParcel/NewEntryParcel/EntitySpatial',
        EntitySpatial='./EntitySpatial ',
        Contours='./Contours/ExistContour/EntitySpatial',
        DeleteAllBorder='./Contours/DeleteAllBorder',
        NewContours='./Contours/NewContour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat(./../../../@CadastralNumber, "(", ./../@Definition, ")")',
        area='./..//Area/Area/text()'
    ),
    NewContours=dict(
        registration_number='concat(./../../../@CadastralNumber, "(", ./../@NumberRecord, ")")',
        area='./../Area/Area/text()'
    ),
    DeleteAllBorder=dict(),
    CompositionEZ=dict(
        registration_number='concat(./../../../../../@CadastralNumber, "(", ./../@Definition, ")")',
        area='./../Area/Area/text()'
    )
)
SPECIFY_PARCEL_SUB_GEOMETRY = dict(
    names=dict(
        EntitySpatial='./EntitySpatial ',
        Contours='./Contours/Contour/EntitySpatial',
    ),
    Contours=dict(
        area='./../Area/Area/text()',
        registration_number='concat(./../../../../../@CadastralNumber, ./../../../@Definition, "(", ./../@Number, ")")'
    ),
)


PACKAGE_SUB_PARCEL_NEW = dict(
    registration_number='concat(./../CadastralNumberParcel/text(), ./@Definition)',
    srid='concat("77", substring(./../CadastralNumberParcel/text(), 1, 2), "0", substring(.//@Y, 1, 1))',
    area='./Area/Area/text()'
)
PACKAGE_SUB_PARCEL_NEW_GEOM = dict(
    names=dict(
        EntitySpatial='./EntitySpatial',
        Contours='./Contours/Contour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat("77", substring(./../../CadastralNumberParcel/text(), 1, 2), "0", substring(./..//@Y, 1, 1))',
        area='./../Area/Area/text()',
    )
)

PACKAGE_SUB_PARCEL_EXIST = dict(
    registration_number='concat(./../CadastralNumberParcel/text(), ./@NumberRecord)',
    srid='concat("77", substring(./../CadastralNumberParcel/text(), 1, 2), "0", substring(.//@Y, 1, 1))',
    area='./Area/Area/text()'
)
PACKAGE_SUB_PARCEL_EXIST_GEOM = dict(
    names=dict(
        EntitySpatial='./EntitySpatial',
        Contours='./Contours/Contour/EntitySpatial'
    ),
    Contours=dict(
        registration_number='concat("77", substring(./../../CadastralNumberParcel/text(), 1, 2), "0", substring(./..//@Y, 1, 1))',
        area='./../Area/Area/text()',
    )
)

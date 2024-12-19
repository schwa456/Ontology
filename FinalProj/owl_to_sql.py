from owlready2 import get_ontology
from models import Heritage, Session

#OWL File Path
OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'

# Get Ontology
onto = get_ontology(OWL_FILE_PATH).load()

# Creating Session
session = Session()

# Injecting Instance of Heritage Class into Data Base
for heritage in onto.Heritage.instances():
    data = {}
    for prop in heritage.get_properties():
        values = getattr(heritage, prop.name, [])
        data[prop.name] = values[0] if values else None



    name_hangul = getattr(heritage, 'hasNameHangul', [None])[0]
    name_hanja = getattr(heritage, 'hasNameHanja', [None])[0]
    city = getattr(heritage, 'hasCity', [None])[0]
    district = getattr(heritage, 'hasDistrict', [None])[0]
    mngmnt_org = getattr(heritage, 'hasManagementOrg', [None])[0]
    lon = getattr(heritage, 'hasLongitude', [None])[0]
    lat = getattr(heritage, 'hasLatitude', [None])[0]
    mngmnt_num = getattr(heritage, 'hasManagementNum', [None])[0]
    assoc_num = getattr(heritage, 'hasAssociationNum', [None])[0]
    city_num = getattr(heritage, 'hasCityNum', [None])[0]
    canceled = getattr(heritage, 'isCanceled', [None])[0]
    type = getattr(heritage, 'hasType', [None])[0]
    type1 = getattr(heritage, 'hasType1', [None])[0]
    type2 = getattr(heritage, 'hasType2', [None])[0]
    type3 = getattr(heritage, 'hasType3', [None])[0]
    type4 = getattr(heritage, 'hasType4', [None])[0]
    qty = getattr(heritage, 'hasQuantity', [None])[0]
    desig_date = getattr(heritage, 'hasDesignatedDate', [None])[0]
    address = getattr(heritage, 'hasAddress', [None])[0]
    era = getattr(heritage, 'hasEra', [None])[0]
    possessor = getattr(heritage, 'isPossessedBy', [None])[0]
    imageURL = getattr(heritage, 'hasImageURL', [None])[0]
    description = getattr(heritage, 'hasDescription', [None])[0]

    if mngmnt_num:
        new_heritage = Heritage()
        session.add(new_heritage)

session.commit()
session.close()
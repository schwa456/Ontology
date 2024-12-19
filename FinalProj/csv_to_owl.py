import pandas as pd
from owlready2 import get_ontology, Thing, DataProperty

CSV_FILE_PATH = 'eng_col_heritage_data.csv'

OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'

try:
    df = pd.read_csv(CSV_FILE_PATH, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')

onto = get_ontology("http://example.org/heritage_ontology#")

with onto:
    class Information(Thing):
        pass

    class NameHangul(Information):
        pass

    class NameHanja(Information):
        pass

    class Quantity(Information):
        pass

    class Era(Information):
        pass

    class DesignatedDate(Information):
        pass

    class ImageURL(Information):
        pass

    class Description(Information):
        pass

    class Location(Thing):
        pass

    class City(Location):
        pass

    class District(Location):
        pass

    class Longitude(Location):
        pass

    class Latitude(Location):
        pass

    class Type(Thing):
        pass

    class Type1(Type):
        pass

    class Type2(Type):
        pass

    class Type3(Type):
        pass

    class Type4(Type):
        pass

    class Management(Thing):
        pass

    class ManagementNum(Management):
        pass

    class ManagementOrg(Management):
        pass

    class AssociationNum(Management):
        pass

    class Possessor(Management):
        pass


    class Heritage(Thing):
        pass
    class hasNameHangul(Heritage >> str, DataProperty):
        pass
    class hasNameHanja(Heritage >> str, DataProperty):
        pass
    class hasCity(Heritage >> str, DataProperty):
        pass
    class hasDistrict(Heritage >> str, DataProperty):
        pass
    class hasManagementOrg(Heritage >> str, DataProperty):
        pass
    class hasLongitude(Heritage >> str, DataProperty):
        pass
    class hasLatitude(Heritage >> str, DataProperty):
        pass
    class hasManagementNum(Heritage >> int, DataProperty):
        pass
    class hasAssociationNum(Heritage >> int, DataProperty):
        pass
    class isCanceled(Heritage >> str, DataProperty):
        pass
    class hasType(Heritage >> str, DataProperty):
        pass
    class hasType1(Heritage >> str, DataProperty):
        pass
    class hasType2(Heritage >> str, DataProperty):
        pass
    class hasType3(Heritage >> str, DataProperty):
        pass
    class hasType4(Heritage >> str, DataProperty):
        pass
    class hasQuantity(Heritage >> str, DataProperty):
        pass
    class hasDesignatedDate(Heritage >> str, DataProperty):
        pass
    class hasAddress(Heritage >> str, DataProperty):
        pass
    class hasEra(Heritage >> str, DataProperty):
        pass
    class isPossessedBy(Heritage >> str, DataProperty):
        pass
    class hasImageURL(Heritage >> str, DataProperty):
        pass
    class hasDescription(Heritage >> str, DataProperty):
        pass

for _, row in df.iterrows():
    with onto:
        management_num = str(row['management_number'])
        heritage = Heritage(management_num)
        heritage.hasNameHangul.append(row['name_hangul'])
        heritage.hasNameHanja.append(row['name_hanja'])
        heritage.hasCity.append(row['city'])
        heritage.hasDistrict.append(row['district'])
        heritage.hasManagementOrg.append(row['management_organization'])
        heritage.hasLongitude.append(row['longitude'])
        heritage.hasLatitude.append(row['latitude'])
        heritage.hasManagementNum.append(row['management_number'])
        heritage.hasAssociationNum.append(row['association_number'])
        #heritage.hasCityNumber.append(row['city_number'])
        heritage.isCanceled.append(row['canceled'])
        heritage.hasType1.append(row['type1'])
        heritage.hasType2.append(row['type2'])
        heritage.hasType3.append(row['type3'])
        heritage.hasType4.append(row['type4'])

        types = [str(row[t]).strip() for t in ['type1', 'type2', 'type3', 'type4'] if row[t] != '-']
        heritage.hasType = [" ".join(types) if types else '']

        heritage.hasQuantity.append(row['quantity'])
        heritage.hasDesignatedDate.append(row['designated_date'])
        heritage.hasAddress.append(row['address'])
        heritage.hasEra.append(row['era'])
        heritage.isPossessedBy.append(row['possession'])
        heritage.hasImageURL.append(row['image_URL'])
        heritage.hasDescription.append(row['description'])

onto.save(file=OWL_FILE_PATH, format="rdfxml")

print(f"OWL 파일이 '{OWL_FILE_PATH}'에 성공적으로 저장되었습니다.")
import pandas as pd
from owlready2 import get_ontology, Thing, DataProperty
from datetime import datetime

CSV_FILE_PATH = 'merged_heritage_data.csv'

OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'

try:
    df = pd.read_csv(CSV_FILE_PATH, encoding='utf-8')
except UnicodeDecodeError:
    df = pd.read_csv(CSV_FILE_PATH, encoding='latin1')

onto = get_ontology("http://example.org/heritage_ontology#")

with onto:
    class Heritage(Thing):
        pass

    class hasName(Heritage >> str, DataProperty):
        pass
    class hasCity(Heritage >> str, DataProperty):
        pass

    class hasDistrict(Heritage >> str, DataProperty):
        pass

    class hasManagement(Heritage >> str, DataProperty):
        pass

    class hasDesignatedDate(Heritage >> str, DataProperty):
        pass
    class hasEra(Heritage >> str, DataProperty):
        pass
    class hasDescription(Heritage >> str, DataProperty):
        pass

for _, row in df.iterrows():
    with onto:
        heritage = Heritage(f"Heritage_{row['name'].replace(' ', '_')}")
        heritage.hasName = row['name']
        heritage.hasCity = row['city']
        heritage.hasDistrict = row['district']
        heritage.hasManagement = row['management']
        heritage.hasDesignatedDate = row['designateddate']
        heritage.hasEra = row['era']
        heritage.hasDescription = row['description']

onto.save(file=OWL_FILE_PATH, format="rdfxml")

print(f"OWL 파일이 '{OWL_FILE_PATH}'에 성공적으로 저장되었습니다.")
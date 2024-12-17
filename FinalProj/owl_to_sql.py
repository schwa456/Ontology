from owlready2 import get_ontology
from models import Heritage, Session
from datetime import datetime

#OWL File Path
OWL_FILE_PATH = 'heritige_ontology_final.owl'

# Get Ontology
onto = get_ontology(OWL_FILE_PATH).load()

# Creating Session
session = Session()

# Injecting Instance of Heritage Class into Data Base
for heritage in onto.Heritage.instances():
    name = heritage.hasName[0] if hasattr(heritage, 'hasName') and heritage.hasName else None
    description = heritage.hasDescription[0] if hasattr(heritage, 'hasDescription') and heritage.hasDescription else None
    date_str = heritage.hasDesignatedDate[0] if hasattr(heritage, 'hasDesignatedDate') and heritage.hasDesignatedDate else None
    designated_date = datetime.strptime(date_str, '%Y%m%d') if date_str else None
    print(name, description, designated_date)

    if name:
        new_heritage = Heritage(name=name, description=description, designated_date=designated_date)
        session.add(new_heritage)

session.commit()
session.close()
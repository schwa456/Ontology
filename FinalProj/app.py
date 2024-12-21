from flask import Flask, render_template, request, jsonify
from owlready2 import get_ontology, World, onto_path
import os

app = Flask(__name__)

OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'
world = World()
onto = get_ontology(OWL_FILE_PATH).load()

world.sparql_prefixes = {
    '': "http://example.org/heritage_ontology#"
}

default_namespace = onto.get_namespace("http://example.org/heritage_ontology#")
onto.default_namespace = default_namespace

PROPERTY_NAME_MAPPING = {
    "heritage_owl_by_schwa.hasNameHangul": "이름(한글)",
    "heritage_owl_by_schwa.hasNameHanja": "이름(한자)",
    "heritage_owl_by_schwa.hasLongitude": "경도",
    "heritage_owl_by_schwa.hasLatitude": "위도",
    "heritage_owl_by_schwa.hasManagementNum": "관리번호",
    "heritage_owl_by_schwa.hasAssociationNum": "국가유산연계번호",
    "heritage_owl_by_schwa.isCanceled": "지정해제여부",
    "heritage_owl_by_schwa.hasQuantity": "수량",
    "heritage_owl_by_schwa.hasDesignatedDate": "지정일",
    "heritage_owl_by_schwa.hasAddress": "주소",
    "heritage_owl_by_schwa.hasEra": "시대",
    "heritage_owl_by_schwa.hasImageURL": "이미지 URL",
    "heritage_owl_by_schwa.hasDescription": "내용",
    "heritage_owl_by_schwa.hasCity": "시/도",
    "heritage_owl_by_schwa.hasDistrict": "구/군",
}

@app.route('/')
def index():
    return render_template('index.html')

def parse_input_to_sparql(user_input):
    if "시대:" in user_input:
        keyword = extract_keyword(user_input)
        return f"""
        PREFIX : <http://example.org/heritage_ontology#>
        SELECT ?heritage ?era ?name
        WHERE {{
            ?heritage a :Heritage ;
                      :hasNameHangul ?name ;
                      :hasEra ?era .
            FILTER(CONTAINS(?era, "{keyword}"))
        }}
        """
    elif "이름:" in user_input:
        keyword = extract_keyword(user_input)
        return f"""
        PREFIX : <http://example.org/heritage_ontology#>
        SELECT ?property ?value
        WHERE {{
            ?heritage a :Heritage ;
                      :hasNameHangul "{keyword}" ;
                      ?property ?value .
            FILTER(isLiteral(?value))
        }}
        """

    return None

def extract_keyword(user_input):
    import re
    match = re.search(r"'(.*?)'", user_input)
    if match:
        return match.group(1)
    if "이름에" in user_input and "포함" in user_input:
        try:
            return user_input.split("이름에")[1].split("포함")[0].strip()
        except IndexError:
            return None
    if "시대가" in user_input:
        try:
            return user_input.split("시대가")[1].strip()
        except IndexError:
            return None
    return None

@app.route('/query', methods=['POST'])
def query():
    user_input = request.json.get('input', '').strip()
    is_sparql = request.json.get('is_sparql', False)

    sparql_query = user_input if is_sparql else parse_input_to_sparql(user_input)

    if sparql_query is None:
        return jsonify({'error': '조건을 검색할 수 없습니다.'})

    try:
        results = list(onto.world.sparql(sparql_query))
        print("Raw Results:", results)

        namespace = default_namespace.base_iri  # 기본 네임스페이스 추출

        cleaned_result = []
        for row in results:
            cleaned_row = {}
            for field, value in zip(sparql_query.split()[1:], row):
                value_str = str(value)

                # 값이 네임스페이스로 시작하면 URI에서 네임스페이스 제거
                if value_str.startswith("heritage_owl_by_schwa."):
                    cleaned_value = value_str.replace("heritage_owl_by_schwa.", "")
                else:
                    # 일반 텍스트는 그대로 유지
                    cleaned_value = value_str

                cleaned_row[field.replace(namespace, "")] = cleaned_value
            cleaned_result.append(cleaned_row)

        print("Cleaned Result:", cleaned_result)
        return jsonify(cleaned_result)




    except Exception as e:
        return jsonify({'error': str(e)})




if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

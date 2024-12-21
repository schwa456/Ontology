from owlready2 import get_ontology, World

# 온톨로지 로드
OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'
world = World()
onto = get_ontology(OWL_FILE_PATH).load()

world.sparql_prefixes = {
    '': "http://example.org/heritage_ontology#"
}

# 자연어를 SPARQL로 변환
def parse_input_to_sparql(user_input):
    if "이름에" in user_input and "포함" in user_input:
        keyword = extract_keyword(user_input)
        print(f"Extracted keyword: {keyword}")  # 디버깅용 출력
        return f"""
        PREFIX : <http://example.org/heritage_ontology#>
        SELECT ?heritage ?name
        WHERE {{
            ?heritage a :Heritage ;
                      :hasNameHangul ?name .
            FILTER(CONTAINS(?name, "{keyword}"))
        }}
        """
    elif "시대가" in user_input:
        keyword = extract_keyword(user_input)
        print(f"Extracted keyword: {keyword}")  # 디버깅용 출력
        return f"""
        PREFIX : <http://example.org/heritage_ontology#>
        SELECT ?heritage ?name ?era
        WHERE {{
            ?heritage a :Heritage ;
                      :hasEra "{keyword}" ;
                      :hasNameHangul ?name .
        }}
        """
    return None

def extract_keyword(user_input):
    """
    자연어 입력에서 키워드를 추출합니다.
    """
    import re

    # 작은따옴표로 감싸진 키워드 추출
    match = re.search(r"'(.*?)'", user_input)
    if match:
        return match.group(1)

    # '이름에' 다음과 '포함' 사이의 텍스트 추출
    if "이름에" in user_input and "포함" in user_input:
        try:
            return user_input.split("이름에")[1].split("포함")[0].strip()
        except IndexError:
            return None

    # '시대가' 다음의 텍스트 추출
    if "시대가" in user_input:
        try:
            return user_input.split("시대가")[1].strip()
        except IndexError:
            return None

    return None

# 테스트용 입력값
if __name__ == '__main__':
    user_input = input("Enter your query: ")  # 사용자 입력 받기
    sparql_query = parse_input_to_sparql(user_input)  # SPARQL 변환
    print(f"Generated SPARQL Query:\n{sparql_query}")  # 생성된 SPARQL 쿼리 출력

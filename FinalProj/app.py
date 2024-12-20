from flask import Flask, request, render_template, jsonify
from owlready2 import get_ontology
import sqlparse
import re
import os

app = Flask(__name__)
OWL_FILE_PATH = 'heritage_owl_by_schwa.owl'
onto = get_ontology(OWL_FILE_PATH).load()

data_properties = {prop.name.lower(): prop.name for prop in onto.data_properties()}

def sql_to_sparql(sql_query):

    # SELECT * 쿼리 처리
    if sql_query.strip().upper() == "SELECT * FROM HERITAGE;":
        return """
        PREFIX : <http://example.org/heritage_ontology#>
        SELECT ?heritage ?property ?value
        WHERE {
            ?heritage a :Heritage .
            ?heritage ?property ?value .
        }
        """

    parsed = sqlparse.parse(sql_query)[0]
    tokens = [token for token in parsed.tokens if not token.is_whitespace]

    # SELECT 절 FIELD 추출
    select_fields = []
    for idx, token in enumerate(tokens):
        if token.value.upper() == 'SELECT':
            fields = tokens[idx+1].value.split(',')
            select_fields = [field.strip().replace('.', '') for field in fields]

    # WHERE 절 조건 추출
    where_clause = ''
    for idx, token in enumerate(tokens):
        if token.value.upper() == 'WHERE':
            where_clause = tokens[idx+1].value.strip()

    sparql_fields = [data_properties.get(field, field) for field in select_fields]

    # SPARQL SELECT 절 구성
    sparql_select = ' '.join(f'?{field}' for field in sparql_fields)

    # SPARQL WHERE 절 구성
    sparql_where = ' '.join(f'?heritage :{field} ?{field} .' for field in sparql_fields)

    # WHERE 절 조건을 SPARQL FILTER로 변환
    sparql_filter = ''
    if where_clause:
        where_clause = re.sub(r"(\w+)\s*>=\s*'([\d\-]+)'", r'FILTER(?\1 >= "\2")', where_clause)
        for sql_col, sparql_prop in data_properties.items():
            where_clause = where_clause.replace(sql_col, sparql_prop)
        sparql_filter = where_clause

    # 최종 SPARQL 쿼리
    sparql_query = f"""
    PREFIX : <http://example.org/heritage_ontology#>
    SELECT {sparql_select}
    WHERE {{
        ?heritage a :Heritage .
        {sparql_where}
        {sparql_filter}
    }}
    """

    print("Generated SPARQL Query:")
    print(sparql_query)

    return sparql_query

# homepage : rendering SQL input form
@app.route('/')
def index():
    return render_template('index.html')

# endpoint which executes received SQL query and reflects on ontology
@app.route('/query', methods=['POST'])
def query():
    #sql_query = request.json['query']
    #sparql_query = sql_to_sparql(sql_query)
    sparql_query = request.json['query']

    try:
        results = list(onto.world.sparql(sparql_query))
        result_list = [{field: str(value) for field, value in zip(sparql_query.split()[1:], row)} for row in results]
        return jsonify(result_list)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

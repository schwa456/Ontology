from flask import Flask, request, render_template, jsonify
from owlready2 import get_ontology, onto_path, World
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



data_properties = {prop.name.lower(): prop.name for prop in onto.data_properties()}

# homepage : rendering SPARQL input form
@app.route('/')
def index():
    return render_template('index.html')

# endpoint which executes received SPARQL query and reflects on ontology
@app.route('/query', methods=['POST'])
def query():
    sparql_query = request.json['query']

    try:
        results = list(onto.world.sparql(sparql_query))
        cleaned_result = [
            {field: str(value).split('.')[-1] for field, value in zip(sparql_query.split()[1:], row)}
            for row in results
        ]

        return jsonify(cleaned_result)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=True)

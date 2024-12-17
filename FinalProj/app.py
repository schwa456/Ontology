from flask import Flask, render_template, request, jsonify
from models import Heritage, Session
from sqlalchemy import text

app = Flask(__name__)

# homepage : rendering SQL input form
@app.route('/')
def index():
    return render_template('index.html')

# endpoint which executes received SQL query
@app.route('/run-query', methods=['POST'])
def run_query():
    session = Session()
    try:
        query = request.json.get('query')
        result = session.execute(text(query))
        rows = [dict(row) for row in result]
        session.commit()
        return jsonify(rows)
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)})
    finally:
        session.close()

if __name__ == '__main__':
    app.run(debug=True)

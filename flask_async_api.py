from flask import Flask, request, jsonify
from tasks import add

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def submit_add_task():
    data = request.json
    task = add.delay(data['x'], data['y'])
    return jsonify({'task_id': task.id}), 202

if __name__ == '__main__':
    app.run(debug=True)

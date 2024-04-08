from flask import Flask, request, jsonify
from business_logic import perform_division
from tasks import add

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def submit_add_task():
    """
    A function to submit an addition task to the Celery worker.
    This end point is asynchronous and returns a JSON response containing the task ID.
    """
    data = request.json
    task = add.delay(data['x'], data['y'])
    return jsonify({'task_id': task.id}), 202

@app.route('/divide', methods=['POST'])
def divide():
    """
    A function to handle a POST request to divide two numbers.
    This end point is synchronous and returns a JSON response containing the result of the division operation.
    Parameters:
    - None

    Returns:
    - A JSON response containing the result of the division operation or an error message.
    """
    data = request.json
    try:
        x = data['x']
        y = data['y']
        result = perform_division(x, y)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except KeyError:
        return jsonify({'error': 'Please provide both "x" and "y" values.'}), 400
    return jsonify({'result': result}), 200

# if __name__ == '__main__':
#     app.run(debug=True)

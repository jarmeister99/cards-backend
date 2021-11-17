from flask import current_app as app
import json

foo = 1

@app.route('/api/shares/', methods=['GET'])
def get_shares():
    dummy_shares = [
        {
            'title': 'hello world!'
        },
        {
            'title': 'test post please ignore!'
        }
    ]
    response = app.response_class(
        response=json.dumps(dummy_shares),
        mimetype='application/json'
    )
    return response


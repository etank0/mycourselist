from flask import json, Response

def message(code, status, message):
    return Response( 
        response=json.dumps({
        "status": status,
        "message": message,
        }),
        status=code,
        mimetype='application/json'
    )
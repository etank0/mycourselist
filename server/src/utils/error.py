from flask import Response, json

# error function for any errors
def error(error):
    return Response( 
        response=json.dumps({
        "status": "failed",
        "message": "Error Occurred",
        "error": error
        }),
        status=500,
        mimetype='application/json'
    )
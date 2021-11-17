from flask import current_app as app

from bson import json_util

from knowledge_app.db.models.Share import Share


@app.route("/api/shares/", methods=["GET"])
def get_shares():
    """
    Return a JSON response containing all shares queried from the database
    """

    shares = Share.get_all()
    response = app.response_class(
        response=json_util.dumps(shares), mimetype="application/json", status=200
    )
    return response

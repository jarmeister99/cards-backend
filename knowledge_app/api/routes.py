from flask import current_app as app, request

from bson import json_util

from knowledge_app.db.models.Share import Share
from util.images_from_url import get_images

import time


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


@app.route("/api/shares/<share_id>", methods=["DELETE"])
def delete_share(share_id: str):
    print(f'Attempting to delete {share_id}')
    return 200


@app.route("/api/shares/", methods=["POST"])
def create_share():
    """
    Add the given share to the database and return the created share
    """
    request_body = request.get_json()

    # parse body
    share_object = {}

    # ensure we have all required fields
    for field in Share.required_fields:
        if not request_body.get(field):
            # error if missing any
            return {'error': f'request missing \'{field}\''}, 400
        # save required field to object
        share_object[field] = request_body.get(field)

    # save all optional fields to object
    for field in Share.optional_fields:
        if request_body.get(field):
            share_object[field] = request_body.get(field)
        else:
            share_object[field] = ''

    # look for image on link
    if not share_object.get('img_url'):
        img = get_images(url=share_object.get('link'), min_height=100, min_width=100)
        if img:
            share_object['img_url'] = img

    Share.insert(share_object)
    response = app.response_class(
        response=json_util.dumps(share_object), mimetype="application/json", status=200
    )
    return response

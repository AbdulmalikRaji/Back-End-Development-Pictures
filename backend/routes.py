from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    """return data"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for value in data:
        if value["id"]== id:
            return jsonify(value), 200
    return jsonify({'error': 'Picture not found'}), 404


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    
    try:
    # Extract the picture data from the incoming request
        pic = request.get_json()

        # Check if the 'id' already exists in the data
        if any(picture['id'] == pic['id'] for picture in data):
            return jsonify({"Message": f"picture with id {pic['id']} already present"}), 302

        # Append the new picture to the data
        data.append(pic)

        # Return the newly created picture with a 201 status code
        return jsonify(pic), 201
    except Exception as e:
        # Handle any errors gracefully
        return jsonify({"error": str(e)}), 500

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    # Extract data from the incoming request
    updated_picture = request.get_json()

    # Find the picture in the 'data' list by ID
    picture = next((item for item in data if item['id'] == id), None)

    # If the picture is found, update it
    if picture:
        picture.update(updated_picture)
        return jsonify(picture), 200
    else:
        # If the picture is not found, return a 404 error with a message
        return jsonify({"message": "picture not found"}), 404

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id): 
    # Find the picture in the 'data' list by ID
    pic = next((item for item in data if item['id'] == id), None)

    if pic:
        data.remove(pic)
        return '', 204 #empty body
    
    else:
        return jsonify({"message": "picture not found"}), 404

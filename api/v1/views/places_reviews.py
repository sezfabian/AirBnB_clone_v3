#!/usr/bin/python3
""" Objects that handle all default RESTful API actions for Review objects """
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>',
                 methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a specific Review object by its ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<string:review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific Review object by its ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({})


@app_views.route('/places/<string:place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    review_data = request.get_json()
    if 'user_id' not in review_data:
        abort(400, description="Missing user_id")
    if 'text' not in review_data:
        abort(400, description="Missing text")
    user_id = review_data['user_id']
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    review_data['place_id'] = place_id
    review = Review(**review_data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<string:review_id>',
                 methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a specific Review object by its ID
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    review_data = request.get_json()
    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200

#!/usr/bin/python3
''' Handles all Restful API actions for Reviews'''
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    ''' Retrives a list of all Review objects associated to a place'''
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/api/v1/reviews/<review_id>', methods=['GET'],
                 strict_slashes=False)
def get_review_obj(review_id):
    ''' Retrieves a Review object'''
    review = storage.get(Review, review_id)

    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/api/v1/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    ''' Deletes a Review object with a given id'''
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/api/v1/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    ''' Creates a review for a place'''
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, description="Not a JSON")

    if 'user_id' not in data:
        abort(400, description="Missingg user_id")

    user = storage.get(User, data.get('user_id'))

    if not user:
        abort(404)

    if 'text' not in data:
        abort(400, description="Missing text")

    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/api/v1/reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    ''' Updates a Review instance for a place'''
    review = storage.get(Review, review_id)

    if not review:
        abort(404)

    data = request.get_json()
    if not data:
        abort(404, description="Not a JSON")

    ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
        storage.save()
        return make_response(jsonify(review.to_dict()), 200)

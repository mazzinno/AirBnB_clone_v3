#!/usr/bin/python3
"""
places_reviews.py
"""
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User
from . import app_views


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Place not found")
    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """Retrieves a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Review not found")
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Review not found")
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review object"""
    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()
    user_id = data.get('user_id')
    text = data.get('text')

    if not user_id:
        return make_response("Missing user_id", 400)
    if not text:
        return make_response("Missing text", 400)

    place = storage.get(Place, place_id)
    if not place:
        abort(404, "Place not found")

    user = storage.get(User, user_id)
    if not user:
        abort(404, "User not found")

    new_review = Review(user_id=user_id, place_id=place_id, text=text)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by its ID"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404, "Review not found")

    if not request.is_json:
        return make_response("Not a JSON", 400)
    data = request.get_json()

    ignored_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200

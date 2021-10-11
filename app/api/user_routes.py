from flask import Blueprint, jsonify, request
from flask_login import login_required
from app.models import User, db, user
from app.forms.follow_form import DeleteFollow, NewFollow
from colors import *


user_routes = Blueprint('users', __name__)


@user_routes.route('/')
@login_required
def users():
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}

@user_routes.route('/following/<int:id>')
def followers(id):
    user = User.query.get(id)
    return {'user': user.to_dict()}


@user_routes.route('/following/', methods=["POST"])
def add_follow():
    form = NewFollow()
    data = form.data
    print(CGREEN + "\n DATA: \n", data, "\n\n" + CEND)

    form['csrf_token'].data = request.cookies['csrf_token']

    if form.validate_on_submit():

        user_to_follow = User.query.get(data['user_to_follow_id'])
        current_user = User.query.get(data['current_user_id'])

        current_users_following = [user for user in current_user.following]
        current_users_following.append(user_to_follow.id)

        user_to_follow_followers = [user for user in user_to_follow.followers]
        user_to_follow_followers.append(current_user.id)

        current_user.following = current_users_following
        user_to_follow.followers = user_to_follow_followers

        db.session.commit()

        return {'user': user_to_follow.to_dict()}
    else:
        return "Bad Data"

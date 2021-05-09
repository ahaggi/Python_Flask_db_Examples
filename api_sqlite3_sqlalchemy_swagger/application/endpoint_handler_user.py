from flask import (make_response, abort)
from .models import User, UserSchema, sqlalc


def read_all():
    """
    This function responds to a request for GET /api/users
    with the complete lists of user
    :return:        JSON string of list of user
    """
    users = User.query.all()
    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    print('***********************************************************')
    return user_schema.dump(users)


def read_one(id):
    """
    This function responds to a request for GET /api/users/{id}
    with JUST one matching user
    :param id:      id of the user to find
    :return:        User matching id
    """
    # Build the initial query
    user = User.query.filter(User.id == id).one_or_none()

    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data
    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for id: {id}")


#  TODO try catch unique username
def add_one(body):
    """
    This function responds to a request for POST/api/users/{id}
    and creates a new User. 
    :body:             The JSON containing the User data
    :return:           201 on success
    """
    _id = body.get("id")
    print(f' _id {_id}')
    existing_user = User.query.filter(User.id == _id).one_or_none()
#  TODO try catch unique username

    if existing_user is None:
        user_schema = UserSchema()
        new_user = user_schema.load(body, session=sqlalc.session)

        # Add the user to the database
        sqlalc.session.add(new_user)
        sqlalc.session.commit()

        # Serialize and return the newly created user in the response
        data = user_schema.dump(new_user)

        return data, 201

    # Otherwise, nope, user exists already
    else:
        abort(
            409, f"The request could not be completed due to a conflict with the current state of the target resource\nUser with {_username} exists already")


#  TODO try catch unique username
def update_one(id, body):
    """
    This function responds to a request for PUT /api/users/{id}
    This function updates an existing user 
    :param id:          id of the user to update  
    :param body:        User to update
    :return:            updated user structure
    """
    print(f'id, {id} ')
    print(f'body, {body} ')
    # Get the user requested from the db into session
    existed_user = (User.query.filter(User.id == id).one_or_none())
    print(f'existed_user, {existed_user}!')

#  TODO try catch unique username
    if existed_user is not None:
        # turn the passed in user into a db object, IMPORTANT: body.id = null
        user_schema = UserSchema()
        update = user_schema.load(body, session=sqlalc.session)

        # Set the value of update.id which was null prev.
        update.id = existed_user.id
        print(f'update, {update}!')

        # merge the new object "update" into the old "existed_user" and commit it to the db
        sqlalc.session.merge(update)
        sqlalc.session.commit()
        print(f'existed_user, {existed_user}!')

        # return updated user in the response
        data = user_schema.dump(existed_user)

        return data, 200

    else:
        abort(404, f"User not found for id: {id}")


def delete_one(id):
    """
    This function responds to a request for DELETE /api/users/{id}
    This function deletes a user  
    :param id:      id of the user to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Get the user requested
    user = User.query.filter(User.id == id).one_or_none()

    # Did we find a user?
    if user is not None:
        sqlalc.session.delete(user)
        sqlalc.session.commit()
        return make_response(f"The user {id} is deleted", 200)

    else:
        abort(404, f"User not found for id: {id}")

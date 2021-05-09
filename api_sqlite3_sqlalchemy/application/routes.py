from flask import request, render_template, make_response, jsonify, abort
from flask import current_app as app
from .models import User, UserSchema, sqlalc


@app.route('/', methods=['GET'])
def home():
    """Create a user via query string parameters."""
    users = User.query.all()
    print(users)
    return {"data": [
        {"username": u.username, "password": u.password, "notes":
         [
            {"id": n.id, "content": n.content, "createdOn": n.createdOn,
                "priority": n.priority, "categoryId": n.categoryId}
            for n in u.notes
            ]
         }
        for u in users
    ]}

# 
@app.route('/users', methods=['GET'])
def user_all():
    """
    This function responds to a request for GET /api/users
    with the complete lists of user
    :return:        JSON string of list of user
    """
    users = User.query.all()
    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
    data = user_schema.dump(users)
    print('***********************************************************')
    print(data)
    print('***********************************************************')
    return jsonify(data)



@app.route('/users/<id>', methods=['GET'])
def user_one(id):
    """
    This function responds to a request for GET /api/users/{id}
    with JUST one matching user
    :param id:      id of the user to find
    :return:        User matching id
    """
    # Build the initial query
    user = User.query.filter(User.id == 1).one_or_none()
    print(id)

    if user is not None:
        # Serialize the data for the response
        user_schema = UserSchema()
        # Serialize objects by passing them to your schema’s dump method, which returns the formatted result
        data = user_schema.dump(user)
        print('***********************************************************')
        print(data)
        print('***********************************************************')
        return jsonify(data)
    # Otherwise, nope, didn't find that user
    else:
        abort(404, f"User not found for id: {id}")

from flask import (make_response, abort)
from .models import Category, CategorySchema, sqlalc


def read_all():
    """
    This function responds to a request for GET /api/categories
    with the complete lists of category
    :return:        json string of list of category
    """
    categories = Category.query.all()
    # Serialize the data for the response
    category_schema = CategorySchema(many=True)
    print('***********************************************************')
    return category_schema.dump(categories)


def read_one(id):
    """
    This function responds to a request for GET /api/categories/{id}
    with JUST one matching category
    :param id:   id of the category to find
    :return:           Category matching id
    """
    # Build the initial query
    category = Category.query.filter(Category.id == id).one_or_none()

    if category is not None:
        # Serialize the data for the response
        category_schema = CategorySchema()
        data = category_schema.dump(category)
        return data
    # Otherwise, nope, didn't find that category
    else:
        abort(404, f"Category not found for id: {id}")

#  TODO try catch unique type


def add_one(body):
    """
    This function responds to a request for POST /api/categories
    and creates a new category. 
    :body:             The JSON containing the category data
    :return:           201 success Or 409 conflict
    """
    _id = body.get("id")

    print(f' 0000000000000000000 id, {_id} ')

    existing_category = Category.query.filter(Category.id == _id).one_or_none()

#  TODO try catch unique type

    if existing_category is None:
        category_schema = CategorySchema()
        new_category = category_schema.load(body, session=sqlalc.session)

        # Add the category to the database
        sqlalc.session.add(new_category)
        sqlalc.session.commit()

        # Serialize and return the newly created category in the response
        data = category_schema.dump(new_category)

        return data, 201

    # Otherwise, nope, category exists already
    else:
        abort(
            409, f"The request could not be completed due to a conflict with the current state of the target resource\nCategory with {_id} exists already")

#  TODO try catch unique type


def update_one(id, body):
    """
    This function responds to a request for POST /api/categories/{id}
    and updates an existing category 
    :param id:          Id of the category to update  
    :param body:        Category to update
    :return:            updated category structure
    """
    # Get the category requested from the db into session
    existed_category = Category.query.filter(Category.id == id).one_or_none()

#  TODO try catch unique type

    if existed_category is not None:
        # turn the passed in category into a db object, IMPORTANT: body.id = null
        category_schema = CategorySchema()
        update = category_schema.load(body, session=sqlalc.session)

        # Set the value of update.id which was null prev.
        update.id = existed_category.id

        # merge the new object "update" into the old "existed_category" and commit it to the db
        sqlalc.session.merge(update)
        sqlalc.session.commit()

        # return updated category in the response
        data = category_schema.dump(existed_category)
        return data, 200

    else:
        abort(404, f"Category not found for id: {id}")


def delete_one(id):
    """
    This function responds to a request for DELETE /api/categories/{id}
    This function deletes a category  
    :param id:          id of the category to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the category requested
    category = Category.query.filter(Category.id == id).one_or_none()

    if category is not None:
        sqlalc.session.delete(category)
        sqlalc.session.commit()
        return make_response(f"The category {id} is deleted", 200)

    else:
        abort(404, f"Category not found for id: {id}")

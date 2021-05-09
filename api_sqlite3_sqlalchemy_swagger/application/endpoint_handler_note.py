from flask import (make_response, abort)
from .models import User, Note, NoteSchema, sqlalc

def read_all():
    """
    This function responds to a request for GET /api/notes
    with the complete lists of Note
    :return:        json string of list of note
    """
    notes = Note.query.all()
    # Serialize the data for the response
    note_schema = NoteSchema(many=True)
    print('***********************************************************')
    return note_schema.dump(notes)


def read_one(id):
    """
    This function responds to a request for GET /api/notes/{id}
    with JUST one matching Note 
    :param id:         id of the note to find
    :return:           Note matching id
    """
    # Build the initial query
    note = Note.query.filter(Note.id == id).one_or_none()

    if note is not None:
        # Serialize the data for the response
        note_schema = NoteSchema()
        data = note_schema.dump(note)
        return data
    # Otherwise, nope, didn't find that note
    else:
        abort(404, f"Note not found for id: {id}")


def add_one(body):
    """
    This function responds to a request for POST /api/notes
    and creates a new note. 
    :body:             The JSON containing the note data
    :return:           201 success Or 409 conflict
    """
    _id = body.get("id")
    existing_note = Note.query.filter(Note.id == _id).one_or_none()

    if existing_note is None:
        note_schema = NoteSchema()
        new_note = note_schema.load(body, session=sqlalc.session)

        # Add the note to the database
        sqlalc.session.add(new_note)
        sqlalc.session.commit()

        # Serialize and return the newly created note in the response
        data = note_schema.dump(new_note)

        return data, 201

    # Otherwise, nope, note exists already
    else:
        abort(
            409, f"The request could not be completed due to a conflict with the current state of the target resource\nNote with {_id} exists already")


def update_one(id, body):
    """
    This function responds to a request for PUT /api/notes/{id}
    and updates an existing note 
    :param id:          Id of the note to update  
    :param body:        Note to update
    :return:            updated note structure
    """
    # Get the note requested from the db into session
    existed_note = Note.query.filter(Note.id == id).one_or_none()

    if existed_note is not None:
        # turn the passed in note "body" into a db object, IMPORTANT: body.id = null
        note_schema = NoteSchema()
        update = note_schema.load(body, session=sqlalc.session)

        # Set the value of update.id which was null prev
        update.id = existed_note.id

        # merge the new object "update" into the old "existed_user" and commit it to the db
        sqlalc.session.merge(update)
        sqlalc.session.commit()

        # return updated note in the response
        data = note_schema.dump(existed_note)
        return data, 200

    else:
        abort(404, f"Note not found for id: {id}")


def delete_one(id):
    """
    This function responds to a request for DELETE /api/notes/{id}
    This function deletes a note 
    :param id:          id of the note to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the note requested
    note = Note.query.filter(Note.id == id).one_or_none()

    if note is not None:
        sqlalc.session.delete(note)
        sqlalc.session.commit()
        return make_response(f"The note {id} is deleted", 200)

    else:
        abort(404, f"Note not found for id: {id}")






# """
# USECASE2:
#     Note is dependent on User i.e. if the user deleted all his notes will be cascade deleted ,, Remember to set the db schema accordingly.
# """

# def read_all():
#     """
#     This function responds to a request for GET /api/notes
#     with the complete lists of Note
#     :return:        json string of list of note
#     """
#     notes = Note.query.all()
#     # Serialize the data for the response
#     note_schema = NoteSchema(many=True)
#     print('***********************************************************')
#     return note_schema.dump(notes)


# def read_one(userId, id):
#     """
#     This function responds to a request for GET /api/users/{userId}/notes/{id}
#     with JUST one matching Note 
#     :param userId:      userId of the user who owns the note  
#     :param id:          id of the note to find
#     :return:            Note matching id
#     """
#     # Build the initial query
#     note = Note.query.filter(Note.id == id).filter(Note.userId == userId).one_or_none()

#     # Did we find a Note?
#     if note is not None:
#         # Serialize the data for the response
#         note_schema = NoteSchema()
#         data = note_schema.dump(note)
#         return data
#     # Otherwise, nope, didn't find that note
#     else:
#         abort(404, f"Note not found for id: {id}")


# def add_one(userId, body):
#     """
#     This function responds to a request for POST /api/users/{userId}/notes
#     and creates a new note. 
#     :param userId:      userId of the user who owns the note  
#     :body:              The JSON containing the note data
#     :return:            201 success Or 409 conflict
#     """
#     if (body['userId'] is not None) and (int(body['userId']) != int(userId) ) :
#         abort(404, f"sdfdsfsdf  Id: {userId}") # TODO the userId is note editable

#     user = User.query.filter(User.id == userId).one_or_none()
#     if user is None:
#         abort(404, f"User not found for Id: {userId}")

#     _id = body.get("id")
#     existing_note = Note.query.filter(Note.id == _id).one_or_none()
#     if existing_note is not None:
#         # note exists already
#         abort(409, f"The request could not be completed due to a conflict with the current state of the target resource\nNote with {_id} exists already")

#     note_schema = NoteSchema()
#     new_note = note_schema.load(body, session=sqlalc.session)

#     # Add the note to the person and database, NOTICE that Note is dependent on User i.e. if the user deleted all his notes will be cascade deleted  
#     user.notes.append(new_note)
#     sqlalc.session.commit()

#     # Serialize and return the newly created note in the response
#     data = note_schema.dump(new_note)

#     return data, 201



# def update_one(userId, id, body):
#     """
#     This function responds to a request for PUT /api/users/{userId}/notes/{id}
#     and updates an existing note 
#     :param userId:    userId of the user who owns the note  
#     :param id:          Id of the note to update  
#     :param body:        Note to update
#     :return:            updated note structure
#     """
#     if (body['userId'] is not None) and (int(body['userId']) != int(userId) ) :
#         abort(404, f"sdfdsfsdf  Id: {userId}") # TODO the userId is note editable?????,,, Even now note.userId is editable
#     """
#     to change note.userId i.e from userId=2 to userId=3 call /api/users/3/notes/{id} with new data
#     """
#     # Get the note requested from the db into session
#     update_note = Note.query.filter(Note.id == id).one_or_none()

#     if update_note is not None:
#         # turn the passed in note into a db object
#         note_schema = NoteSchema()
#         update = note_schema.load(body, session=sqlalc.session)

#         # Set the id to the note we want to update
#         update.id = update_note.id   

#         # merge the new object into the old and commit it to the db
#         sqlalc.session.merge(update)
#         sqlalc.session.commit()

#         # return updated note in the response
#         data = note_schema.dump(update_note)
#         return data, 200

#     else:
#         abort(404, f"Note not found for id: {id}")


# def delete_one(userId, id):
#     """
#     This function responds to a request for DELETE /api/users/{userId}/notes/{id}
#     This function deletes a note 
#     :param userId:      userId of the user who owns the note  
#     :param id:          id of the note to delete
#     :return:            200 on successful delete, 404 if not found
#     """
#     # Get the note requested
#     note = Note.query.filter(Note.id == id).one_or_none()

#     if note is not None:
#         sqlalc.session.delete(note)
#         sqlalc.session.commit()
#         return make_response(f"The note {id} is deleted", 200)

#     else:
#         abort(404, f"Note not found for id: {id}")

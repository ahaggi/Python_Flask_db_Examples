from . import sqlalc ,ma
import datetime
from sqlalchemy.orm import relationship, backref  
from marshmallow import fields  


class User(sqlalc.Model):
    __tablename__ = 'User'
    # __table_args__ = {'extend_existing': True}  => Specifies that a table wit hthis name already exists in the target database.  When this is set, your model will 
    #                    not override existing tables Thus, it is possible that the fields in your model might not match up with columns in your table.
    __table_args__ = {'extend_existing': True} 

    username = sqlalc.Column(
        sqlalc.String(80), 
        primary_key=True, 
        )
    password = sqlalc.Column(
        sqlalc.String(80), 
        index=False,
        unique=False, 
        nullable=False
        )
    def __repr__(self):
        return '<User usn: {arg1},  psw: {arg2} >'.format(arg1=self.username , arg2=self.password)

class Category(sqlalc.Model):
    id = sqlalc.Column(
        sqlalc.String(80), 
        primary_key=True
        )
    type = sqlalc.Column(
        sqlalc.String(80), 
        unique=True,
        nullable=False
        )
    def __repr__(self):
        return '<Category id: {arg1},  tp: {arg2} >'.format(arg1=self.id , arg2=self.type)
    # returns <Category id: 1,  tp: type1 >

class Note(sqlalc.Model):
    id = sqlalc.Column(
        sqlalc.String(80),
        primary_key=True
        )
    content = sqlalc.Column(
        sqlalc.String(80), 
        nullable=False
        )
    createdOn = sqlalc.Column( # test nullable!
        sqlalc.String(80), 
        # sqlalc.DateTime, 
        # default=datetime.datetime.utcnow
        ) 
    priority = sqlalc.Column(
        sqlalc.Integer, 
        nullable=False
        )
    username = sqlalc.Column(
        sqlalc.String(80), 
        sqlalc.ForeignKey('User.username'),    
        nullable=False # nullable??
        ) 
    user = relationship("User",backref="notes")             # <----------One to many  we will call this feild  
    categoryId = sqlalc.Column(
        sqlalc.String(80), 
        sqlalc.ForeignKey('Category.id'),    
        nullable=False # nullable??
        ) 
    def __repr__(self):
        return '<Note id: {arg1},  tp: {arg2} >'.format(arg1=self.id , arg2=self.content)

""" 
How to use  UserSchema :
    This is a serialization mechanizm using the Marshmallow package and its instance "ma" which is initiated in __init__.py file,
    Make sure to import "ma" from __init__.py by uncommenting "from . import ma"

    and UserSchema can be used as flws:
    @app.route('/', methods=['GET'])
    def user_records():
        users = User.query.all()
        user_schema = UserSchema(many=True)
        print(user_schema.dump(users))
        return jsonify(user_schema.dump(users))
"""
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Optional: deserialize to model instances
        include_relationships = True

    # username = ma.auto_field()
    # password = ma.auto_field()
    notes = fields.Nested('UserNoteSchema', default=[], many=True)
    # # notes = ma.auto_field()

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        load_instance = True
        include_relationships = True

class NoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Note
        load_instance = True
        # include_fk = True
    user = fields.Nested('NoteUserSchema',  many=False)

    # id = ma.auto_field()
    # content= ma.auto_field()
    # createdOn= ma.auto_field()
    # priority = ma.auto_field()
    # username = ma.auto_field()
    # categoryId = ma.auto_field()

class NoteUserSchema(ma.SQLAlchemyAutoSchema):
    """
    This class is just like User BUT WITHOUT the "Note relation"
    This class exists to get around a recursion issue
    """
    username = fields.Str()
    password = fields.Str()

class UserNoteSchema(ma.SQLAlchemyAutoSchema):
    """
    This class is just like Note
    This class exists  to get around a recursion issue
    """
    id = fields.Str()
    content = fields.Str()
    createdOn = fields.Str()
    priority = fields.Int()
    categoryId = fields.Str()

from server import db, ma
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy import Table, Column, Integer, ForeignKey
from datetime import datetime
from marshmallow import fields

# USER -------------------------------------------------------------------------

from werkzeug.security import generate_password_hash , check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text)
    password_hash = db.Column(db.Text)
    role = db.Column(db.Text)
    cust_id = db.Column(db.Integer)

    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash,password)

    def generate_auth_token(self, expiration = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_in = expiration)
        return s.dumps({ 'id': self.id })

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None # valid token, but expired
        except BadSignature:
            return None # invalid token
        user = User.query.get(data['id'])
        return user

class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session

class Roles(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text)
    ability = db.Column(db.Text)

# RELATIONSHIP TABLES ----------------------------------------------------------
persona_roles_rel = db.Table('persona_roles_rel',
    db.Column('persona_id',db.Integer, ForeignKey('persona.id')),
    db.Column('persona_role_id',db.Integer, ForeignKey('persona_roles.id'))
    )

pers_prod_rel = db.Table('pers_prod_rel',
    db.Column('persona_id',db.Integer, ForeignKey('persona.id')),
    db.Column('product_id',db.Integer, ForeignKey('product.id'))
    )

insight_persona_rel = db.Table('insight_persona_rel',
    db.Column('persona_id',db.Integer, ForeignKey('persona.id')),
    db.Column('insight_id',db.Integer, ForeignKey('insight.id'))
    )

insight_product_rel = db.Table('insight_product_rel',
    db.Column('product_id',db.Integer, ForeignKey('product.id')),
    db.Column('insight_id',db.Integer, ForeignKey('insight.id'))
    )

# PRODUCT ----------------------------------------------------------------------

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    metrics = db.Column(db.Text)
    goals = db.Column(db.Text)
    features = db.Column(db.Text)
    archived = db.Column(db.Boolean, default=False)
    owner = db.Column(db.Text)
    last_update  = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    create_date = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    revision = db.Column(db.Integer, default = 0)
    creator_id = db.Column(db.Integer)
    product_homepage = db.Column(db.Text)
    product_life = db.Column(db.Text)
    cust_id = db.Column(db.Integer)

class ProductSchema(ma.ModelSchema):
    personas = ma.Nested('PersonaSchema', many=True, exclude=('products','persona_picture' , 'cust_id'))

    class Meta:
        model = Product
        sqla_session = db.session

class ProductComments(db.Model):
    __tablename__ = 'product_comments'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer,ForeignKey('product.id'))
    comment_body = db.Column(db.Text)
    creator_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    action = db.Column(db.Text)
    downchange = db.Column(db.Text)
    upchange = db.Column(db.Text)
    create_date = db.Column(db.DateTime,default=datetime.utcnow)
    user = db.relationship('User')

class ProductCommentsSchema(ma.ModelSchema):
    user = ma.Nested('UserSchema', exclude=('password_hash',))

    class Meta:
        model = ProductComments
        sqla_session = db.session

class ProductFile(db.Model):
    __tablename__ = 'product_files'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, ForeignKey('product.id'))
    filename = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    filetype = db.Column(db.Text)

class ProductFileSchema(ma.ModelSchema):
    class Meta:
        model = ProductFile
        sqla_session = db.session


## PERSONAS --------------------------------------------------------------------
class PersonaRoles(db.Model):
    __tablename__ = 'persona_roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)

class PersonaRoleSchema(ma.ModelSchema):
    class Meta:
        model = PersonaRoles
        sqla_session = db.session

class PersonaComments(db.Model):
    __tablename__ = 'persona_comments'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer,ForeignKey('persona.id'))
    comment_body = db.Column(db.Text)
    creator_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    action = db.Column(db.Text)
    downchange = db.Column(db.Text)
    upchange = db.Column(db.Text)
    create_date = db.Column(db.DateTime,default=datetime.utcnow)
    user = db.relationship('User')

class PersonaCommentsSchema(ma.ModelSchema):
    user = ma.Nested('UserSchema', exclude=('password_hash',))

    class Meta:
        model = PersonaComments
        sqla_session = db.session

class PersonaFile(db.Model):
    __tablename__ = 'persona_files'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, ForeignKey('persona.id'))
    filename = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    filetype = db.Column(db.Text)

class PersonaFileSchema(ma.ModelSchema):
    class Meta:
        model = PersonaFile
        sqla_session = db.session

class Persona(db.Model):
    __tablename__ = 'persona'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    title = db.Column(db.Text)
    quote = db.Column(db.Text)
    job_function = db.Column(db.Text)
    needs = db.Column(db.Text)
    wants = db.Column(db.Text)
    pain_point = db.Column(db.Text)
    external = db.Column(db.Integer, default=0)
    market_size = db.Column(db.Integer)
    buss_val = db.Column(db.Integer)
    create_date = db.Column(db.DateTime,
                            default=datetime.utcnow)
    revision = db.Column(db.Integer, default = 0)
    creator_id = db.Column(db.Integer)
    access_group = db.Column(db.Integer)
    archived = db.Column(db.Boolean, default=False)
    persona_maturity = db.Column(db.Text)
    persona_picture = db.Column(db.Binary)
    cust_id = db.Column(db.Integer)
    roles = db.relationship('PersonaRoles' , secondary = 'persona_roles_rel' , backref=db.backref('personas')  )
    products = db.relationship('Product' , secondary = 'pers_prod_rel' ,backref=db.backref('personas')  )

    # @staticmethod
    # def check_if_avatar(self):
    #     self.avatar = db.Column(db.Boolean, default=False)
    #     if self.persona_picture == None:
    #         self.avatar = False
    #     else:
    #         self.avatar = True

class PersonaSchema(ma.ModelSchema):
    roles = ma.Nested('PersonaRoleSchema', many=True)
    products = ma.Nested('ProductSchema', many=True, exclude=('personas','cust_id',))
    avatar = fields.Function(lambda obj : obj.persona_picture != None)

    class Meta:
        model = Persona
        sqla_session = db.session

# INSIGHTS ---------------------------------------------------------------------
class Insight(db.Model):
    __tablename__ = 'insight'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    content = db.Column(db.Text)
    file = db.Column(db.Text)
    experience_vector = db.Column(db.Text)
    magnitude = db.Column(db.Integer, default = None)
    frequency = db.Column(db.Text)
    emotions = db.Column(db.Text)
    props = db.Column(db.Text)
    journey = db.Column(db.Text)
    archived = db.Column(db.Boolean, default = False)
    create_date = db.Column(db.DateTime,
                            default=datetime.utcnow)
    revision = db.Column(db.Integer, default = 0)
    creator_id = db.Column(db.Integer, default = None)
    cust_id = db.Column(db.Integer)
    personas = relationship('Persona' , secondary = 'insight_persona_rel' , backref=db.backref('insights') )
    products = relationship('Product' , secondary = 'insight_product_rel' , backref=db.backref('insights') )

class InsightSchema(ma.ModelSchema):
    personas = ma.Nested('PersonaSchema', many=True , exclude=('products','persona_picture','cust_id',))
    products = ma.Nested('ProductSchema', many=True, exclude=('personas','cust_id',))

    class Meta:
        model = Insight
        sqla_session = db.session

class InsightComments(db.Model):
    __tablename__ = 'insight_comments'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer,ForeignKey('insight.id'))
    comment_body = db.Column(db.Text)
    creator_id = db.Column(db.Integer, ForeignKey('users.user_id'))
    create_date = db.Column(db.DateTime,default=datetime.utcnow)
    user = db.relationship('User')

class InsightCommentsSchema(ma.ModelSchema):
    user = ma.Nested('UserSchema', exclude=('password_hash',))

    class Meta:
        model = InsightComments
        sqla_session = db.session

class InsightFile(db.Model):
    __tablename__ = 'insight_files'
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, ForeignKey('insight.id'))
    filename = db.Column(db.Text)
    file = db.Column(db.LargeBinary)
    filetype = db.Column(db.Text)

class InsightFileSchema(ma.ModelSchema):
    class Meta:
        model = InsightFile
        sqla_session = db.session


# INSIGHTS ---------------------------------------------------------------------
class Playlist(db.Model):
    __tablename__ = 'playlist'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('users.user_id'), index=True)
    source_table = db.Column(db.Text)
    source_id = db.Column(db.Integer)
    order = db.Column(db.Integer)


class PlaylistSchema(ma.ModelSchema):

    class Meta:
        model = Playlist
        sqla_session = db.session

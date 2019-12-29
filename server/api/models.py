from server import db, ma
from sqlalchemy.dialects.postgresql import JSON
from datetime import datetime


class Result(db.Model):
    __tablename__ = 'results'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String())
    result_all = db.Column(JSON)
    result_no_stop_words = db.Column(JSON)

    def __init__(self, url, result_all, result_no_stop_words):
        self.url = url
        self.result_all = result_all
        self.result_no_stop_words = result_no_stop_words

    def __repr__(self):
        return '<id {}>'.format(self.id)


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
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    revision = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    access_group = db.Column(db.Integer)
    archived = db.Column(db.Boolean, default=False)
    persona_file = db.Column(db.Binary)
    persona_picture = db.Column(db.Binary)


class PersonaSchema(ma.ModelSchema):
    class Meta:
        model = Persona
        sqla_session = db.session

class Product(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    metrics = db.Column(db.Text)
    goals = db.Column(db.Text)
    features = db.Column(db.Text)
    archived = db.Column(db.Boolean)
    owner = db.Column(db.Text)
    last_update  = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    create_date = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    revision = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    product_homepage = db.Column(db.Text)

    # def __init__(self,name,description,metrics,goals,features,archived,owner,last_update,create_date,revision,creator_id,product_homepage):
    #     self.name = name


class ProductSchema(ma.ModelSchema):
    class Meta:
        model = Product
        sqla_session = db.session

class Insight(db.Model):
    __tablename__ = 'insight'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    metrics = db.Column(db.Text)
    goals = db.Column(db.Text)
    features = db.Column(db.Text)
    archived = db.Column(db.Boolean)
    owner = db.Column(db.Text)
    last_update  = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    create_date = db.Column(db.DateTime,
                            default=datetime.utcnow,
                            onupdate=datetime.utcnow)
    revision = db.Column(db.Integer)
    creator_id = db.Column(db.Integer)
    product_homepage = db.Column(db.Text)

class InsightSchema(ma.ModelSchema):
    class Meta:
        model = Product
        sqla_session = db.session

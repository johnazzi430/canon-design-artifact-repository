


from flask_sqlalchemy import SQLAlchemy


#
class Persona:
    def __init__(self ,id,name,title,quote,
                job_function,needs,wants,pain_point,external,
                market_size,buss_val,record_date,
                revision,creator_id,access_group,archived,persona_file):
        self.id = id
        self.name = name
        self.title = title
        self.quote = quote
        self.job_function = job_function
        self.needs = needs
        self.wants = wants
        self.pain_point = pain_point
        self.external = external
        self.market_size = market_size
        self.buss_val = buss_val
        self.record_date = record_date
        slef.revision = revision
        self.creator_id = creator_id
        self.access_group = access_group
        self.archived = archived
        self.persona_file = persona_file


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)

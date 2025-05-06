# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy import MetaData

metadata = MetaData()
db = SQLAlchemy(metadata=metadata)

class Soldier(db.Model, SerializerMixin):
    __tablename__ = 'soldiers'
    serialize_rules = ('-machines.soldier',)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=False)
    machines = db.relationship('Machine', backref='soldier', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Soldier {self.id}, {self.rank} {self.name}>'

class Machine(db.Model, SerializerMixin):
    __tablename__ = 'machines'
    serialize_rules = ('-soldier.machines',)

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)
    serial_number = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String, default='Operational')
    assigned_soldier_id = db.Column(db.Integer, db.ForeignKey('soldiers.id'))

    def __repr__(self):
        return f'<Machine {self.id}, {self.type}, {self.status}>'

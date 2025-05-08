from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)

class Soldier(db.Model):
    __tablename__ = "soldiers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    rank = db.Column(db.String, nullable=False) 

    def __repr__(self):
        return f"<Soldier {self.id}, {self.name}, {self.rank}>"
    
from src.database import db

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
        }
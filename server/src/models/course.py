from src.database import db

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    thumbnail = db.Column(db.String, nullable=False)
    hours = db.Column(db.Integer, nullable=False)
    creator = db.Column(db.String, nullable=False)
    modules = db.Column(db.Integer, nullable=False)
    enrolled = db.Column(db.Integer, default=0)
    published_at = db.Column(db.Date, default=None)
    rating = db.Column(db.Float, default=0.0)
    tags = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "link": self.link,
            "thumbnail": self.thumbnail,
            "hours": self.hours,
            "creator": self.creator,
            "modules": self.modules,
            "enrolled": self.enrolled,
            "rating": self.rating,
            "published_at": self.published_at,
            "tags": [tag.lstrip() for tag in self.tags.split(",") if tag != " "],
            "description": self.description
        }
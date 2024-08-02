from src.database import db
from datetime import datetime

class Enrollment(db.Model):
    userid = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    courseid = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    is_completed = db.Column(db.Integer, nullable=False, default=False)
    completed_at = db.Column(db.DateTime, default=None)
    modules_completed = db.Column(db.Integer, nullable=False, default=0)
    rating = db.Column(db.Integer, default=None)

    def json(self):
        return {
            "userid": self.userid,
            "courseid": self.courseid,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at,
            "modules_completed": self.modules_completed,
            "rating": self.rating
        }
    
    def completed_course(self):
        self.is_completed = True
        self.completed_at = datetime.now()
    
    def ongoing_course(self):
        self.is_completed = False
        self.completed_at = None
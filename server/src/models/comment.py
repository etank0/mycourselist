from src.database import db
from datetime import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    receiverid = db.Column(db.Integer, db.ForeignKey('user.id'))
    senderid = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver_username = db.Column(db.String, nullable=False)
    sender_username = db.Column(db.String, nullable=False)
    sent_at = db.Column(db.DateTime, default=datetime.now())

    def json(self):
        return {
            "id": self.id,
            "comment": self.comment,
            "receiverid": self.receiverid,
            "receiver_username": self.receiver_username,
            "sender_username": self.sender_username,
            "senderid": self.senderid,
            "sent_at": self.sent_at,
        }
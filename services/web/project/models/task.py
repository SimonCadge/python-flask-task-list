from dataclasses import dataclass
import datetime
from project import db

@dataclass
class Task(db.Model):
    __tablename__ = 'task'

    id: int
    text: str
    # Since status is set to bool it is serialized/jsonified as True/False rather than 1/0.
    # I could set it to int, or write a custom serializer, if that is an issue.
    status: bool

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    text = db.Column(db.String(128), nullable=False)
    status = db.Column(db.Boolean(), default=False, nullable=False)
    # These two fields weren't in the spec but I add them to every table I ever make. They
    # always help a lot when debugging, but only if you added them before the bug happened,
    # which is why I now just add them to everything.
    created_at = db.Column(db.DateTime(timezone=True), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False)

    def __init__(self, text):
        self.text = text
        self.created_at = datetime.datetime.now(datetime.UTC)
        self.updated_at = datetime.datetime.now(datetime.UTC)
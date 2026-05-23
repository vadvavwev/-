from . import db
from datetime import datetime


class Device(db.Model):
    __tablename__ = "devices"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), default="")
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id", ondelete="RESTRICT"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    category = db.relationship("Category", back_populates="devices")

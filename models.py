from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    tasks = db.relationship('Task', back_populates='category', lazy='dynamic')

    def __repr__(self):
        return f"<Category {self.id} {self.name!r}>"

class Task(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(32), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    category = db.relationship('Category', back_populates='tasks')

    def __repr__(self):
        return f"<Task {self.id} {self.task!r} ({self.category.name if self.category else 'Unassigned'})>"

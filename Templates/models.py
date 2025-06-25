from Connect import db

# User Model
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    province_of_birth = db.Column(db.String(50))
    city_of_birth = db.Column(db.String(50))
    province_of_residence = db.Column(db.String(50))
    city_of_residence = db.Column(db.String(50))
    income = db.Column(db.String(50))
    contact_number = db.Column(db.String(15))

    # Relationship to Feedback
    feedbacks = db.relationship('Feedback', backref='user', lazy=True)

# Feedback Model
class Feedback(db.Model):
    __tablename__ = 'feedbacks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    neighborhood = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    severity = db.Column(db.String(20))
    date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

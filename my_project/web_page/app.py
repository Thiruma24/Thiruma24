from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize the Flask application
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/tailstone_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable tracking for better performance

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Ensure database tables are created
with app.app_context():
    db.create_all()

# Define routes
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name")
    email = request.form.get("email")
    if not name or not email:
        return "Name and email are required!", 400  # Return an error if input is invalid
    
    # Add the new user to the database
    new_user = User(name=name, email=email)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return f"An error occurred: {str(e)}", 500  # Handle database errors

    return f"Thank you, {name}! Your email {email} has been saved."

# Run the application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))



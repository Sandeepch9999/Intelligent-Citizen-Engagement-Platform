from flask import Flask, render_template, request, redirect, url_for, session, flash
from auth import auth  # Import the authentication blueprint
import joblib
import matplotlib.pyplot as plt


from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Initialize Flask app
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///connect.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Suppress warning

# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.secret_key = 'your_secret_key_here'
app.config['SESSION_PERMANENT'] = False  # Automatically log out when the app exits

# Register the authentication blueprint
app.register_blueprint(auth, url_prefix='/auth')

# Load the trained Logistic Regression model and vectorizer
model = joblib.load('model/model.pkl')
vectorizer = joblib.load('model/vectorizer.pkl')

# Function to create a bar chart
def create_bar_chart(data, filename):
    categories = list(data.keys())
    counts = list(data.values())
    plt.bar(categories, counts, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Feedback Categories')
    plt.savefig(f'static/{filename}')
    plt.close()

# Route for Home Page
@app.route('/')
def home():
    return render_template('home.html', user=session.get('user'))

# Route for Feedback Form
@app.route('/feedback', methods=['GET', 'POST'])
def feedback_form():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        feedback = request.form['feedback']
        neighborhood = request.form['neighborhood']
        postal_code = request.form['postal_code']
        severity = request.form['severity']
        date = request.form['date']
        reporting_for_name = request.form.get('reporting_for_name', None)
        reporting_for_contact = request.form.get('reporting_for_contact', None)

        # Process optional file attachment
        attachment = request.files.get('attachment', None)
        if attachment:
            attachment.save(f'static/uploads/{attachment.filename}')

        # Example logging for debugging (replace with actual processing)
        print(f"Feedback: {feedback}")
        print(f"Neighborhood/Area: {neighborhood}")
        print(f"Postal Code: {postal_code}")
        print(f"Severity: {severity}")
        print(f"Date: {date}")
        print(f"Reporting for Name: {reporting_for_name}")
        print(f"Reporting for Contact: {reporting_for_contact}")
        if attachment:
            print(f"Attachment saved as: static/uploads/{attachment.filename}")

        # Predict the category using the model
        category = model.predict(vectorizer.transform([feedback]))[0]
        print(f"Predicted Category: {category}")

        return render_template(
            'thank_you.html',
            message="Thank you for your feedback!",
            category=category,
            user=session.get('user'),
        )

    return render_template('feedback.html', user=session.get('user'))

# Route for the Dashboard
@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    data = {"Health": 10, "Infrastructure": 15, "Education": 5, "Environment": 8, "Transport": 12}
    create_bar_chart(data, 'chart.png')
    return render_template('dashboard.html', chart_url='/static/chart.png', user=session.get('user'))

# Route for Contact Us
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        return render_template('thank_you.html', message="Thank you for reaching out! We'll get back to you soon.", user=session.get('user'))
    return render_template('contact.html', user=session.get('user'))

if __name__ == '__main__':
    app.run(debug=True)

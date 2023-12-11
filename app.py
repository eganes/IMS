from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

@app.route('/')
def index():
    user = {'name': 'John Doe'}
    return render_template('index.html', user=user)

@app.route('/pages/dashboard.html')
def dashboard():
    return render_template('pages/dashboard.html')

@app.route('/pages/signup.html')
def signup():
    return render_template('pages/signup.html')

@app.route('/signupUser', methods=['POST'])
def signupUser():
    # Get form data from the request
    # username = request.form.get('username')
    # email = request.form.get('email')
    # password = request.form.get('password')
    # confirm_password = request.form.get('confirm-password')
    # print(f"Received signup request: Username - {username}, Email - {email}, Password - {password}")
    # return redirect(url_for('dashboard'))
     # Get form data from the request
    username = request.form.get('fullname')  # Update to match the form field name
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Perform basic form validation
    if not (username and email and password and password == confirm_password):
        return render_template('signup.html', error='Invalid form data. Please try again.')

    # Check if the user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return render_template('signup.html', error='User with this email already exists. Please use a different email.')

    # Create a new user and add to the database
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Redirect to the dashboard upon successful signup
    return redirect(url_for('dashboard'))

@app.route('/pages/policies.html')
def policies():
    return render_template('pages/policies.html')

@app.route('/pages/notifications.html')
def notifications():
    return render_template('pages/notifications.html')

@app.route('/pages/account.html')
def account():
    return render_template('pages/account.html')


@app.route('/initialize_database')
def initialize_database():
    with app.app_context():
        db.create_all()
        
        # Query all users
        users = User.query.all()

        for user in users:
            print("ID: {}, Username: {}, Email: {}, Password: {}".format(user.id, user.username, user.email, user.password))


    return 'Database initialized'




if __name__ == '__main__':
    app.run(debug=True)

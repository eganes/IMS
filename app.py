from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


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
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')

    # Perform signup logic (validate and store user data, for example)

    # For demonstration purposes, print the data to the console
    print(f"Received signup request: Username - {username}, Email - {email}, Password - {password}")

    # Redirect to a success page or do any other necessary actions
    # return "Signup successful! You can customize this response."
    # return render_template('pages/dashboard.html')
    # Redirect to the dashboard page
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

if __name__ == '__main__':
    app.run(debug=True)

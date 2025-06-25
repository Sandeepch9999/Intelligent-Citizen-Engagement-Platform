from flask import Blueprint, request, render_template, redirect, url_for, flash , session

auth = Blueprint('auth', __name__)

# Temporary in-memory storage for user data
users = {}

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collecting data from the signup form
        full_name = request.form['full_name']
        age = request.form['age']
        cnic = request.form['cnic']
        province_of_birth = request.form['province_of_birth']
        city_of_birth = request.form['city_of_birth']
        province_of_residence = request.form['province_of_residence']
        city_of_residence = request.form['city_of_residence']
        income = request.form['income']
        email = request.form['email']
        contact_number = request.form['contact_number']
        password = request.form['password']  # Add this field in the signup form for login

        # Logging the data for debugging
        print(f"Name: {full_name}, Age: {age}, CNIC: {cnic}")
        print(f"Province of Birth: {province_of_birth}, City of Birth: {city_of_birth}")
        print(f"Province of Residence: {province_of_residence}, City of Residence: {city_of_residence}")
        print(f"Income: {income}, Email: {email}, Contact: {contact_number}")

        # Store user data in the dictionary (temporary storage)
        users[email] = {
            'name': full_name,
            'age': age,
            'cnic': cnic,
            'birth_province': province_of_birth,
            'birth_city': city_of_birth,
            'residence_province': province_of_residence,
            'residence_city': city_of_residence,
            'income': income,
            'contact': contact_number,
            'password': password
        }

        # Flash success message
        flash('Sign-up successful! Please log in.')

        # Redirect to the login page
        return redirect(url_for('auth.login'))

    # Render the signup page for GET requests
    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = users.get(email)
        
        if user:
            if user['password'] == password:
                session['user'] = user['name']
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                return render_template('login.html', error="Invalid password. Please try again.")
        else:
            return render_template('login.html', error="Account not found. Please sign up.")
    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.pop('user', None)  # Remove user from session
    flash('Logged out successfully.')
    return redirect(url_for('auth.login'))

from flask import Flask, render_template, request, redirect, url_for
import password_testing

app = Flask(__name__)

user_logged_in = ''
@app.route('/', methods=['GET', 'POST'])
def login_and_register():  # put application's code here
    password_testing.initialise()
    if request.method == "POST":
        password = request.form.get("password")
        username = request.form.get("username")
        print(username, password)
        global user_logged_in
        if request.form.get("user_function") == "Login":
            if password_testing.login_attempt(username, password) == True:
                user_logged_in = username
                return redirect(url_for("dashboard"))
            else:
                return render_template('launch_page.html', failed_login=True)
        elif request.form.get("user_function") == "Register":
            valid_registration_flag = password_testing.is_username_valid(username)
            if valid_registration_flag == True:
                password_testing.add_user(username, password)
                new_user_file = f"static/{request.form.get('username')}.txt"
                create_file = open(new_user_file, "x")
                user_logged_in = username
                return redirect(url_for("dashboard"))
            else:
                return render_template('launch_page.html', user_already_created=True)
    return render_template('launch_page.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    print(user_logged_in)
    return render_template('dashboard.html', user_of_session=user_logged_in)
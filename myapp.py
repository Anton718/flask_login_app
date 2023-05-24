from flask import Flask, render_template, redirect, flash, url_for, request, session
import sqlite3
from datetime import timedelta
from passlib.hash import sha256_crypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfhsjnsfghsrthsfgaert34556rghfh'
app.permanent_session_lifetime = timedelta(minutes=30)

@app.route("/", methods=["POST", "GET"])
@app.route("/login", methods=["POST", "GET"])
def index():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            try:
                conn = sqlite3.connect('registered.db')
                input_email = request.form['email']
                input_pass = request.form['password']
                print(input_pass)
                print('connection established')
                curs = conn.cursor()
                password = curs.execute('select password from registers where email = ?', [input_email]).fetchone()
                to_string_hash = ''.join(password)
                print(to_string_hash)
                if (sha256_crypt.verify(input_pass, to_string_hash)):
                        session.permanent = True
                        session['user'] = request.form['email']
                        flash(f"""You logged in, welcome, <{request.form['email']}> !!
                        Explore what's new today in INFO section.""", 'info')
              
                else:
                    flash('Not registered or email and password incorrect.', 'error')
                    print('Not registered or email and password incorrect.')
            except: 
                conn.rollback()
                print("hmm")
                flash("Email or password is incorrect")
            finally:
                conn.close()
                print('connection closed')
                return redirect(url_for("index"))
        else:
            return render_template('login.html')



@app.route("/user", methods=["POST", "GET"])
def user():
        if "user" in session:
            user = session["user"]
            return render_template("home.html") 
        return redirect(url_for("register")) 


@app.route("/home", methods=["POST", "GET"])
def home():
        if "user" in session:
            return redirect(url_for("home"))
        return redirect(url_for("register")) 

@app.route("/register", methods=["POST", "GET"])
def register():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        if request.method == "POST":
            try:
                connection = sqlite3.connect('registered.db')
                connection.execute("INSERT INTO registers (email, password) VALUES (?, ?)", 
                (request.form['email'].lower(), sha256_crypt.hash(request.form['password'])))
                connection.commit()
                session.permanent = True
                session['user'] = request.form['email']
                flash('You are registered!')
            except: 
                connection.rollback()
                print('email already exists')
                flash(f"A user with  email: <{request.form['email']}> already exists.", 'error')
            finally:
                connection.close()
                return redirect(url_for("user"))
        return render_template("register.html")
             

@app.route("/logout")
def logout():
    session.pop("user", None)
    return render_template("logout.html")

@app.route("/about")
def about():
    if "user" in session:
        return redirect(url_for("user"))
    else:
        return render_template("about.html")
    

@app.route("/contacts", methods=["POST", "GET"])
def contacts():
    if "user" in session:
        return redirect(url_for("user"))
    elif request.method == 'POST':
         with open("emails.csv", "a") as file:
            email = request.form['mail']
            content = request.form['mailcontent']
            file.write(f"{email}, {content}\n") 
            flash("Your email was sent. Thank you!", "info")
            return render_template("contacts.html")
    else:
        return render_template("contacts.html")

    

@app.route("/videos")
def videos():
    if "user" not in session:
        return redirect(url_for("register")) 
    return render_template("videos.html")

@app.route("/photos")
def photos():
    if "user" not in session:
        return redirect(url_for("register")) 
    return render_template("photos.html")

@app.route("/chat")
def something():
    if "user" not in session:
        return redirect(url_for("register")) 
    return render_template("chat.html")   
    


if __name__ == "__main__":
    app.run(debug=True, port=8080)
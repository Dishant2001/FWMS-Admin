from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = '4f2bfa6592418c6a7e50573998ce99db'

# Mock database for user credentials
users = {'test1': '123456', 'test2': '789100'}

# Here we are creating two routes for login normal and /login 
# Both work same 
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid username or password')  
    return render_template('login.html')

# This is the route for home page were strategies run
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)

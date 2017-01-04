from flask import Flask, session, redirect, url_for, escape, request, render_template, abort
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/user/<string:username>')
def user():
    pass


@app.route('/admin')
def admin():
    return render_template("admin.html")


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        do_login()
    else:
        # show_login_form()
        return render_template("login.html")

@app.route('/logout')
def logout():
    # remove the username from the session
    session.pop('username', None)
    return redirect(url_for('index'))


def do_login():
    pass


def show_login_form():
    pass


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.secret_key = '|]b\xa1O\xc7\xe7FP\xd7~lGl\xa5X\xce\x0c\x9a>\x9f[!\x02'
if __name__ == "__main__":
    app.run()

from pymongo import MongoClient
from flask import Flask, session, redirect, url_for, escape, request, render_template, abort
from library import lib
app = Flask(__name__)

client = MongoClient()
db = client.yelp
#print(db.collection_names())




def get_latitude(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"latitude": 1}):
        return i['latitude']

def get_longitude(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"longitude": 1}):
        return i['longitude']

def get_review_count(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"review_count": 1}):
        return i['review_count']

def get_star_rating(business_id):
    for i in db.businesses.find({'business_id': business_id}, {"stars": 1}):
        return i['stars']


print(get_latitude('m5hMJ7SPIK7are8SykvlvA'))






@app.route('/')
@app.route('/index')
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
        user_id = request.form.get('user_id')
        # print(user_id)

        print(lib.get_user_lda_sims(user_id))
        # library.get_user_lda_sims()
        # lib.get_user_lda_sims()


        return redirect('/')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session
    session.pop('username', None)
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.secret_key = '|]b\xa1O\xc7\xe7FP\xd7~lGl\xa5X\xce\x0c\x9a>\x9f[!\x02'
if __name__ == "__main__":
    app.run()

from pymongo import MongoClient
<<<<<<< HEAD
from flask import Flask, session, redirect, url_for, escape, request, render_template, abort, g
=======
from flask import Flask, session, redirect, url_for, escape, request, render_template, abort
from library import lib
>>>>>>> 3c3368e6106baab57a830074ec52d388d81e26d1
app = Flask(__name__)

client = MongoClient()
db = client.yelp
# print(db.collection_names())

# class User():
#     _tablename_ = "users"
#     username = db.Column('user_id', db.String(30), unique=True)




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


#business list
def business_id_longlat_attributes(business_id_list):
    long = []
    for i in business_id_list:
        for x in db.businesseses.find({'business_id': i}, {"longitude":1}):
            long.append(x['longitude'])
    return long

def business_id_longlat_attributes(business_id_list):
    lat = []
    for i in business_id_list:
        for x in db.businesseses.find({'business_id': i}, {"latitude":1}):
            lat.append(x['latitude'])
    return lat

def business_id_star_attributes(business_id_list):
    star = []
    for i in business_id_list:
        for x in db.businesseses.find({'business_id': i}, {"stars":1}):
            star.append(x['stars'])
    return star

def business_id_review_attributes(business_id_list):
    review = []
    for i in business_id_list:
        for x in db.businesseses.find({'business_id': i}, {"review_count":1}):
            review.append(x['review_count'])
    return review




mock_restaurants = ['mVHrayjG3uZ_RLHkLj-AMg','KayYbHCt-RkbGcPdGOThNg', 'wJr6kSA5dchdgOdwH6dZ2w', 'fNGIbpazjTRdXgwRY_NIXA', 'b9WZJp5L1RZr4F1nxclOoQ', 'zaXDakTd3RXyOa7sMrUE1g', '6o3RK6rTcN3nw-j-r2nQmA', 'rv7CY8G_XibTx82YhuqQRw', 'SQ0j7bgSTazkVQlF5AnqyQ']

#print(get_latitude('m5hMJ7SPIK7are8SykvlvA'))



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
        # lib.
        # library.get_user_lda_sims()
        # lib.get_user_lda_sims()


        return redirect('/')
    return render_template('login.html')
    # if request.method == 'GET':
    #     return render_template('login.html')
    # username = request.form['user_id']
    # registered = User.query.filter_by(user_id=username).first()
    # if registered is None:
    #     flash('Invalid username', 'error')
    #     return render_template('login.html')
    # return redirect('/')


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

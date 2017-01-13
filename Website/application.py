from pymongo import MongoClient
from flask import Flask, session, redirect, url_for, jsonify, escape, request, render_template, abort
from library import lib
app = Flask(__name__)

client = MongoClient()
db = client.yelp
# print(db.collection_names())


def get_restaurant_from_index(indx):
    restaurant = db.vegas_restaurants.find()[indx]

    return {
        'name': restaurant['name'],
        'address': restaurant['full_address'],
        'stars': restaurant['stars'],
        'review_count': restaurant['review_count'],
        'categories': restaurant['categories'],
        'longitude': restaurant['longitude'],
        'latitude': restaurant['latitude']
    }


@app.route('/query', methods=["GET", "POST"])
def search_query():
    if request.method == 'POST':
        query = request.form.get('query')

        restaurants = lib.get_recommendation(query)
        container = []
        count = 0
        for rest in restaurants:
            container.append(get_restaurant_from_index(rest[0]))
            count += 1
            if count > 10:
                break

        return jsonify(container)

        # print(query, session.get('user_topic'))
        # return "yes"


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", username=session['username'])


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
        username = db.vegas_users.find_one({'user_id': user_id})['name']

        get_user_topic = lib.get_user_lda_sims(user_id)
        print(get_user_topic, username)
        session['user_topic'] = get_user_topic
        session['username'] = username

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
    # session.pop('username', None)
    session.clear()
    return redirect(url_for('login'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

app.secret_key = '|]b\xa1O\xc7\xe7FP\xd7~lGl\xa5X\xce\x0c\x9a>\x9f[!\x02'
if __name__ == "__main__":
    app.run()

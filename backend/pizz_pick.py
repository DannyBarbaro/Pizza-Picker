import configparser
import pymysql
import math
from flask import Flask, render_template, request, jsonify
import query_templates as qt
from flask_cors import CORS

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)
CORS(app)

# Create a function for fetching data from the database.
def sql_query(sql, args=None):
    db = pymysql.connect(**config['pymysql.connect'])
    cursor = db.cursor()
    cursor.execute(sql, args)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def sql_execute(sql, args=None):
    db = pymysql.connect(**config['pymysql.connect'])
    cursor = db.cursor()
    cursor.execute(sql, args)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.

@app.route('/auth')
def auth():
    username = request.headers['user']
    password = request.headers['pass']
    return jsonify(sql_query(qt.validate_user, (username, password))[0][0] == 1)

# routing user to different things
@app.route('/availableUser/<username>')
def check_user(username):
    # query database for if the user under username exists
    # if exists, return true
    # else, return false
    
    return jsonify(result="True")

def make_pizzas(prefs_list):
    """
    Takes as input a list of preferences containing topping-yumminess pairs.
    Yumminess quotient values should be set as -2 for allergic to this thing, as
    -1 for they dislike the thing, and as 1 for they like the thing.  Ignores any
    toppings that at least one person in the order is allergic to.  Creates a
    vector that can hold values for all the toppings that might get put on the
    pizza.  Does magical nonsense to put toppings together that won't upset
    anyone.  Calculates the size of the pizza using number of standard size
    slices, and assumes the magical constant of average 3.5 slices per person,
    rounded down to the nearest multiple of 2 with a minimum of 8.  The acceptable
    range of sizes are small (8), medium (10), large (12), and extra large 14).

    Returns a list of pizzas.  Each pizza is a list of tuples containing the
    toppings on a slice and how many slices have those toppings.
    """
    num_slices = min(math.floor((3.5 * len(prefs_list))/2)*2, 8)

    # dict that matches topping name to a (num_likes, num_dislikes) pair
    topping_yummy = {}
    bad_tops = []
    # for each person's preference list
    for pref in prefs_list:
        # for each topping specification in a person's preference
        for top_yum in pref:
            # if someone else is allergic to this topping
            if top_yum[0] in bad_tops:
                continue
            # if this person is allergic to this topping
            if top_yum[1] == -2:
                # put the topping in the bad topping list
                bad_tops.append(top_yum[0])
                # remove the topping from the topping list if someone else already put it in
                if top_yum[0] in topping_yummy:
                    del topping_yummy[top_yum[0]]
            # if someone else already had a preference for the topping
            elif top_yum[0] in topping_yummy:
                # if this person likes the topping
                if top_yum[1] > 0:
                    # increment num_likes
                    topping_yummy[top_yum[0]] = (topping_yummy[top_yum[0]][0]+1, topping_yummy[top_yum[0]][1])
                # if this person doesn't like the topping
                else:
                    # increment num_dislikes
                    topping_yummy[top_yum[0]] = (topping_yummy[top_yum[0]][0], topping_yummy[top_yum[0]][1]+1)
            # if no one has mentioned the topping before
            else:
                if top_yum[1] > 0:
                    topping_yummy[top_yum[0]] = (1, 0)
                else:
                    topping_yummy[top_yum[0]] = (0, 1)

    pref_vecs = []
    for pref in prefs_list:
        pref_vecs.append([])


#@app.route('/', methods=['GET', 'POST'])
def template_response_with_data():
    print(request.form)
    if "buy-book" in request.form:
        book_id = int(request.form["buy-book"])
        sql = "delete from book where id={book_id}".format(book_id=book_id)
        sql_execute(sql)
    template_data = {}
    sql = "select id, title from book order by title"
    books = sql_query(sql)
    template_data['books'] = books
    return render_template('home-w-data.html', template_data=template_data)

if __name__ == '__main__':
    app.run(**config['app'])

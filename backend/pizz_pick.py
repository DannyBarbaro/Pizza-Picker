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

# routing user to different things
@app.route('/userExists/<username>')
def check_user(username):
    # query database for if <username> is already being used for some account
    # if exists, return true
    # else, return false
    return jsonify(sql_query(qt.check_user, (username))[0][0] == 1)

@app.route('/newUser', methods=['POST'])
def make_new_user():
    # header has username and password
    # get values from header, and send it down to db
    # return some success/fail message?
    user = request.headers['user']
    password = request.headers['pass']
    sql_execute(qt.new_user, (user, password))
    #I'm going to assume this returns an empty 200

@app.route('/auth')
def validate_login():
    # header has username and password
    # check if account exists w/ those credentials (count > 0)
    # return success/fail
    username = request.headers['user']
    password = request.headers['pass']
    return jsonify(sql_query(qt.validate_user, (username, password))[0][0] == 1)

@app.route('/friends/<username>')
def get_friends(username):
    # query for all friends under the account with <username>
    # return a json with a list of the friends
    result = sql_query(qt.get_friends, (username))
    fixed = []
    #this isn't quite working yet
    for friend in result:
        fixed.append(friend[0])
    return jsonify(fixed)

@app.route('/friend/<username1>/<username2>', methods=['POST'])
def make_new_friend(username1, username2):
    # send new friend relationships for <username1> and <username2>
    # make sure to add the relationship in both directions
    # return success/fail?
    sql_execute(qt.new_friends, (username1, username2))
    sql_execute(qt.new_friends, (username2, username1))
    # returns empty 200?

@app.route('/unfriend/<username1>/<username2>', methods=['DELETE'])
def remove_friend(username1, username2):
    # remove friend relationship between <username1> and <username2>
    # remove relationship in both directions
    # return success/fail?
    sql_execute(qt.remove_friends, (username1, username2))
    sql_execute(qt.remove_friends, (username2, username1))
    return "1"

@app.route('/prefsets/<username>')
def get_preference_sets(username):
    # query for all preference sets under <username>
    # return a json with the list of prefs
    result = sql_query(qt.get_preference_sets, (username))

    raise NotImplementedError

@app.route('/current/<username>/<prefSetName>', methods=['POST'])
def change_current_pref_set(username, prefSetName):
    # mark current set of <username> to be <prefSetName>
    # return success/fail?
    raise NotImplementedError

@app.route('/order', methods=['POST'])
def place_order():
    # body has list of <username>s participating in order
    # not sure where the prefs are here?
    # guessing prefs will get queried later, but then this one can't actually generate the order
    raise NotImplementedError

@app.route('/stat/total/<username>')
def get_total_orders(username):
    # query for total order value under <username>
    # return json with number
    raise NotImplementedError

@app.route('/stat/bestfriend/<username>')
def get_best_pizza_pal(username):
    # query for best friend of <username>
    # return json with username of best friend
    raise NotImplementedError

@app.route('/stat/favTop/<username>')
def get_fav_top(username):
    # query for favorite topping of <username>
    # return json with topping
    raise NotImplementedError

@app.route('/toppings/<username>')
def get_topping_list(username):
    # query for all available toppings
    # return json with list of toppings
    raise NotImplementedError

@app.route('/prefs/<set_id>')
def get_preference(set_id):
    # query for all toppings/yummy values in preference set <prefSetName> under <username>
    # return a json with toppings and yummy values
    raise NotImplementedError

@app.route('/prefsUpdate/<set_id>', methods=['POST'])
def update_preference_set(set_id):
    # body contains preferences
    # delete old preferences under <prefSetName>?
    ### are we wiping every time or do we have a way to know what was removed and added?
    # send new ones to db
    # return success/fail
    raise NotImplementedError

@app.route('/prefsNew/<username>', methods=['POST'])
def make_new_preference_set(username):
    # body contains preferences
    # construct new preference, send to db
    # return success/fail
    pref_set = request.get_json()
    sql_execute(qt.new_preference_set, (pref_set['name']))
    raise NotImplementedError

def make_pizzas(prefs_list): # change to also take the standard topping list?
    """
    Takes as input a list of preferences containing topping-yumminess pairs.
    Yumminess quotient values should be set as -2 for allergic to this thing, as
    -1 for they dislike the thing, and as 1 for they like the thing.  Ignores any
    toppings that at least one person in the order is allergic to.  Creates a
    vector that can hold values for all the toppings that might get put on the
    pizza.  Does magical nonsense to put toppings together that won't upset
    anyone.  Calculates the size of the pizza using number of standard size
    slices, and assumes the magical constant of average 3.5 slices per person,
    rounded down to the nearest multiple of 2 with a minimum of 8.

    Returns a list of pairs containing the set of toppings on a slice and how
    many of those
    """
    num_slices = max(math.floor((3.5 * len(prefs_list))/2)*2, 8)
    slice_per_person = num_slices / len(prefs_list)
    leftovers = num_slices % len(prefs_list)

    # dict that matches topping name to a num_likes-num_dislikes difference
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
                topping_yummy[top_yum[0]] += top_yum[1]
            # if no one has mentioned the topping before
            else:
                topping_yummy[top_yum[0]] = top_yum[1]

    standard_top_order = []
    best_topping = ("", -999999) # order limited to at most 1000000 people so this doesn't break
    for topping in topping_yummy:
        standard_top_order.append(topping)
        if topping_yummy[topping] > best_topping[1]:
            best_topping = (topping, topping_yummy[topping])
    best_topping = best_topping[0]

    # make standard ordered and sanatized vectors of yumminess quotients for each preference
    pref_vecs = []
    for pref in prefs_list:
        pref_vecs.append([])
        for topping in topping_yummy:
            if (topping, -1) in pref:
                pref_vecs[-1].append(-1)
            elif (topping, 1) in pref:
                pref_vecs[-1].append(1)
            else:
                pref_vecs[-1].append(0)
        # a value to track how many people agree with this topping set
        pref_vecs[-1].append(1)

    used_indices = []
    num_combos = len(pref_vecs)

    i = 0
    while i < len(pref_vecs):
        if i in used_indices:
            i += 1
            continue
        j = 0
        while j < len(pref_vecs):
            if i in used_indices:
                break
            if i == j or j in used_indices:
                j += 1
                continue
            combo_vec = []
            good_combo = True
            for k in range(len(pref_vecs[0])):
                combo_vec.append(pref_vecs[i][k] + pref_vecs[j][k])
                # if the two preferences have some conflict of interest: one like, the other dislike
                if abs(combo_vec[k]) < abs(pref_vecs[i][k]) or abs(combo_vec[k]) < abs(pref_vecs[j][k]):
                    good_combo = False
                    break
            if good_combo:
                used_indices.extend([i, j])
                pref_vecs.append(combo_vec)
                num_combos -= 1
            j += 1
        i += 1

    slice_set = []
    for i in range(len(pref_vecs)):
        if i in used_indices:
            continue
        topping_list = []
        for topping, j in standard_top_order, range(len(pref_vecs[0])-1):
            if pref_vecs[j] > 0:
                topping_list.append(topping)
        slice_set.append((topping_list, slice_per_person * pref_vecs[i][-1]))

    if leftovers > 0:
        # fill in the rest with the most popular topping
        slice_set.append(((best_topping), leftovers))

    return slice_set

if __name__ == '__main__':
    app.run(**config['app'])

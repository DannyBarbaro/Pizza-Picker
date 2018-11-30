import configparser
import pymysql
import math
from flask import Flask, request, jsonify, make_response
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
    return make_response()

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
    return make_response()

@app.route('/unfriend/<username1>/<username2>', methods=['DELETE'])
def remove_friend(username1, username2):
    # remove friend relationship between <username1> and <username2>
    # remove relationship in both directions
    # return success/fail?
    sql_execute(qt.remove_friends, (username1, username2))
    sql_execute(qt.remove_friends, (username2, username1))
    return make_response()


@app.route('/prefsets/<username>')
def get_preference_sets(username):
    # query for all preference sets under <username>
    # return a json with the list of prefs
    result = sql_query(qt.get_preference_sets, (username))
    sets = []
    for set in result:
        prefs = sql_query(qt.get_preferences, (set[0]))
        fixed = []
        for pref in prefs:
            fixed.append({'topping': pref[0], 'score': pref[1]})
        sets.append({'id': set[0], 'name': set[2], 'isCurrent': set[3] == 1, 'prefs': fixed})
    return jsonify(sets)

@app.route('/current/<username>/<pref_id>', methods=['POST'])
def change_current_pref_set(username, pref_id):
    # mark current set of <username> to be <pref_id>
    # unmark old current set
    # return success/fail?
    sql_execute(qt.deselect_current_set, (username))
    sql_execute(qt.activate_preference_set, (pref_id))
    return make_response()

@app.route('/order', methods=['POST'])
def place_order():
    # body has list of <username>s participating in order
    # get their active preference sets, generate safe topping list, pass to algo

    #get toppings
    hungry_bois = request.get_json()
    param_list = qt.format_list(hungry_bois)
    query = qt.get_valid_toppings % (param_list, param_list)
    toppings = sql_query(query, list(hungry_bois) + list(hungry_bois))

    # make topping list from a dict from query
    fixed_toppings = []
    for topping in toppings:
        fixed_toppings.append(topping[0])

    #get active sets for each person
    actives = []
    for boi in hungry_bois:
        actives.append(sql_query(qt.get_active_set, (boi))[0][0])

    #for each person get scores
    topping_params = qt.format_list(fixed_toppings)
    query = qt.get_topping_scores % ("%s", topping_params)
    scores = []
    for id in actives:
        scores.append([])
        for pair in sql_query(query, [id] + fixed_toppings):
            scores[-1].append(pair[1])

    division = make_pizzas(fixed_toppings, scores)

    components = []
    toppings_used = []
    for part in division:
        components.append({'toppings': part[0], 'sliceCount': part[1]})
        #add toppings to the list for safekeeping
        for top in part[0]:
            if top not in toppings_used:
                toppings_used.append(top)

    sql_execute(qt.create_order, None)
    id = sql_query(qt.get_recent_order, None)[0][0]
    for boi in hungry_bois:
        for top in toppings_used:
            sql_execute(qt.add_order_details, (id, boi, top))

    return jsonify({'components': components})

@app.route('/stat/total/<username>')
def get_total_orders(username):
    # query for total order value under <username>
    # return json with number
    result = sql_query(qt.get_order_count, (username))
    return jsonify(result[0][0])

@app.route('/stat/bestfriend/<username>')
def get_best_pizza_pal(username):
    # query for best friend of <username>
    # return json with username of best friend
    result = sql_query(qt.get_best_friend, (username))
    if (result == ()):
        return '"You haven\'t ordered any pizzas yet!"'
    return jsonify(result[0][0])

@app.route('/stat/favTop/<username>')
def get_fav_top(username):
    # query for favorite topping of <username>
    # return json with topping
    result = sql_query(qt.get_favorite_toppings, (username))
    if (result == ()):
        return '"Seriously, get yourself a pizza!"'
    return jsonify(result[0][0])

@app.route('/toppings')
def get_topping_list():
    # query for all available toppings
    # return json with list of toppings
    toppings = sql_query(qt.get_toppings)
    fixed = []
    for topping in toppings:
        fixed.append(topping[0])
    return jsonify(fixed)

@app.route('/prefs/<set_id>')
def get_preference(set_id):
    # query for all toppings/yummy values in preference set with matching ID
    # return a json with toppings and yummy values
    result = sql_query(qt.get_preferences, (set_id))
    fixed = []
    for pref in result:
        fixed.append(pref[0])
    return jsonify(fixed)

@app.route('/prefsUpdate/<set_id>', methods=['POST'])
def update_preference_set(set_id):
    # body contains preferences
    # update records in db and create any new ones
    pref_set = request.get_json()

    for pref in pref_set['preferences']:
        params = {'set_id': set_id, 'topping': pref['topping'], 'score': pref['score']}
        sql_execute(qt.update_preference, params)
    
    return make_response()

@app.route('/prefsNew/<username>', methods=['POST'])
def make_new_preference_set(username):
    # body contains preferences
    # construct new preference, send to db
    # return ID of new set
    pref_set = request.get_json()

    #make this set active if it is the first one
    if sql_query(qt.get_set_count, (username)) == ():
        sql_execute(qt.new_preference_set, (username, pref_set['name'], 1))
    else:
        sql_execute(qt.new_preference_set, (username, pref_set['name'], 0))

    #add preferences
    set_id = sql_query(qt.get_preference_set_id, (username, pref_set['name']))[0][0]
    for pref in pref_set['preferences']:
        print(pref)
        sql_execute(qt.new_preference, (pref['topping'], set_id, pref['score']))

    return jsonify(set_id)

@app.route('/removePref/<set_id>', methods=['DELETE'])
def delete_preference_set(set_id):
    #Deletes the preferences and preference set with the specified ID
    sql_execute(qt.delete_preference, (set_id))
    sql_execute(qt.delete_preference_set, (set_id))
    return make_response()


@app.route('/allergies/<username>')
def get_user_allergies(username):
    #query for all toppings the user is allergic to
    allergies = sql_query(qt.get_allergies, (username))
    fixed = []
    for allergy in allergies:
        fixed.append(allergy[0])
    return jsonify(fixed)

@app.route('/allergy/<username>/<topping>', methods=['POST'])
def toggle_allergy(username, topping):
    #Search for an allergy. Delete it if found. Otherwise create one.
    print(sql_query(qt.check_allergy, (username, topping)))
    if sql_query(qt.check_allergy, (username, topping))[0][0] == 1:
        sql_execute(qt.delete_allergy, (username, topping))
    else:
        sql_execute(qt.new_allergy, (username, topping))

    return make_response()

def make_pizzas(good_topping_list, pref_vecs): # change to also take the standard topping list?
    """
    Takes as input a list good_topping_list that contains every topping that at
    least one user in the order likes and no user in the order is allergic to,
    and a list pref_vecs of preference value vectors.  Each vector holds values
    1, -1, and 0 to signify like, dislike, and neutral, respectively.  The values
    correspond to toppings in the same order as they appear in good_topping_list

    Does magical nonsense to put toppings together that won't upset
    anyone.  Calculates the size of the pizza using number of standard size
    slices, and assumes the magical constant of average 3.5 slices per person,
    rounded down to the nearest multiple of 2 with a minimum of 8.

    Returns a list of pairs containing the set of toppings on a slice and how
    many of that type of slice
    """
    num_slices = max(math.floor((3.5 * len(pref_vecs))/2)*2, 8)
    slice_per_person = num_slices / len(pref_vecs)
    leftovers = num_slices % len(pref_vecs)

    sum_vec = [0] * len(pref_vecs)
    # sum preference vectors to find topping with largest like - dislike difference
    for vec in pref_vecs:
        for i in range(len(vec)):
            sum_vec[i] += vec[i]
        # a value to track how many people agree with this topping set
        vec.append(1)

    best_val = -999999
    best_index = -1
    for i in range(len(sum_vec)):
        if sum_vec[i] > best_val:
            best_val = sum_vec[i]
            best_index = i
    best_topping = good_topping_list[best_index]

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
        for topping, j in topping_list, range(len(pref_vecs[0])-1):
            if pref_vecs[j] > 0:
                topping_list.append(topping)
        slice_set.append((topping_list, slice_per_person * pref_vecs[i][-1]))

    if leftovers > 0:
        # fill in the rest with the most popular topping
        slice_set.append(((best_topping), leftovers))

    return slice_set

if __name__ == '__main__':
    app.run(**config['app'])

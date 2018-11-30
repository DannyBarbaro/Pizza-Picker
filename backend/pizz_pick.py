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
    return "It doesn't actually return an empty 200"

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
    return "didit"

@app.route('/unfriend/<username1>/<username2>', methods=['DELETE'])
def remove_friend(username1, username2):
    # remove friend relationship between <username1> and <username2>
    # remove relationship in both directions
    # return success/fail?
    sql_execute(qt.remove_friends, (username1, username2))
    sql_execute(qt.remove_friends, (username2, username1))
    return "So, there's a man crawling through the desert. He'd decided to try \
    his SUV in a little bit of cross-country travel, had great fun zooming over \
    the badlands and through the sand, got lost, hit a big rock, and then he \
    couldn't get it started again. There were no cell phone towers anywhere near, \
    so his cell phone was useless. He had no family, his parents had died a few \
    years before in an auto accident, and his few friends had no idea he was out \
    here. He stayed with the car for a day or so, but his one bottle of water ran \
    out and he was getting thirsty. He thought maybe he knew the direction back, \
    now that he'd paid attention to the sun and thought he'd figured out which \
    way was north, so he decided to start walking. He figured he only had to go \
    about 30 miles or so and he'd be back to the small town he'd gotten gas in \
    last. He thinks about walking at night to avoid the heat and sun, but based \
    upon how dark it actually was the night before, and given that he has no \
    flashlight, he's afraid that he'll break a leg or step on a rattlesnake. So, \
    he puts on some sun block, puts the rest in his pocket for reapplication \
    later, brings an umbrella he'd had in the back of the SUV with him to give \
    him a little shade, pours the windshield wiper fluid into his water bottle \
    in case he gets that desperate, brings his pocket knife in case he finds a \
    cactus that looks like it might have water in it, and heads out in the \
    direction he thinks is right. He walks for the entire day. By the end of the \
    day he's really thirsty. He's been sweating all day, and his lips are \
    starting to crack. He's reapplied the sunblock twice, and tried to stay under \
    the umbrella, but he still feels sunburned. The windshield wiper fluid \
    sloshing in the bottle in his pocket is really getting tempting now. He knows \
    that it's mainly water and some ethanol and coloring, but he also knows that \
    they add some kind of poison to it to keep people from drinking it. He \
    wonders what the poison is, and whether the poison would be worse than dying \
    of thirst. He pushes on, trying to get to that small town before dark. By the \
    end of the day he starts getting worried. He figures he's been walking at \
    least 3 miles an hour, according to his watch for over 10 hours. That means \
    that if his estimate was right that he should be close to the town. But he \
    doesn't recognize any of this. He had to cross a dry creek bed a mile or two \
    back, and he doesn't remember coming through it in the SUV. He figures that \
    maybe he got his direction off just a little and that the dry creek bed was \
    just off to one side of his path. He tells himself that he's close, and that \
    after dark he'll start seeing the town lights over one of these hills, and \
    that'll be all he needs. "


@app.route('/prefsets/<username>')
def get_preference_sets(username):
    # query for all preference sets under <username>
    # return a json with the list of prefs
    result = sql_query(qt.get_preference_sets, (username))
    sets = []
    for set in result:
        sets.append(set[0])
    return jsonify(sets)

@app.route('/current/<username>/<prefSetName>', methods=['POST'])
def change_current_pref_set(username, prefSetName):
    # mark current set of <username> to be <prefSetName>
    # unmark old current set
    # return success/fail?
    sql_execute(qt.deselect_current_set, (username))
    sql_execute(qt.activate_preference_set, (username, prefSetName))
    return  "condescending conned ascending con dissenting condor-sending \
    condescending con's descending condor sending condor-sending condescending \
    con's dissenting conte's ending condescending con-dissenting Condi's ending \
    condescending contes ending condescending Khan's descending on dissenting \
    conned ascending con dissenting condor-sending condescending con's descending \
    condor sending condor-sending condescending con's dissenting conte's ending \
    condescending con-dissenting Condi's ending condescending contes sending \
    condescending Khan descending condescending condor-sending condescending \
    con's descending condor sending condor-sending condescending con's dissenting \
    conte's ending condescending con-dissenting Condi's ending condescending contes \
    ending condescending conned ascending con's dissenting on dissenting \
    condor-sending con's descending condor sending condor-sending condescending \
    con's dissenting conte's ending condescending con-dissenting Condi's ending \
    condescending contes sending condescending conned ascending con's dissenting \
    condor-sending condescending con's descending condor sending condor-sending \
    condescending con's dissenting conte's ending condescending con-dissenting \
    Condi's ending condescending contes on descending condescending Khan's descending"

@app.route('/order', methods=['POST'])
def place_order():
    # body has list of <username>s participating in order
    # get their active preference sets, generate safe topping list, pass to algo
    hungry_bois = request.headers['users']
    active_sets = []
    for boi in hungry_bois:
        active_sets.append(sql_query(qt.get_active_set, (boi))[0][0])
    # make topping list from a dict from
    raise NotImplementedError

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
    return jsonify(result[0][0])

@app.route('/stat/favTop/<username>')
def get_fav_top(username):
    # query for favorite topping of <username>
    # return json with topping
    result = sql_query(qt.get_favorite_toppings, (username))
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

@app.route('/prefsNew/<set_id>', methods=['POST'])
def make_new_preference_set(username, prefSetName):
    # body contains preferences
    # construct new preference, send to db
    # return ID of new set
    pref_set = request.get_json()

    #make this set active if it is the first one
    if sql_query(qt.get_set_count, (username))[0][0] == 0:
        sql_execute(qt.new_preference_set, (username, pref_set['name'], 1))
    else:
        sql_execute(qt.new_preference_set, (username, pref_set['name'], 0))

    #add preferences
    set_id = sql_query(qt.get_preference_set_id, (username, pref_set['name']))
    for pref in pref_set['prefs']:
        sql_execute(qt.new_preference, (pref['topping'], set_id, pref['score']))

    return jsonify(set_id)

@app.route('/allergies/<username>')
def get_user_allergies(username):
    #query for all toppings the user is allergic to
    allergies = sql_query(qt.get_allergies, (username))
    fixed = []
    for allergy in allergies:
        fixed.append(allergy[0])
    return jsonify(fixed)

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

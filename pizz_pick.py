import configparser
import pymysql
import math
from flask import Flask, render_template, request

# Read configuration from file.
config = configparser.ConfigParser()
config.read('config.ini')

# Set up application server.
app = Flask(__name__)

# Create a function for fetching data from the database.
def sql_query(sql):
    db = pymysql.connect(**config['pymysql.connect'])
    cursor = db.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def sql_execute(sql):
    db = pymysql.connect(**config['pymysql.connect'])
    cursor = db.cursor()
    cursor.execute(sql)
    db.commit()
    cursor.close()
    db.close()

# For this example you can select a handler function by
# uncommenting one of the @app.route decorators.

# routing user to different things
@app.route('/availableUser/<username>')
def check_user(username):
    print(request.form)
    # query database for if the user under username exists
    # if exists, return true
    # else, return false
    return True

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
    best_topping = ("", -999999)
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

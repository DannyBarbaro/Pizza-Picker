def format_list(list):
    """Accepts a list and returns a format string that you can use
    as a parameter for any query that accepts a list as a parameter."""
    return ','.join(['%s'] * len(list))

#Create a user
#params: username and password of new user
#Password is not encrypted in any way.
new_user = "insert into User values (%s, %s)"

#Checks if a user exists
#params: username
#returns 1 if the user exists, 0 otherwise
check_user = "select count(1) from User where username = %s"

#validate a user
#params: username and password to validate.
#returns 1 if the password is correct, 0 otherwise
validate_user = "select count(1) from User where username = %s and password = %s"

#Get all preference sets for a given user
#params: username
#returns all preference sets that are associated with username
get_preference_sets = "select * from Preference_Set where user = %s"

# Get active preference set for a given user
# Params: username
# returns the set that the user has selected to be active for orders
get_active_set = "select * from Preference_Set where user = %s and is_active = 1"

#Get the preferences that make up a set
#params: ID of the preference set
#returns all toppings and scores for the preference
get_preferences = "select topping, score from Preference where set_id = %s"

#Get the allergies for a user
#params: username
#returns a list of all allergies that are associated with username
get_allergies = "select topping from Allergy where user = %s"

#Get all toppings that should be considered when creating a pizza
#params: dict containing the users
#returns a list of toppings such that each topping is desired by at least 1 user
# and no user is allergic to any topping.
get_valid_toppings = "select distinct p.topping " \
                     "from Preference_Set ps " \
                     "inner join Preference p on p.set_id = ps.id " \
                     "where ps.user in (%(users)s) and ps.is_active = 1 and p.topping not in " \
                          "(select distinct topping from Allergy where user in (%(users)s)"

#Get the score for toppings in a preference set
#params: Preference set ID, list of toppings
#returns the topping and the score of that topping
get_topping_scores = "select topping, score from Preference where set_id = %s and topping in (%s)"

#Create a new friendship between two users
#params: username of friend1, username of friend2
#inserts a new row in the Friends table. Be sure to run this twice, once for each orientation
new_friends = "insert into Friends values (%s, %s)"

# Remove friendship between two users
# params: username of friend1, username of friend2
# removes a row in the Friends table involving those two users
# run in both directions
remove_friends = "delete from Friends where friend1 = %s and friend2 = %s"

#Get all of the friends of a given user
#params: username
#returns all the users that this user is friends with
get_friends = "select friend2 from Friends where friend1 = %s"

#Calculates the number of orders for a user
#params: username
#returns the number of orders the user has been a part of
get_order_count = "select count(order_id) from Order_Details where user = %s"

#Calculates the user's top toppings
#params: username
#returns a list of toppings ordered by their frequency, and the number of orders they appear in
get_favorite_toppings = "select topping, count(order_id) as frequency from Order_Details where user = %s " \
                        "group by topping order by frequency"

#Calculates the user's best friend
#params: username
#returns a list of people they have ordered a pizza with and the number of orders with that person
get_best_friend = "select count(o1.order_id) as frequency " \
                  "from Order_Details o1 " \
                  "join Order_Details o2 on o1.order_id = o2.order_id " \
                  "where o1.user = %s and o2.user <> o1.user " \
                  "group by o2.user order by frequency"

#Updates a preference
#params: dict containing set_id, topping, and score
#Call this on each preference when a set is updated
update_preference = "insert into Preference values (%(topping)s, %(set_id)s, %(score)s) " \
                    "on duplicate key update score = %(score)s where topping = %(topping)s and set_id = %(set_id)s"

# Deselects the current preference set of a user
# params: username
deselect_current_set = "update Preference_Set set is_active = 0 where user = %s and is_active = 1"

# Activates a preference set of a user, specified by title
# params: username, title
activate_preference_set = "update Preference_Set set is_active = 1 where user = %s and title = %s"

#updates a preference set
#params: title, is_active (1/0), id
update_preference_set = "update Preference_Set set title = %s, is_active = %s where id = %s"

#creates a new preference set
#params: username, title, is_active (1/0)
new_preference_set = "insert into Preference_Set (user, title, is_active) values (%s, %s, %s)"

#gets the ID of a preference set
#params: username, title
#returns the set_id of the matching preference_set
get_preference_set_id = "select id from Preference_Set where user = %s and title = %s"

#gets the number of preference sets defined by a user
#params: username
#returns the number of preference sets owned by this user
get_set_count = "select count(id) as count from Preference_Set where user = %s group by user"

#creates a new preference inside a set
#params: topping, set_id, score
new_preference = "insert into Preference values (%s, %s, %s)"

#gets all the toppings
#params: none
#returns a list of toppings
get_toppings = "select * from Topping"

#deletes a preference set
#params: set_id
#only deletes the set, must delete all preferences first
delete_preference_set = "delete from Preference_Set where id = %s"

#deletes all preferences from a given set
#params: set_id
#run this before you delete the preference set
delete_preference = "delete from Preference where set_id = %s"

#checks for an allergy
#params: username, topping
#returns 1 if the user has this allergy, 0 else
check_allergy = "select case when exists " \
                "(select topping from Allergy where user = %s and topping = %s) " \
                "then 1 else 0 end"

#creates a new allergy for a user
#params: username, topping
new_allergy = "insert into Allergy values (%s, %s)"

#deletes an allergy for a user
#params: username, topping
delete_allergy = "delete from Allergy where user = %s and topping = %s"
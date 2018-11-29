def format_list(list):
    """Accepts a list and returns a format string that you can use
    as a parameter for any query that accepts a list as a parameter."""
    return ','.join(['%s'] * len(list))

#Create a user
#params: username and password of new user. Password is not encrypted in any way.
new_user = "insert into User values (%s, %s)"

#validate a user
#params: username and password to validate.
#returns 1 if the password is correct, 0 otherwise
validate_user = "select count(1) from User where username = %s and password = %s"

#Get all preference sets for a given user
#params: username
#returns all preference sets that are associated with username
get_preference_sets = "select * from Preference_set where user = %s"

#Get the preferences that make up a set
#params: ID of the preference set
#returns all toppings and scores for the preference
get_preferences = "select topping, score from Preference where set_id = %s"

#Get the allergies for a user
#params: username
#returns a list of all allergies that are associated with username
get_allergies = "select topping from Allergy where user = %s"

#Get all toppings that should be considered when creating a pizza
#params: list of usernames, same list of usernames
#returns a list of toppings such that each topping is desired by at least 1 user
# and no user is allergic to any topping.
get_valid_toppings = "select distinct p.topping " \
                     "from Preference_Set ps " \
                     "inner join Preference p on p.set_id = ps.id " \
                     "where ps.user in (%s) and ps.is_active = 1 and p.topping not in " \
                          "(select distinct topping from Allergy where user in (%s)"

#Get the score for toppings in a preference set
#params: Preference set ID, list of toppings
#returns the topping and the score of that topping
get_topping_scores = "select topping, score from Preference where set_id = %s and topping in (%s)"

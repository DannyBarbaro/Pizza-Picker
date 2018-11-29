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
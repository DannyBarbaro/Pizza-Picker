#Create a user
#params: username and password of new user. Password is not encrypted in any way.
new_user = "insert into User values (%s, %s)"

#validate a user
#params: username and password to validate.
#returns 1 if the password is correct, 0 otherwise
validate_user = "select count(1) from User where username = %s and password = %s"
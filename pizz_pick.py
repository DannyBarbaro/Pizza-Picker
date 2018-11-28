import configparser
import pymysql
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

# routing user to different pages
@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/login')
def login_page():
    return render_template('login_page.html')

@app.route('/<username>/preferences')
def prefs_page(username):
    return render_template('prefs_page.html')

@app.route('/<username>/profile')
def profile_page(username):
    return render_template('profile_page.html')

@app.route('/<username>/allergies')
def allergies_page(username):
    return render_template('allergies_page.html')

@app.route('/<username>/friends')
def friends_page():
    return render_template('friends_page.html')

@app.route('/order')
def order_page():
    return render_template('order_page.html')


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

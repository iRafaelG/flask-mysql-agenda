from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQl connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

@app.route('/')
def home():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM contacts')
    data = cursor.fetchall()

    return render_template('index.html', contacts = data)

@app.route('/add', methods=['POST'])
def addContact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO contacts (fullname, phone, email)VALUE (%s, %s, %s)', (fullname, phone,  email))
        mysql.connection.commit()

        flash('Contact added successfully')

        return redirect(url_for('home'))

@app.route('/edit/<string:id>')
def editContact(id):

    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT *
        FROM contacts
        WHERE id = %s
    """, (id,))
    data = cursor.fetchall()[0]

    return render_template('edit.html', contact = data)

@app.route('/update/<string:id>', methods=['POST'])
def updateContact(id):

    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE contacts
            SET fullname = %s,
                phone = %s,
                email = %s
            WHERE id = %s
        """, (fullname, phone, email, id))
        mysql.connection.commit()
    
    flash('Contact updated successfully')

    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def deleteContact(id):

    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM contacts WHERE id = %s', (id,))
    mysql.connection.commit()

    flash('Contacts removed successfully')

    return redirect(url_for('home'))

if(__name__ == '__main__'):
    app.run(port = 3000, debug=True)
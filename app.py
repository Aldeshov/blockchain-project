import sqlite3
from datetime import datetime

import requests
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)


def get_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/<int:order_id>')
def fetch(order_id):
    conn = get_connection()
    _order = conn.execute("SELECT * FROM orders WHERE id=(?)", (order_id,)).fetchall()[0]
    content = requests.get('https://blockchain-project-1-remote.herokuapp.com',
                           {"status": _order['status']}).content.decode()
    conn.execute("UPDATE OR ABORT orders SET status = (?) WHERE id=(?)", (content, _order['id'],))
    if content == "delivered":
        now = datetime.now()
        conn.execute("UPDATE OR ABORT orders SET delivery_date = (?) WHERE id=(?)",
                     (now.strftime("%d/%m/%Y %H:%M:%S"), _order['id'],))
    conn.commit()
    conn.close()
    return redirect(url_for('status'))


@app.route('/order', methods=('GET', 'POST'))
def order():
    if request.method == 'POST':
        _name = request.form['name']
        _type = request.form['type']
        _weight = request.form['weight']
        _number = request.form['number']
        _departure_date = request.form['departure_date']
        _message = request.form['message']

        conn = get_connection()
        conn.execute("INSERT INTO orders (profile_id, name, message, type, weight, number, "
                     "departure_date, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                     (1, _name, _message, _type, _weight, _number, _departure_date, 'pending'))
        conn.commit()
        conn.close()
        return redirect(url_for('status'))
    conn = get_connection()
    profiles = conn.execute('SELECT * FROM profile WHERE id=1').fetchall()
    return render_template('order.html', profile=profiles[0])


@app.route('/status')
def status():
    conn = get_connection()
    profiles = conn.execute('SELECT * FROM profile WHERE id=1').fetchall()
    statistics = conn.execute("SELECT * FROM statistics WHERE id=(?)", (profiles[0]['statistics_id'],)).fetchall()
    orders = conn.execute("SELECT * FROM orders WHERE profile_id=(?)", (profiles[0]['id'],)).fetchall()
    conn.close()
    delivered = 0
    pending = 0
    for o in orders:
        if o['status'] == 'delivered':
            delivered += 1 / len(orders) * 100
        if o['status'] == 'pending':
            pending += 1
    return render_template('status.html',
                           profile=profiles[0],
                           statistics=statistics[0],
                           orders=orders,
                           delivered=int(delivered),
                           pending=pending)


@app.route('/')
def index():
    return redirect(url_for('status'))


if __name__ == '__main__':
    app.run()

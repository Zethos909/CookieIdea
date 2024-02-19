from flask_app import app
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_cookies import Cookies
from flask_app.models.models_users import User

@app.route('/')
def index():
    return redirect('/cookie_order_list')

@app.route('/cookie_order_list')
def order_list():
    orders = User.get_all_orders()
    print(f"Orders: {orders}")
    for user in orders:
        print(f"User data: {user.__dict__}")
    return render_template('cookie_order_list.html', orders=orders)

@app.route('/new_order')
def new_order_form():
    return render_template('new_order.html')

@app.route('/edit_order/<int:order_id>')
def edit_order_form(order_id):
    order = Cookies.get_order_by_id(order_id)
    if order:
        return render_template('edit_order.html', order=order)
    else:
        return render_template('order_not_found.html')

@app.route('/update_order/<int:order_id>', methods=['POST'])
def update_order(order_id):
    order = Cookies.get_order_by_id(order_id)
    if not order:
        return render_template('order_not_found.html')
    cookie_type = request.form['cookie_type']
    quantity = request.form['quantity']
    if len(cookie_type) < 2:
        flash('Cookie type must be at least 2 characters')
    if not quantity.isdigit() or int(quantity) <= 0:
        flash('Quantity must be a positive number')
    if '_flashes' in session:
        return redirect(url_for('edit_order_form', order_id=order_id))
    Cookies.update_order(order_id, cookie_type, quantity)
    flash('Order updated successfully!')
    return redirect('/cookie_order_list')

@app.route('/place_order', methods=['POST'])
def place_order():
    user_name = request.form['user_name']
    cookie_type = request.form['cookie_type']
    quantity = request.form['quantity']
    if not user_name:
        flash('User name is required', 'user_name_error')
    if not cookie_type:
        flash('Cookie type is required', 'cookie_type_error')
    if not quantity:
        flash('Quantity is required', 'quantity_error')
    if '_flashes' not in session:
        if len(user_name) < 2:
            flash('Name must be at least 2 characters', 'name_error')
        if len(cookie_type) < 2:
            flash('Cookie type must be at least 2 characters', 'cookie_type_error')
        try:
            quantity = int(quantity)
            if quantity <= 0:
                flash('Quantity must be a positive number', 'quantity_error')
        except ValueError:
            flash('Quantity must be a valid number', 'quantity_error')
    if '_flashes' in session:
        return redirect('/new_order')
    user = User.get_user_by_name(user_name)
    if user:
        user_id = user.id
    else:
        user_id = User.create_user(user_name)
    Cookies.create_cookie_order(user_id, cookie_type, quantity)
    return redirect('/cookie_order_list')





from flask import render_template, session, redirect, request, url_for, flash
from werkzeug import datastructures


from shop import app, db, bcrypt
from .models import User
from .forms import RegistrationForm, LoginForm
from shop.products.models import Addproduct, Category, Brand
import os


# Lấy toàn bộ sản phẩm
@app.route('/admin')
def admin():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
        return redirect(url_for('login'))
    products = Addproduct.query.order_by(Addproduct.id.desc()).all()
    return render_template('admin/productmanager.html', title="Admin page", products=products)

# Lấy toàn bộ nhãn hiệu
@app.route('/brands')
def brands():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/itemmanager.html', title='brands',brands=brands, name_manager="Brands", name_list="List of brands")

# Lấy toàn bộ thể loại
@app.route('/categories')
def categories():
    if 'email' not in session:
        flash(f'Please login first', 'danger')
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/itemmanager.html', title='categories',categories=categories)

# Đăng ký Admin
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        user = User(name= form.name.data,username= form.username.data,email= form.email.data,
                    password = hash_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.name.data}, Thanks you for registering', 'success')
        return redirect(url_for('login'))
    return render_template('admin/register.html', form=form, title="Register Admin page")

# Đăng nhập Admin
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {form.email.data} You are logedin now', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Wrong Password or Email, please try again', 'danger')
    return render_template('admin/login.html', form=form, title="Login Admin page")

# Đăng xuất Admin
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))
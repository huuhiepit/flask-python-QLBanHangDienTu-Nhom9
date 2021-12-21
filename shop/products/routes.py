from flask import redirect, render_template, url_for, flash, request, session, current_app

from shop import db, app, photos, search
from .models import Brand, Category, Addproduct
from .forms import Addproducts
import secrets
from flask_msearch import Search
import os


# Hàm lấy toàn bộ nhãn hiệu
def brands():
    brands = Brand.query.join(Addproduct, (Brand.id == Addproduct.brand_id)).all()
    return brands
# Hàm lấy toàn bộ thể loại
def categories():
    categories = Category.query.join(Addproduct,(Category.id == Addproduct.category_id)).all()
    return categories

#Trang chủ
@app.route('/')
def home():
    products = Addproduct.query.filter( Addproduct.stock > 0).order_by(Addproduct.id.desc())
    return render_template('customer/index.html', products=products, brands=brands(), categories=categories())

@app.route('/brand/<int:id>')
def get_brand(id):
    get_brand_prod = Addproduct.query.filter_by(brand_id=id)
    return render_template('customer/index.html', get_brand_prod=get_brand_prod, brands=brands(), categories=categories())

@app.route('/category/<int:id>')
def get_category(id):
    get_cat_prod = Addproduct.query.filter_by(category_id=id)
    return render_template('customer/index.html', get_cat_prod=get_cat_prod , categories=categories(), brands=brands())

@app.route('/search')
def search():
    searchword = request.args.get('key')
    products = Addproduct.query.msearch(searchword, fields=['name'], limit=30)
    return render_template('customer/search.html', products=products, brands=brands(), categories=categories())

# Thêm một nhãn hiệu
@app.route('/addbrand', methods=['GET','POST'])
def addbrand():
    if request.method=="POST":
        getbrand = request.form.get('brand')
        brand = Brand(name= getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'The Brand {getbrand} was added to your database', 'success')
        return redirect(url_for('addbrand'))
    return render_template('admin/addbrand.html', brands='brands')

# Chỉnh sửa nhãn hiệu
@app.route('/updatebrand/<int:id>',methods=['GET','POST'])
def updatebrand(id):
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method =="POST":
        updatebrand.name = brand
        flash(f'The brand {updatebrand.name} was changed to {brand}','success')
        db.session.commit()
        return redirect(url_for('brands'))
    brand = updatebrand.name
    return render_template('admin/addbrand.html', title='Udate brand',brands='brands',updatebrand=updatebrand, brand=brand)

# Xóa một nhãn hiệu

@app.route('/deletebrand/<int:id>', methods=['GET','POST'])
def deletebrand(id):
    brand = Brand.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(brand)
        flash(f"The brand {brand.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('brands'))
    flash(f"The brand {brand.name} can't be  deleted from your database","warning")
    return redirect(url_for('brands'))


# Thêm một thể loại
@app.route('/addcat', methods=['GET','POST'])
def addcat():
    if request.method=="POST":
        getcat = request.form.get('category')
        cat = Category(name= getcat)
        db.session.add(cat)
        db.session.commit()
        flash(f'The Category {getcat} was added to your database', 'success')
        return redirect(url_for('addcat'))
    return render_template('admin/addbrand.html')

# Chỉnh sửa một thể loại
@app.route('/updatecat/<int:id>',methods=['GET','POST'])
def updatecat(id):
    updatecat = Category.query.get_or_404(id)
    category = request.form.get('category')  
    if request.method =="POST":
        updatecat.name = category
        flash(f'The category {updatecat.name} was changed to {category}','success')
        db.session.commit()
        return redirect(url_for('categories'))
    category = updatecat.name
    return render_template('admin/addbrand.html', title='Update cat',updatecat=updatecat, category=category)

# Xóa một thể loại
@app.route('/deletecat/<int:id>', methods=['GET','POST'])
def deletecat(id):
    category = Category.query.get_or_404(id)
    if request.method=="POST":
        db.session.delete(category)
        flash(f"The brand {category.name} was deleted from your database","success")
        db.session.commit()
        return redirect(url_for('categories'))
    flash(f"The brand {category.name} can't be  deleted from your database","warning")
    return redirect(url_for('categories'))


# Thêm một sản phẩm
@app.route('/addproduct', methods=['POST', 'GET'])
def addproduct():
    brands = Brand.query.all()
    categories = Category.query.all()
    form = Addproducts(request.form)
    if request.method =="POST":
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        desc = form.discription.data
        brand = request.form.get('brand')
        category = request.form.get('category')
        
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
        
        addproduct = Addproduct(name=name,price=price,discount=discount,stock=stock,colors=colors,desc=desc,category_id=category,brand_id=brand,image_1=image_1,image_2=image_2,image_3=image_3)
        db.session.add(addproduct)
        flash(f'The product {name} was added in database','success')
        db.session.commit()
        return redirect(url_for('addproduct'))

    return render_template('admin/addproduct.html', form=form, title="Add product page", brands=brands, categories=categories)

# Chỉnh sửa sản phẩm
@app.route('/updateproduct/<int:id>', methods=['GET','POST'])
def updateproduct(id):
    form = Addproducts(request.form)
    product = Addproduct.query.get_or_404(id)
    brands = Brand.query.all()
    categories = Category.query.all()
    brand = request.form.get('brand')
    category = request.form.get('category')
    if request.method =="POST":
        product.name = form.name.data 
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data 
        product.colors = form.colors.data
        product.desc = form.discription.data
        product.category_id = category
        product.brand_id = brand
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
            except:
                product.image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + ".")
        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")
            except:
                product.image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + ".")

        flash('The product was updated','success')
        db.session.commit()
        return redirect(url_for('admin'))
    form.name.data = product.name
    form.price.data = product.price
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors
    form.discription.data = product.desc
    brand = product.brand.name
    category = product.category.name
    return render_template('admin/addproduct.html', form=form, title='Update Product',getproduct=product, brands=brands,categories=categories)

# Xóa một sản phẩm
@app.route('/deleteproduct/<int:id>', methods=['POST'])
def deleteproduct(id):
    product = Addproduct.query.get_or_404(id)
    if request.method =="POST":
        try:
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_1))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_2))
            os.unlink(os.path.join(current_app.root_path, "static/images/" + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'The product {product.name} was delete from your record','success')
        return redirect(url_for('admin'))
    flash(f'Can not delete the product','success')
    return redirect(url_for('admin'))
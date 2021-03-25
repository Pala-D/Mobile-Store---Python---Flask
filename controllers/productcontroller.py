from flask import Blueprint, redirect, render_template, request
from models.product import Product
from models.category import Category
from models.brand import Brand
product = Blueprint('product',__name__)

@product.before_request
def checkSignin():
    print('path', request.path)
    print('endpoint', request.endpoint)
    print('url', request.url)
    print('method', request.method)
    if request.cookies.get('session') == None:
        return redirect(f'/authen/signin?returl={request.path}')

@product.route('/product')
def index():
    pro = Product()
    arr = pro.getProducts()
    return render_template('/product/index.html', arr = arr)

@product.route('/product/add')
def add():
    cat = Category()
    br = Brand()
    return render_template('/product/add.html', brr = br.getBrands(), crr = cat.getCategories())

@product.route('/product/add', methods=["post"])
def doAdd():
    f = request.files.get("f")
    f.save("static/image/" + f.filename)
    name = request.form.get("name")
    cat = request.form.get("cat")
    brand = request.form.get("brand")
    price = request.form.get("price")
    des = request.form.get("des")
    qty = request.form.get("qty")
    a = (name, brand, cat, price, f.filename, qty, des)
    pro = Product()
    ret = pro.add(a)
    if ret > 0:
        return redirect("/product")
    return "Failed"

@product.route('/product/edit/<id>')
def edit(id):
    cat = Category()
    brand = Brand()
    pro = Product()
    return render_template('/product/edit.html', crr = cat.getCategories(), brr = brand.getBrands(), u = pro.getProductById(id))

@product.route('/product/edit/<id>', methods=["post"])
def doEdit(id):
    img = request.form.get("img")
    f = request.files.get("f")
    if f:
        f.save("static/image/"+f.filename)
        img = f.filename
    cat = request.form.get("cat")
    brand = request.form.get("brand")
    name = request.form.get("name")
    price = request.form.get("price")
    des = request.form.get("des")
    qty = request.form.get("qty")
    a = (name, brand, cat, price, img, qty, des, id)
    pro = Product()
    ret = pro.edit(a)
    if ret > 0:
        return redirect('/product')
    return "Failed"

@product.route("/product/delete/<id>")
def delete(id):
    pro = Product()
    pro.delete(id)
    return redirect('/product')




from flask import Blueprint, render_template, redirect, request
from models.category import Category
from models.brand import Brand
from models.product import Product
from math import ceil
home = Blueprint('home', __name__)

@home.route('/')
@home.route('/<int:p>')
def index(p=1):
    cat = Category()
    brand = Brand()
    pro = Product()
    a = pro.getProductsForHome(p, 8)
    b = brand.getBrands()
    c = cat.getCategories()
    total = pro.homeCount()
    n = ceil(total / 8)
    return render_template('home/index.html', arr = a, crr = c, brr = b, title = "Mobile Store", n = n)

@home.route('/home/category/<int:id>')
def category(id):
    cat = Category()
    brand = Brand()
    pro = Product()
    a = pro.getProductsByCategory(id)
    b = brand.getBrands()
    c = cat.getCategories()
    d = cat.getCategoryById(id)
    return render_template('home/category.html', arr = a, crr = c, brr = b, title = d[1])

@home.route('/home/brand/<int:id>')
def brand(id):
    cat = Category()
    brand = Brand()
    pro = Product()
    a = pro.getProductsByBrand(id)
    b = brand.getBrands()
    c = cat.getCategories()
    d = brand.getBrandById(id)
    return render_template('home/brand.html', arr = a, crr = c, brr = b, title = d[1])

@home.route('/home/detail/<int:id>')
def detail(id):
    cat = Category()
    brand = Brand()
    pro = Product()
    a = pro.getProductById(id)
    b = brand.getBrands()
    c = cat.getCategories()
    d = pro.getProductsRelation(id)
    return render_template('home/detail.html', u = a, crr = c, brr = b, arr = d)

@home.route('/home/search')
@home.route('/home/search/<int:p>')
def search(p=1):
    q = request.args.get('q')
    cat = Category()
    brand = Brand()
    pro = Product()
    a = pro.searchProducts(q, p, 4)
    b = brand.getBrands()
    c = cat.getCategories()
    total = pro.searchCount(q)
    n = ceil(total / 4)
    return render_template('home/search.html', arr = a, crr = c, brr = b, title = q, n = n)


    
from flask import Blueprint, render_template, redirect, request, make_response
from models.cart import Cart
from util import randomString
from models.invoice import Invoice
cart = Blueprint('cart', __name__)

@cart.route('/cart/add', methods=["post"])
def add():
    cart = Cart()
    id = request.cookies.get('cart')
    if id == None:
        id = randomString(16)
        response = make_response(redirect('/cart'))
        response.set_cookie('cart', id, max_age= 3600 * 24 * 30)
    else:
        response = redirect('/cart')
    productid = request.form.get('productid')
    quantity = request.form.get('quantity')
    cart.add((id, productid, quantity))
    return response

@cart.route('/cart')
def index():
    id = request.cookies.get('cart')
    if id != None:
        cart = Cart()
        a = cart.getCarts(id)
        sum = 0
        b = []
        for i in a:
            b.append(i[2]*i[4])
        for u in b:
            sum += u
        return render_template('cart/index.html', arr = a, sum = sum)
    return redirect("/")

@cart.route('/cart/delete', methods=['post'])
def delete():
    productid = request.form.get('pid')
    cartid = request.cookies.get('cart')
    cart = Cart()
    cart.delete((cartid, productid))
    return redirect("/cart")

@cart.route('/cart/edit', methods=['post'])
def edit():
    productid = request.form.get('pid')
    cartid = request.cookies.get('cart')
    quantity = request.form.get('qty')
    cart = Cart()
    ret = cart.edit((quantity, cartid, productid))
    return str(ret)

@cart.route("/cart/checkout")
def checkout():
    return render_template("cart/checkout.html")

@cart.route("/cart/checkout", methods=['post'])
def doCheckout():
    invoice = Invoice()
    cartid = request.cookies.get('cart')
    fullname = request.form.get('fullname')
    address = request.form.get('address')
    phone = request.form.get('phone')
    email = request.form.get('email')
    invoice.add((cartid, fullname, address, phone, email))
    return redirect('/cart/success/'+ cartid)

@cart.route('/cart/success/<id>')
def success(id):
    return render_template('cart/success.html')

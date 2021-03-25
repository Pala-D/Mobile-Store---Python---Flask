from flask import Blueprint, render_template, request, redirect, jsonify
from models.brand import Brand
from random import randint
brand = Blueprint('brand', __name__)

@brand.before_request
def checkSignin():
    print('path', request.path)
    print('endpoint', request.endpoint)
    print('url', request.url)
    print('method', request.method)
    if request.cookies.get('session') == None:
        return redirect(f'/authen/signin?returl={request.path}')

@brand.route('/brand')
def index():
    brand = Brand()
    brr = brand.getBrands()
    return render_template('brand/index.html', brr = brr)

@brand.route('/brand/delete/<id>')
def delete(id):
    brand = Brand()
    ret = brand.delete(id)
    if ret > 0:
        return redirect("/brand")
    return "Failed"

@brand.route('/brand/delall', methods=["post"])
def delall():
    a = request.form.getlist('a')
    brand = Brand()
    b = []
    for i in a:
        b.append((i, ))
    ret = brand.deletes(b)
    return redirect('/brand')

@brand.route('/brand/edit/<id>')
def edit(id):
    brand = Brand()
    i = brand.getBrandById(id)
    return render_template('brand/edit.html', i = i)

@brand.route('/brand/edit/<id>', methods=['post'])
def doEdit(id):
    brand = Brand()
    a = (request.form.get('name'), id)
    ret = brand.edit(a)
    if ret > 0:
        return redirect('/brand')
    return "Failed"


@brand.route("/brand/add", methods=["post"])
def add():
    brand = Brand()
    id = randint(0,999999)
    name = request.form.get("name")
    ret = brand.add((id, name))
    if ret > 0:
        return jsonify({"id": id, "name": name})
    return "Failed"

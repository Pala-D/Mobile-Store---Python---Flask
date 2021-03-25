from flask import Blueprint, render_template, request, redirect, jsonify
from models.category import Category
from random import randint
category = Blueprint('category', __name__)

@category.before_request
def checkSignin():
    print('path', request.path)
    print('endpoint', request.endpoint)
    print('url', request.url)
    print('method', request.method)
    if request.cookies.get('session') == None:
        return redirect(f'/authen/signin?returl={request.path}')

@category.route('/category')
def index():
    cat = Category()
    arr = cat.getCategories()
    return render_template('category/index.html', arr = arr)

@category.route('/category/delete/<id>')
def delete(id):
    cat = Category()
    ret = cat.delete(id)
    if ret > 0:
        return redirect("/category")
    return "Failed"

@category.route('/category/delall', methods=["post"])
def delall():
    a = request.form.getlist('a')
    cat = Category()
    b = []
    for i in a:
        b.append((i, ))
    ret = cat.deletes(b)
    return redirect('/category')

@category.route('/category/edit/<id>')
def edit(id):
    cat = Category()
    i = cat.getCategoryById(id)
    return render_template('category/edit.html', i = i)

@category.route('/category/edit/<id>', methods=['post'])
def doEdit(id):
    cat = Category()
    a = (request.form.get('name'), id)
    ret = cat.edit(a)
    if ret > 0:
        return redirect('/category')
    return "Failed"


@category.route("/category/add", methods=["post"])
def add():
    cat = Category()
    id = randint(0,999999)
    name = request.form.get("name")
    ret = cat.add((id, name))
    if ret > 0:
        return jsonify({"id": id, "name": name})
    return "Failed"

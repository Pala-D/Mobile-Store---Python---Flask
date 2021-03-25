from flask import Blueprint, render_template, redirect, request, jsonify
from models.role import Role
from random import randint
role = Blueprint('role',__name__)

@role.before_request
def checkSignin():
    print('path', request.path)
    print('endpoint', request.endpoint)
    print('url', request.url)
    print('method', request.method)
    if request.cookies.get('session') == None:
        return redirect(f'/authen/signin?returl={request.path}')

@role.route("/role")
def index():
    ro = Role()
    return render_template("role/index.html", arr = ro.getRoles())


@role.route("/role/create", methods=["post"])
def create():
    ro = Role()
    id = randint(0,999999)
    name = request.form.get("name")
    if ro.add((id, name)) > 0:
        return jsonify({"id": id, "name": name})
    return "Failed"

@role.route("/role/edit/<id>")
def edit(id):
    ro = Role()
    a = ro.getRoleById(id)
    return render_template('role/edit.html', a = a)

@role.route('/role/edit/<id>', methods=['post'])
def doEdit(id):
    ro = Role()
    a = (request.form.get('name'), id)
    ret = ro.edit(a)
    if ret > 0:
        return redirect('/role')
    return "Failed"

@role.route("/role/delete/<id>")
def delete(id):
    ro = Role()
    a = ro.delete(id)
    return redirect("/role")

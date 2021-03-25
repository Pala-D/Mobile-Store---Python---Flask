from flask import Blueprint, redirect, request, render_template, make_response
from util import randomString
from models.session import Session
from models.account import Account
from models.role import Role
from hashlib import md5
authen = Blueprint('authen',__name__)

@authen.route("/authen")
def index():
    if request.cookies.get("session"):
        acc = Account()
        v = acc.getAccountIdBySession(request.cookies.get('session'))
        accid = v['id']
        ro = Role()
        u = ro.getRoleByAccountId(accid)
        return render_template("authen/index.html", v = v, u = u)
    return redirect("/authen/signin")

@authen.route("/authen/signin")
def signin():
    return render_template("authen/signin.html")

@authen.route("/authen/signin", methods=["post"])
def doSignin():
    usr = request.form.get('usr')
    pwd = request.form.get('pwd') + '#$%^&*$@' + usr
    rem = request.form.get('rem')
    pwd = md5(pwd.encode())
    acc = Account()
    v = acc.getAccount((usr, pwd.digest()))
    if v:
        res = make_response(redirect("/authen"))
        token = randomString(32)
        ses = Session()
        ret = ses.add((token, v['id']))
        if rem == "1":
            res.set_cookie("session", token, max_age = 30*3600*24)
        else:
            res.set_cookie("session", token)
        return res
    else:
        return render_template('authen/signin.html', err = "Log In Failed")

@authen.route("/authen/signout", methods=["post"])
def signout():
    if request.cookies.get('session'):
        ses = Session()
        ses.delete(request.cookies.get("session"))
        res = make_response(redirect("/authen/signin"))
        res.set_cookie("session", "", max_age = -1)
        return res
    return redirect("/authen/signin")

@authen.route('/authen/signup')    
def signup():
    return render_template("authen/signup.html")

@authen.route("/authen/signup",methods=['post'])
def doSignup():
    id = randomString(16)
    usr = request.form.get("usr")
    pwd = request.form.get("pwd") + '#$%^&*$@' + usr
    eml = request.form.get("eml")
    pwd = md5(pwd.encode())
    acc = Account()
    ret = acc.add( (id, usr, pwd.digest(), eml))
    if ret > 0:
        return redirect("/authen/signin")
    return render_template("authen/signup.html", err = "Username Existed")

@authen.route("/authen/editpassword/<id>")
def editPassword(id):
    acc = Account()
    a = acc.getAccountById(id)
    return render_template("authen/edit.html", a = a)

@authen.route("/authen/editpassword/<id>", methods=['post'])
def doEditPassword(id):
    acc = Account()
    v = acc.getAccountById(id)
    usr = v['usr']
    newpwd = request.form.get("pwd") + '#$%^&*$@' + usr
    newpwd = md5(newpwd.encode())
    a = (newpwd.digest(), id)
    ret = acc.editPassword(a)
    if ret > 0:
        if request.cookies.get('session'):
            ses = Session()
            ses.delete(request.cookies.get("session"))
            res = make_response(redirect("/authen/signin"))
            res.set_cookie("session", "", max_age = -1)
            return res
    return "Failed"

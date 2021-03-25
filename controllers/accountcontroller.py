from flask import Blueprint, redirect, request, render_template, jsonify
from models.account import Account
from models.accountinrole import AccountInRole
from models.role import Role
account = Blueprint('account',__name__)

@account.before_request
def checkSignin():
    print('path', request.path)
    print('endpoint', request.endpoint)
    print('url', request.url)
    print('method', request.method)
    if request.cookies.get('session') == None:
        return redirect(f'/authen/signin?returl={request.path}')

@account.route("/account")
def index():
    acc = Account()
    ro = Role()
    return render_template("/account/index.html", arr = acc.getAccounts(), brr = ro.getRoles())

@account.route('/account/addrole', methods=["post"])
def addRole():
    accountir = AccountInRole()
    accountid = request.form.get('accountid')
    roleid = request.form.get('roleid')
    return str(accountir.add((accountid,roleid)))

@account.route("/account/json/<id>")
def json(id):
    air = AccountInRole()
    a = air.getRoleByAccount(id)
    dic = {}
    for v in a:
        dic[v[0]] = 1
    return jsonify(dic)
    
@account.route('/account/role/<id>')
def role(id):
    acc = Account()
    ro = Role()
    air = AccountInRole()
    b = air.getRoleByAccount(id)
    li = []
    for v in b:
        li.append(v[0])
    return render_template('account/role.html', a = acc.getAccountById(id), arr = ro.getRoles(), brr = li)




    
from flask import Flask
from controllers.accountcontroller import account
from controllers.rolecontroller import role
from controllers.productcontroller import product
from controllers.authencontroller import authen
from controllers.brandcontroller import brand
from controllers.homecontroller import home
from controllers.cartcontroller import cart
from controllers.categorycontroller import category
from controllers.chartcontroller import chart

app = Flask(__name__, static_url_path= "/", template_folder= "views")
app.secret_key = "123456"
app.register_blueprint(account)
app.register_blueprint(role)
app.register_blueprint(product)
app.register_blueprint(authen)
app.register_blueprint(brand)
app.register_blueprint(home)
app.register_blueprint(category)
app.register_blueprint(cart)
app.register_blueprint(chart)


@app.template_filter()
def currency(value):
    return '{0:,.0f}'.format(value)

def recursion(s, dict, k):
    if k in dict:
        parseTree(s, dict, dict[k])

def parseTree(s, dict, li):
    s.append('<ul>')    
    for v in li:
        s.append('<li>')
        s.append(f'<a href="">{v[1]}</a>')
        recursion(s, dict, v[0])
        s.append('</li>')
    s.append('</ul>')

@app.template_filter()
def buildTree(arr):
    li = arr[0]
    dict = arr[1]
    s = []
    parseTree(s, dict, li)
    return ''.join(s)

app.run(debug=True) 
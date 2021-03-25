from flask import Blueprint, render_template, redirect, make_response, request
from models.category import Category
from models.brand import Brand
chart = Blueprint('chart', __name__)

@chart.route('/chart')
def index():
    return render_template("chart/index.html")


@chart.route('/chart/category')
def catchart():
    cat = Category()
    return render_template("chart/categorychart.html", a = cat.statisticCategory())

@chart.route('/chart/brand')
def brandchart():
    brand = Brand()
    return render_template("chart/brandchart.html", a = brand.statisticBrand())
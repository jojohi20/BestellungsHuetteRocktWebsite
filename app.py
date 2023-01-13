from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy, query

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.Integer, nullable=False)
    owner = db.Column(db.String(32), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    time = db.Column(db.DateTime, default=datetime.now)


stores = {
    # "key": "name"
    "c8753ae80e5093d3293765e93405acb5": "Stand  1",
    "c8753ae80e5093d3293765e93405acb6": "Stand  2",

}


class Product:
    def __init__(self, name, id):
        self.name = name
        self.id = id


products = []
products.append(Product("Apfel", 1))
products.append(Product("Banane", 2))


@app.route("/", methods=['GET'])
def index():
    orders = Order.query.order_by(Order.id).all()
    return render_template("index.html", tasks=orders)


def createOrder(key, form):
    print(key)
    id = form["id"]
    amount = form["amount"]

    newOrder = Order(item=id, amount=amount, owner=key)
    try:

        db.session.add(newOrder)
        db.session.commit()
        print(key)
        return redirect("/list?key=" + key)
    except:
        return "Failed to create Task"


@app.route("/list", methods=['POST', 'GET'])
def product_list():
    key = request.args.get("key")
    print(key)
    if not key in stores:
        return "Ungültiger Schlüssel"

    if request.method == 'POST':
        return createOrder(key, request.form)

    else:
        return render_template("productlist.html", products=products, store=stores[key])


@app.route("/delete/<int:id>")
def delete(id):
    del_task = Order.query.get_or_404(id)

    try:
        db.session.delete(del_task)
        db.session.commit()

    except:
        print("Error deleting Task")
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)

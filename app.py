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
    done = db.Column(db.Boolean, default=False)
    canceled = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Created Order with id: {self.id}"


class Product:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class DisplayOrder:
    def __init__(self, id, amount, itemName, store,displaytime):
        self.id = id
        self.amount = amount
        self.itemName = itemName
        self.store = store
        self.displayTime = displaytime


products = []
products.append(Product("Apfel", 1))
products.append(Product("Banane", 2))

stores = ["Blau", "Rot", "Grün"]


def get_product_with_id(id):
    for p in products:
        if p.id == id:
            return p

#sortiert die Betellungen nach erledigt und unerledigt und ändert Order zu DisplayOrder
def transform_orders_to_display(orders):
    displayOrders = []
    for order in orders:
        if order.done or order.canceled:
            continue

        itemName = get_product_with_id(order.item).name
        displayTime = order.time.strftime("%H:%M")
        displayOrder = DisplayOrder(order.id, order.amount, itemName, order.owner, displayTime)
        displayOrders.append(displayOrder)
    return displayOrders

@app.route("/", methods=['GET'])
def index():

    orders = Order.query.order_by(Order.id).all()

    displayOrders = transform_orders_to_display(orders)

    return render_template("index.html", orders=displayOrders)

# Liste aller Bestellungen
@app.route("/all", methods=['GET'])
def all_list():
    orders = Order.query.order_by(Order.id).all()
    return render_template("allorders.html", orders=orders)




def add_order(form, store):
    id = form["id"]
    amount = form["amount"]
    newOrder = Order(item=id, amount=amount, owner=store)
    try:
        db.session.add(newOrder)
        db.session.commit()
        return redirect("/order?store=" + store)
    except:
        return "Failed to create Task"


# Bestellungs Ansicht
@app.route("/order", methods=['POST', 'GET'])
def product_order():
    #mit ?store= werden die Stände identifziert
    store = request.args.get("store")
    if not store in stores:
        return "Ungültiger Stand"

    if request.method == 'POST':
        #fügt die bestellung zur datenbank hinzu
        return add_order(request.form, store)

    else:
        # gibt die aktuellen bestellungen zurück
        orders = Order.query.order_by(Order.id).filter(Order.owner== store)
        displayOrders = transform_orders_to_display(orders)
        return render_template("order.html", products=products, store=store, orders=displayOrders)


# entfernt die Bestellung aus der Liste
@app.route("/done/<int:id>")
def done(id):
    order = Order.query.get_or_404(id)

    try:
        order.done = True
        db.session.commit()

    except:
        print("Error editing Order")
    return redirect("/")

# erlaubt das abbrechen von bestellungen
@app.route("/cancel/<int:id>")
def cancel(id):

    order = Order.query.get_or_404(id)
    try:
        order.canceled = True
        db.session.commit()
    except:
        print("Error editing Order")

    store = request.args.get("store")
    return redirect(f"/order?store={store}")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

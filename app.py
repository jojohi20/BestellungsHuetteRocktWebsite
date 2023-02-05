from datetime import datetime

from flask import Flask, render_template, url_for, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy, query
from sqlalchemy.dialects.postgresql import ARRAY

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://postgres:postgres@localhost/hr'
db = SQLAlchemy(app)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.Column(ARRAY(db.Integer), nullable=False)
    amounts = db.Column(ARRAY(db.Integer), nullable=False)
    owner = db.Column(db.String(32), nullable=False)
    done = db.Column(db.Boolean, default=False)
    in_progress = db.Column(db.Boolean, default=False)
    canceled = db.Column(db.Boolean, default=False)
    time = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self):
        return f"Created Order with id: {self.id}"


class Product:
    def __init__(self, name, id):
        self.name = name
        self.id = id


class DisplayOrder:
    def __init__(self, id, amounts, itemNames, store,displaytime, in_progress):
        self.id = id
        self.items_amounts = zip(itemNames, amounts)
        self.store = store
        self.displayTime = displaytime
        self.in_progress = in_progress


products = []
products.append(Product("Fass Pils", 1))
products.append(Product("Kiste Cola", 2))
products.append(Product("Kiste Fanta", 3))
products.append(Product("Kiste Sprite", 4))
products.append(Product("Kiste Wasser", 5))
products.append(Product("Kiste Becher", 6))


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

        itemNames = [get_product_with_id(item).name for item in order.items]
        displayTime = order.time.strftime("%H:%M")

        displayOrder = DisplayOrder(order.id, order.amounts, itemNames, order.owner, displayTime, order.in_progress)
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
    items, amounts = [], []
    
    for product in products:
        amount = int(form[f"amount{product.id}"])
        if amount <= 0:
            continue
        items.append(product.id)
        amounts.append(int(amount))

    if len(items) == 0:
        return redirect("/order?store=" + store)

    newOrder = Order(items=items, amounts=amounts, owner=store)
    try:
        db.session.add(newOrder)
        db.session.commit()
        return redirect("/order?store=" + store)
    except:
        return "Failed to create Task. Relode"


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
        orders = Order.query.order_by(Order.id).filter(Order.owner == store)
        displayOrders = transform_orders_to_display(orders)
        return render_template("order.html",store=store, products=products, orders=displayOrders)


@app.route("/info", methods=['POST', 'GET'])
def info():
    store_items = {}
    for store in stores:
        orders = Order.query.order_by(Order.id).filter(Order.owner == store)
        items = {}
        for order in orders:
            if not order.done:
                continue
            for i, item in enumerate(order.items):
                product_name = get_product_with_id(item).name
                if not product_name in items:
                    items[product_name] = 0
                items[product_name] += order.amounts[i]

        store_items[store] = items
    return render_template("info.html", store_items=store_items)

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

@app.route("/accept/<int:id>")
def accept(id):
    order = Order.query.get_or_404(id)
    try:
        order.in_progress = True
        db.session.commit()
    except:
        print("Error editing Order")

    return redirect("/")

@app.route('/getOrders', methods=['GET'])
def get_orders():
    store = request.args.get("store")
    orders = Order.query.order_by(Order.id)

    if store:
        orders = orders.filter(Order.owner == store)

    displayOrders = transform_orders_to_display(orders)
    return render_template("ordertable.html", store=store, orders=displayOrders)



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

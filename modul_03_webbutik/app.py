"""Webbutiken. Starta med: flask --app app run --debug

Allt går via vanliga formulär (POST + redirect), så sidan laddas om helt vid varje klick.
Det är med flit: det är här du lägger till fetch.
"""
import os

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "bara-for-lokalt-bruk")

# Priser i hela kronor, exklusive moms.
PRODUCTS = [
    {"id": 1, "name": "Kaffe, stor och svart", "price": 49, "vat": 12},
    {"id": 2, "name": "Pepparkakor, burk", "price": 35, "vat": 12},
    {"id": 3, "name": "Bok: Clean Code", "price": 399, "vat": 6},
    {"id": 4, "name": "Gummianka (för felsökning)", "price": 59, "vat": 25},
    {"id": 5, "name": "Mekaniskt tangentbord", "price": 1290, "vat": 25},
    {"id": 6, "name": "Kabelstrumpa, 5 meter", "price": 79, "vat": 25},
]


def find_product(product_id: int):
    return next((p for p in PRODUCTS if p["id"] == product_id), None)


def cart_rows() -> list[dict]:
    """Bygger raderna i varukorgen ur sessionen."""
    rows = []
    for product_id, quantity in session.get("cart", {}).items():
        product = find_product(int(product_id))
        if product is None:
            continue
        vat_per_unit = int(product["price"] * product["vat"] / 100)
        vat = vat_per_unit * quantity
        rows.append({
            "id": product["id"],
            "name": product["name"],
            "quantity": quantity,
            "price_ex_vat": product["price"] * quantity,
            "vat": vat,
            "total": product["price"] * quantity + vat,
        })
    return rows


def cart_totals(rows: list[dict]) -> dict:
    return {
        "ex_vat": sum(row["price_ex_vat"] for row in rows),
        "vat": sum(row["vat"] for row in rows),
        "to_pay": sum(row["total"] for row in rows),
    }


@app.context_processor
def inject_cart_count():
    return {"cart_count": sum(session.get("cart", {}).values())}


@app.get("/")
def index():
    return render_template("index.html", products=PRODUCTS)


@app.post("/lagg-till")
def add_to_cart():
    product_id = request.form.get("product_id", type=int)
    if product_id is None or find_product(product_id) is None:
        return redirect(url_for("index"))
    cart = session.get("cart", {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    session["cart"] = cart
    return redirect(url_for("index"))


@app.get("/varukorg")
def show_cart():
    rows = cart_rows()
    return render_template("varukorg.html", rows=rows, totals=cart_totals(rows))


@app.post("/ta-bort")
def remove_from_cart():
    product_id = request.form.get("product_id", "")
    cart = session.get("cart", {})
    cart.pop(product_id, None)
    session["cart"] = cart
    return redirect(url_for("show_cart"))


@app.post("/betala")
def pay():
    rows = cart_rows()
    if not rows:
        return redirect(url_for("index"))
    totals = cart_totals(rows)
    session["cart"] = {}
    return render_template("tack.html", rows=rows, totals=totals)

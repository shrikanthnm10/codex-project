from flask import Flask, jsonify, render_template, request
from .config import Config
from .models import Customer, SalesOrder, db


def create_app() -> Flask:
    """Factory method used by Flask, tests, and WSGI server."""
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    @app.get("/")
    def dashboard():
        customer_count = Customer.query.count()
        order_count = SalesOrder.query.count()
        return render_template(
            "dashboard.html",
            customer_count=customer_count,
            order_count=order_count,
        )

    @app.post("/customers")
    def create_customer():
        payload = request.get_json(force=True)
        customer = Customer(name=payload["name"], email=payload["email"])
        db.session.add(customer)
        db.session.commit()
        return jsonify({"id": customer.id, "name": customer.name}), 201

    @app.post("/orders")
    def create_order():
        payload = request.get_json(force=True)
        order = SalesOrder(
            order_number=payload["order_number"],
            customer_id=payload["customer_id"],
            amount=payload["amount"],
        )
        db.session.add(order)
        db.session.commit()
        return jsonify({"id": order.id, "order_number": order.order_number}), 201

    return app


app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=8000, debug=False)

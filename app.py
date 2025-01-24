import requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean, and_
import os

app = Flask(__name__)


class Base(DeclarativeBase):
    pass


# Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URI",'sqlite:///cafes.db')
db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Cafe TABLE Configuration
class Cafe(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    map_url: Mapped[str] = mapped_column(String(500), nullable=False)
    img_url: Mapped[str] = mapped_column(String(500), nullable=False)
    location: Mapped[str] = mapped_column(String(250), nullable=False)
    seats: Mapped[str] = mapped_column(String(250), nullable=False)
    has_toilet: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_wifi: Mapped[bool] = mapped_column(Boolean, nullable=False)
    has_sockets: Mapped[bool] = mapped_column(Boolean, nullable=False)
    can_take_calls: Mapped[bool] = mapped_column(Boolean, nullable=False)
    coffee_price: Mapped[str] = mapped_column(String(250), nullable=True)


with app.app_context():
    db.create_all()

def printff(f):
    print(f)

def set(f):
    if f == None:
        return False
    elif f == "on":
        return True

@app.route('/')
def home():
    calls = request.form.get('calls')
    socket = request.form.get('sockets')
    wifi = request.form.get('wifi')
    toilet = request.form.get('toilet')
    if((calls == None) and (socket == None) and (wifi == None) and (toilet == None)):
        result = db.session.execute(db.select(Cafe))
    else:
        result = db.session.execute(db.select(Cafe).where(and_(Cafe.can_take_calls == calls,Cafe.has_wifi == wifi,Cafe.has_sockets == socket,Cafe.has_toilet == toilet)))
    all_cafes = result.scalars().all()
    return render_template("index.html",cafes =all_cafes)


@app.route('/custom', methods=['POST'])
def custom():
    calls = set(request.form.get('calls'))
    socket = set(request.form.get('sockets'))
    wifi = set(request.form.get('wifi'))
    toilet = set(request.form.get('toilet'))
    filters = []
    if ((calls == False) and (socket == False) and (wifi == False) and (toilet == False)):
        result = db.session.execute(db.select(Cafe))
        all_cafes = result.scalars().all()
    else:
        all_cafes = []

    if calls:
        filters.append(Cafe.can_take_calls == calls)

    if socket:
        filters.append(Cafe.has_sockets == socket)

    if wifi:
        filters.append(Cafe.has_wifi == wifi)

    if toilet:
        filters.append(Cafe.has_toilet == toilet)

    if filters:
        query = db.select(Cafe).where(and_(*filters))
        result = db.session.execute(query)
        new_cafes = result.scalars().all()
        existing_ids = {cafe.id for cafe in all_cafes}
        all_cafes.extend(cafe for cafe in new_cafes if cafe.id not in existing_ids)


    return render_template("index.html", cafes=all_cafes, calls=calls, socket=socket, wifi=wifi, toilet=toilet)




@app.route("/<int:cafe_id>")
def shop_info(cafe_id):
    cafe = db.get_or_404(Cafe, cafe_id)
    return render_template("shop.html",shop=cafe)

if __name__ == "__main__":
    app.run(debug=True)

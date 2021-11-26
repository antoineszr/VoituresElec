import sqlite3
from flask import Flask
from flask import render_template, request, redirect, url_for, g
import zeep
app = Flask(__name__)

DATABASE = "database.db"

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def change_db(query,args=()):
    cur = get_db().execute(query, args)
    get_db().commit()
    cur.close()

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    voitures_list=query_db("SELECT * FROM voitures")
    return render_template("index.html", voitures_list=voitures_list)

@app.route('/trajet', methods = ['POST'])
def trajet():
    result = request.form
    
    auto = result['auto']
    lata = result['lata']
    longa = result['longa']
    latb = result['latb']
    longb = result['longb']
    wsdl = 'https://mycv.glaivemedia.fr/?wsdl'
    client = zeep.Client(wsdl)
    resultat = client.service.tempsParcours(lata, longa, latb, longb, auto)
    return render_template("trajet.html", resultat=resultat)

@app.route('/voitures')
def voitures():
    voitures_list=query_db("SELECT * FROM voitures")
    return render_template("voitures.html",voitures_list=voitures_list)

@app.route('/create', methods=['GET', 'POST'])
def create():

    if request.method == "GET":
        return render_template("create.html",voitures=None)

    if request.method == "POST":
        voitures=request.form.to_dict()
        values=[voitures["marque"],voitures["modele"],voitures["autonomie"]]
        change_db("INSERT INTO voitures (marque,modele,autonomie) VALUES (?,?,?)",values)
        return redirect(url_for("voitures"))

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def udpate(id):

    if request.method == "GET":
        voitures=query_db("SELECT * FROM voitures WHERE id=?",[id],one=True)
        return render_template("update.html",voitures=voitures)

    if request.method == "POST":
        voitures=request.form.to_dict()
        values=[voitures["marque"],voitures["modele"],voitures["autonomie"],id]
        change_db("UPDATE voitures SET marque=?, modele=?, autonomie=? WHERE ID=?",values)
        return redirect(url_for("voitures"))

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):

    if request.method == "GET":
        voitures=query_db("SELECT * FROM voitures WHERE id=?",[id],one=True)
        return render_template("delete.html",voitures=voitures)

    if request.method == "POST":
        change_db("DELETE FROM voitures WHERE id = ?",[id])
        return redirect(url_for("voitures"))
#TODO walidacja
#TODO obsługa błędów
from flask import Flask, url_for, render_template, g, request, redirect
import sqlite3
from hashlib import sha256
app = Flask(__name__)


def get_ingridients(id):
    sql="select * from Skladnik where id=?;"
    db=get_db()
    cursor=db.execute(sql,[id])
    data=list(cursor.fetchone())
    return (data)
#-----------------------------------------------------------
#funkcja jest wywoływana gdy potrzebne jest baza danych
#jeżeli tabele już istnieją zapytania sql nic nie zmienią
#------------------------------------------------------------
def createdatabase():

    sql="""CREATE TABLE IF NOT EXISTS `Skladnik` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Nazwa` VARCHAR(45) NULL,
        `kalorie_na_100gr` INTEGER  NULL,
        `Dodatkowe` VARCHAR(45) NULL
        );

        """
    g.sqlite_db.execute(sql)
    sql="""

        CREATE TABLE IF NOT EXISTS `Administrator` (
        `nazwa_identyfikacyjna` VARCHAR(30) NOT NULL,
        `Mail` VARCHAR(60) NOT NULL,
        `Hasło` VARCHAR(65) NOT NULL,
        PRIMARY KEY (`nazwa_identyfikacyjna`),
        UNIQUE  (`Mail` ASC));

            """
    g.sqlite_db.execute(sql)
    sql="""   

        CREATE TABLE IF NOT EXISTS `Posiłek` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Administrator_nazwa_identyfikacyjna` VARCHAR(30) NOT NULL,
        `Nazwa` VARCHAR(45) NOT NULL,
        CONSTRAINT `fk_Posiłek_Administrator1`
            FOREIGN KEY (`Administrator_nazwa_identyfikacyjna`)
            REFERENCES `Administrator` (`nazwa_identyfikacyjna`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);


            """
    g.sqlite_db.execute(sql)
    sql="""
        CREATE TABLE IF NOT EXISTS `posrednia_skladnik_posilek` (
        `ID` INTEGER  PRIMARY KEY AUTOINCREMENT,
        `Posiłek_ID` INT NOT NULL,
        `Skladnik_ID` INT NOT NULL,
        `Ilosc` FLOAT NOT NULL,
        CONSTRAINT `fk_posrednia_skladnik_posilek_Posiłek1`
            FOREIGN KEY (`Posiłek_ID`)
            REFERENCES `Posiłek` (`ID`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT `fk_posrednia_skladnik_posilek_Skladnik1`
            FOREIGN KEY (`Skladnik_ID`)
            REFERENCES `Skladnik` (`ID`)
            ON DELETE NO ACTION
            ON UPDATE NO ACTION);
            """
    g.sqlite_db.execute(sql)
    g.sqlite_db.commit()

def get_db():
    if not hasattr(g, 'sqlite_db'):
        conn = sqlite3.connect('data5.db3')
        conn.row_factory = sqlite3.Row
        g.sqlite_db = conn
        createdatabase()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def get_ingredients(id):
    sql="select from skladnik where id=?;"
    db=get_db()
    cursor=db.execute(sql[id])
    response_data=cursor.fetchone()
    print(response_data)
    
    


class Posilek:
    def __init__(self, name, calories, ingredients):
        self.name = name
        self.calories = calories
        self.ingredients = ingredients


@app.route('/')
def index():

    a1 = Posilek("Zupa",20000,['Marchew', 'Kości', 'Kostka rosołowa'])
    a2 = Posilek("Zupa",20000,['Twaróg', 'Kości', 'Kostka rosołowa'])
    info = [a1,a1,a1,a2,a2,a1,a2,a1,a2]
    info=[]
    return render_template('Wyswietlenie.html', info=info,get_ingridients=get_ingridients)


@app.route('/skl')
def skladniki():

    db = get_db()
    sql = "select * from Skladnik;"
    cursor = db.execute(sql)
    info = cursor.fetchall()
    return render_template('wyswietl_skl.html',info=info)

def searchforid(name):
    db=get_db()
    sql="select id from Skladnik where nazwa=?;"
    cursor=db.execute(sql,[name])
    for a in cursor.fetchall():
        print(a[0])
        return 1


@app.route('/wpr_po', methods=['GET','POST'])
def wpr():
    db=get_db()
    if(request.method == 'POST'):
        #ilosc=request.form['ilosc']
        name=request.form['nazwa']
        ingridients=request.form['ingredients'].split(';')
        sql="insert into Posiłek values(null, 'Admin',?);"
        db.execute(sql,[name])
        id=int(db.execute('select max(id) from Posiłek;').fetchone()[0])
        print(id)
        sql="insert into posrednia_skladnik_posilek values(null,? ,?,1);"
        for item in ingridients:
            db.execute(sql,[id,searchforid(item)])
        db.commit()
        return render_template('base.html')
    else:
        sql= "select * from Skladnik;"
        cursor=db.execute(sql)
        return render_template('wprowadz_posilek.html',ingredients=cursor.fetchall())

@app.route('/wpr_skl', methods=['GET','POST'])
def wpr_skl():

    db= get_db()
    if request.method == 'POST':

        sql = 'insert into Skladnik values (null, ?, ? ,?);'
        nazwa=request.form['nazwa']
        kalorie=request.form['kalorie']
        db.execute(sql,[nazwa, kalorie, ''])
        db.commit()
        return render_template('wprowadz_skl.html',info='Dane zostały wprowadzone poprawnie')
    else:
        return render_template('wprowadz_skl.html',info='')


@app.route("/logowanie",methods=["GET","POST"])
def singin():
    if(request.method=="GET"):
        return render_template("/logowanie.html")
    else:
        return redirect(url_for("index"))



if __name__=='__main__':
    app.run(port=8031,debug=True)












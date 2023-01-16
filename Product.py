from flask import Flask,request,jsonify,make_response
from sqlalchemy import Table, Column, Integer, String,func,select,create_engine,bindparam,MetaData
from flask_sqlalchemy import SQLAlchemy
import psycopg2



# creation de l'app flask
app = Flask(__name__)


# configuration de SQLite database, relative a cett app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# creation de la table product stored in metadata_obj

metadata_obj  = MetaData()


#instabtation d'un metadata objet pour le storage des table de bd 
product = Table("product",
metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(16), nullable=False),
    Column("price", String(10)),
)
# la connexion a la base de donnees
# engine = create_engine('postgresql+psycopg2://postgres:pass1234/@localhost/postgres')
engine = create_engine('postgresql://postgres:pass1234@localhost:5432/product')

# engine = create_engine(
# 'sqlite:///db.sqlite3',
# connect_args={'check_same_thread': False}
# )
#Create all tables stored in this metadata.
metadata_obj.create_all(engine)
# Etablire la conn
conn = engine.connect()

with app.app_context():
    @app.route("/create/product", methods=["GET", "POST"])
    def product_create():
        if request.method == "POST":
          if request.json["price"] and request.json["name"]:
            try:
                a=float(request.json["price"])
                ins = product.insert().values(price=a,name=request.json["name"])
                # ins.compile().params 
                conn.execute(ins)
                resp=make_response(jsonify(messsagr="product created",name=request.json["name"],price=request.json["price"]),200)
                return resp
            except ValueError:
                rse=make_response(jsonify(messsagr="BAD REQUEST",name=request.json["name"],price=request.json["price"]),400)
                return rse
          elif request.json["price"]=='' or request.json["name"]=='':
                rse=make_response(jsonify(messsagr="BAD REQUEST",name=request.json["name"],price=request.json["price"]),400)
                return rse
    @app.route("/products",methods=["GET"])
    def list_products():
        sel2=product.select()
     
        result=conn.execute(sel2)
        
        # result = connection.execute("SELECT * FROM table_name")
        row = result.fetchall()
        #fetchall()
        
        if len(row)==0:
              rse=make_response(jsonify(messsagr="404 Not Found",name=request.json["name"],price=request.json["price"]),404)
              return rse
        l=[]
        for r in row:
          dict={'id':r[0],'name':r[1],'price':r[2]}
          l.append(dict)
        print(l)
        rse=make_response(jsonify(messsagr="products",rows=l),200)
        return rse
    @app.route("/update/product",methods=["GET","PUT", "POST"])
    def update_product():
       if request.method == "PUT":
              if request.json["id"] and request.json["price"]:
                  PRICE=request.json["price"]
                  id_=request.json["id"]
                  stmt = (product.update().where(product.c.id ==id_).values(price=PRICE))
                  conn.execute(stmt)
                  sel2=product.select().where(product.c.id ==id_)
                  result1=conn.execute(sel2)
                  l=[]
                  row = result1.fetchone()
                  dict={'id':row[0],'name':row[1],'price':row[2]}
                  l.append(dict)
                  rse=make_response(jsonify(messsagr="price modified",row=l),200) 
                  return rse
              elif request.json["id"]=='' or request.json["price"]=='':
                   res=make_response(jsonify(messsagr="BAD REQUEST"),400)
                   return res
    @app.route("/delete/product",methods=["DELETE", "POST"])
    def delete_product():
       if request.method == "DELETE":
            if request.json["id"] :
                id_=request.json["id"]
                stmt = (
                product.delete().where(product.c.id ==id_))
                conn.execute(stmt)
                rse=make_response(jsonify(messsagr="product deleted"),200) 
                return rse
            elif request.json["id"]=='':
              res=make_response(jsonify(messsagr="BAD REQUEST"),400)
              return res



import falcon
#from .images import Resource
import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base

import factura
import os

engine = create_engine("sqlite:///data.sqlite")
session = sessionmaker(engine)()
Base = declarative_base()


class Cliente(Base):
    __tablename__ = 'clientes'
    id = Column(Integer, primary_key=True)
    codigo = Column(Integer)
    agente = Column(Integer)
    nombre = Column(String(128))

    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Agente(Base):
    __tablename__ = 'agentes'
    id = Column(Integer, primary_key=True)
    superagente = Column(Integer)
    agente = Column(Integer)
    nombre = Column(String(128))

    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Visita(Base):
    __tablename__ = 'visitas'
    id = Column(Integer, primary_key=True)
    agente = Column(Integer)
    #anyo = Column(String(128))
    #semana = Column(String(128))

    anyo = Column(Integer)
    semana = Column(Integer)

    diaSemana = Column(String(128))

    horaInicial = Column(DateTime)
    horaFinal = Column(DateTime)

    temasTratados = Column(String)
    acuerdos = Column(String)
    pendienteNuevaVisita = Column(String)
    pendienteAnteriorVisita = Column(String)
    
    pedidoFirme = Column(Boolean, default=False)
    nombreCliente = Column(String)
    
    asistentes = Column(String)

    presencial = Column(Boolean, default=False)
    tipoNoPresencial = Column(String)
    poblacion= Column(String)
    provincia = Column(String)
    enviado = Column(Boolean, default=False)
    
    def to_json(self):
           return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(64))
    email = Column(String(64), unique=True)

    def to_json(self):
        return {"username": self.username, "email": self.email}

class Index(object):
    def on_get(self, req, resp):
        msg = {
            "message": "It's a simple api written with falcon",
            "database": "sqlite",
            "orm": "sqlalchemy",
        }
        resp.body = json.dumps(msg)

class UserResource(object):
    def on_get(self, req, resp):
        username = req.get_param("username")
        user = session.query(User).filter((User.username == username)).first()
        if user is not None:
            resp.body = json.dumps(user.to_json())
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"error": "User not found"})
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        #data = json.load(req.bounded_stream)
        data = req.media
        print(data)
        #raw_json = req.bounded_stream.read()
        #result.json(raw_json, encoding='utf-8')
        #resp.body = json.dumps(result_json, encoding='utf-8')
        user = (
            session.query(User)
            .filter(
                (User.username == data["username"])
                | (User.email == data["email"])
            )
            .first()
        )
        if user is None:
            user = User(username=data["username"], email=data["email"])
            session.add(user)
            session.commit()
            resp.body = json.dumps({"message": "User has been created."})
            resp.status = falcon.HTTP_302
        else:
            resp.body = json.dumps(
                {"error": "Username or email already in use."}
            )
            resp.status = falcon.HTTP_200

    def on_delete(self, req, resp):
        username = req.get_param("username")
        email = req.get_param("email")
        user = (
            session.query(User)
            .filter((User.username == username) & (User.email == email))
            .first()
        )
        if user is not None:
            session.delete(user)
            session.commit()

            resp.data = json.dumps({"message": "User deleted."})
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"error": "User not found"})
            resp.status = falcon.HTTP_404

class ClienteResource(object):
    def on_get(self, req, resp):
        username = req.get_param("username")
        user = session.query(User).filter((User.username == username)).first()
        if user is not None:
            resp.body = json.dumps(user.to_json())
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"error": "User not found"})
            resp.status = falcon.HTTP_404

    def on_post(self, req, resp):
        #data = json.load(req.bounded_stream)
        data = req.media
        print(data)
        #raw_json = req.bounded_stream.read()
        #result.json(raw_json, encoding='utf-8')
        #resp.body = json.dumps(result_json, encoding='utf-8')
        
        cliente = (
            session.query(Cliente)
            .filter(Cliente.codigo == data["codigo"]).first()
        )

        if cliente is None:
            cliente = Cliente(codigo=data["codigo"], nombre=data["nombre"])
            session.add(cliente)
            session.commit()
            resp.body = json.dumps({"message": "Cliente has been created."})
            resp.status = falcon.HTTP_302
        else:
            resp.body = json.dumps(
                {"error": "Cliente already in use."}
            )
            resp.status = falcon.HTTP_200
        


    def on_delete(self, req, resp):
        username = req.get_param("username")
        email = req.get_param("email")
        user = (
            session.query(User)
            .filter((User.username == username) & (User.email == email))
            .first()
        )
        if user is not None:
            session.delete(user)
            session.commit()

            resp.data = json.dumps({"message": "User deleted."})
            resp.status = falcon.HTTP_200
        else:
            resp.body = json.dumps({"error": "User not found"})
            resp.status = falcon.HTTP_404

class ClientesResource(object):
    def on_get(self, req, resp, agente=0):
        if agente == 0:
            clientes = session.query(Cliente).all()
        else:
            clientes = session.query(Cliente).filter(Cliente.agente == agente).all()
        
        clientesArray = []
        for cliente in clientes:
            clientesArray.append(cliente.to_json())

        #return json.dumps(clientesArray)
        resp.body = json.dumps(clientesArray)

class VisitasResource(object):
    def on_get(self, req, resp, agente=0):
        print('ENTRA')
        print(agente)
        
        if agente == 0:
            visitas = session.query(Visita).all()
        else:
            visitas = session.query(Visita).filter(Visita.agente == agente).all()


        visitasArray = []
        for visita in visitas:
            visitasArray.append(visita.to_json())

        resp.body = json.dumps(visitasArray)


class AgentesResource(object):
    def on_get(self, req, resp, superagente=0):
        if superagente != 0:
            agentes = session.query(Agente).filter(Agente.superagente == superagente).all()
        
        agentesArray = []
        for agente in agentes:
            agentesArray.append(agente.to_json())

        resp.body = json.dumps(agentesArray)

class FacturasResource(object):
    def on_get(self, req, resp, numeroFactura=""):
        print("Factura: " + numeroFactura)
        (nom, ext) = numeroFactura.split(".", maxsplit=2)
        facturaJson = nom + ".json"
        facturaPdf = nom + ".pdf"
        factura.procesar(facturaJson, facturaPdf)
        
        script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        rel_path = "facturas/" + facturaPdf
        abs_file_path = os.path.join(script_dir, rel_path)

        #filename="./evaluation.pdf"
        resp.downloadable_as = facturaPdf
        resp.content_type = 'application/pdf'

        resp.stream= open(abs_file_path, 'rb')
        resp.status = falcon.HTTP_200


        #factura.procesar2()
        #resp.body = json.dumps(agentesArray)

        #resp.body = '{"message": "Hello world!"}'
        


class Familia(Base):
    __tablename__ = 'familias'
    id = Column(Integer, primary_key=True)
    codigo = Column(Integer)
    nombre = Column(String(128))
    almacen = Column(Integer)

    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Formato(Base):
    __tablename__ = 'formatos'
    id = Column(Integer, primary_key=True)
    codigo = Column(Integer)
    nombre = Column(String(128))
    almacen = Column(Integer)

    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class Articulo(Base):
    __tablename__ = 'articulos'
    id = Column(Integer, primary_key=True)
    codigo = Column(String(13))
    nombre = Column(String(128))
    familia = Column(Integer)
    formato = Column(Integer)
    fechaFabricacion = Column(Integer)
    fechaCaducidad = Column(Integer)
    loteProveedor = Column(String(20))
    udm = Column(String(3))
    stock = Column(Float)
    cantidadFabricada = Column(Float)
    fechaPrimeraVenta = Column(Integer)
    fechaUltimaVenta = Column(Integer)
    almacen = Column(Integer)


    def to_json(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}

class FormatosResource(object):
    def on_get(self, req, resp, almacen=0):
        if almacen == 0:
            elementos = session.query(Formato).all()
        else:
            elementos = session.query(Formato).filter(Formato.almacen == almacen).all()

        elementosArray = []
        for elemento in elementos:
            elementosArray.append(elemento.to_json())

        resp.body = json.dumps(elementosArray)


class ArticulosResource(object):
    def on_get(self, req, resp, almacen=0):
    
        if almacen == 0:
            elementos = session.query(Articulo).all()
        else:
            elementos = session.query(Articulo).filter(Articulo.almacen == almacen).all()
    
        elementosArray = []
        for elemento in elementos:
            elementosArray.append(elemento.to_json())

        resp.body = json.dumps(elementosArray)


class FamiliasResource(object):
    def on_get(self, req, resp, almacen=0):

        if almacen == 0:
            elementos = session.query(Familia).all()
        else:
            elementos = session.query(Familia).filter(Familia.almacen == almacen).all()

        

        
        elementosArray = []
        for elemento in elementos:
            elementosArray.append(elemento.to_json())

        resp.body = json.dumps(elementosArray)


#api = application = falcon.API()

#images = Resource()
#api.add_route('/images', images)

api = falcon.API()
api.add_route("/", Index())
api.add_route("/user", UserResource())
api.add_route("/cliente", ClienteResource())

api.add_route("/clientes", ClientesResource())
api.add_route(
    "/articulos/{almacen}", 
    ArticulosResource())
api.add_route(
    "/formatos/{almacen}", 
    FormatosResource())
api.add_route(
    "/familias/{almacen}", 
    FamiliasResource()
    )


api.add_route(
    '/clientes/{agente}',
    ClientesResource()
)

api.add_route("/visitas", VisitasResource())
api.add_route(
    '/visitas/{agente}',
    VisitasResource()
)

api.add_route(
    '/facturas/{numeroFactura}',
    FacturasResource()
)



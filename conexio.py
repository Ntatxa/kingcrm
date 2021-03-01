# coding=utf-8

import os
from ftplib import FTP
import json
from app import engine, api, Base, session, Cliente, Visita, Agente, Formato, Familia, Articulo
from sqlalchemy import and_

import time 
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import asyncio

def enviarSMS():

    from twilio.rest import Client

    account_sid = "ACd1adcfae078d76ca36ac71fdf9c50902"
    auth_token = "ae92fe9f01b3e97783463bdcda82581f"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
		    body ="ola que ase :)", # mensaje
		    to = "+34628177604", # remplazamos con nuestro numero o al que queramos enviar el sms
		    from_= "+12055486482") # el numero que nos asigno twilio
    print(message.sid) 


def enviarWassap():

    from twilio.rest import Client

    account_sid = "ACd1adcfae078d76ca36ac71fdf9c50902"
    auth_token = "ae92fe9f01b3e97783463bdcda82581f"

    client = Client(account_sid, auth_token)
    
    from_wassap = "whatsapp:+14155238886"
    to_wassap = "whatsapp:+34628177604"
    message = client.messages.create(
		    body ="ola que ase en wassap :)", # mensaje
		    to = to_wassap,
		    from_= from_wassap)
    print(message.sid) 

def descargarFicheros(servidor, usuario, clave, directorioRemoto, directorioLocal):
    
    with FTP(servidor) as ftp:
        ftp.login(usuario, clave)
        ftp.cwd(directorioRemoto)
        rutaLocal = os.getcwd() + os.sep + directorioLocal
        print(rutaLocal)
        ficheros = ftp.nlst()
        
        for fichero in ficheros:
            local_filename = rutaLocal + fichero
            with open(local_filename, 'wb') as f:
                def callback(data):
                    f.write(data)
        
                ftp.retrbinary('RETR %s' % fichero, callback)
                #ftp.delete(fichero)

def grabarClientes():
    with open('clientes.json', 'r') as f:
        clientes_json = json.load(f)
        #print(clientes_json)
        #print(type(clientes_json))
        for json_item in clientes_json:
            #print(cliente)
            cliente = (
            session.query(Cliente)
            .filter(Cliente.codigo == json_item["codigo"]).first()
            )

            if cliente is None:
                cliente = Cliente(codigo=json_item["codigo"], nombre=json_item["nombre"], agente=json_item["agente"])
                session.add(cliente)
                session.commit()
            else:
                print("Error: cliente ya existente")
            

def grabarClientesSinComprobar():
    with open('clientes.json', 'r') as f:
        clientes_json = json.load(f)
        
        for json_item in clientes_json:
           cliente = Cliente(codigo=json_item["codigo"], nombre=json_item["nombre"], agente=json_item["agente"])
           session.add(cliente)
        ssession.commit()
           
            
def grabarVisitas():
    with open('visitas.json', 'r') as f:
        i = 0
        visitas_json = json.load(f)
        for json_item in visitas_json:
            visita = Visita(agente=json_item["agente"], anyo=json_item["anyo"], semana=json_item["semana"], diaSemana=json_item["diaSemana"], nombreCliente=json_item["nombreCliente"], temasTratados=json_item["temasTratados"], acuerdos=json_item["acuerdos"], pendienteNuevaVisita=json_item["pendienteNuevaVisita"])
            session.add(visita)
            i+=1
            print(i)

            session.commit()

def borrar_visitas():
    session.query(Visita).delete()

def borrar_agentes():
    session.query(Agente).delete()

def borrar_clientes():
    session.query(Cliente).delete()


def borrar_articulos():
    session.query(Articulo).delete()
    

def borrar_familias():
    session.query(Familia).delete()


def borrar_formatos():
    session.query(Formato).delete()


def grabarArticulos(fichero, almacen):
    with open(fichero, 'r') as f:
        datos_json = json.load(f)
        i = 0
        for json_item in datos_json:
            #articulo = Articulo()
            articulo = Articulo(codigo=json_item["codigo"], nombre=json_item["nombre"], familia=json_item["familia"], formato=json_item["formato"], fechaFabricacion=json_item["fechaFabricacion"], fechaCaducidad=json_item["fechaCaducidad"], loteProveedor=json_item["loteProveedor"], udm=json_item["udm"], stock=json_item["stock"], cantidadFabricada=json_item["cantidadFabricada"], fechaPrimeraVenta=json_item["fechaPrimeraVenta"], fechaUltimaVenta=json_item["fechaUltimaVenta"])
            articulo.almacen = almacen
            #for k, v in json_item.items():
               #print(k)
               #print(v)
               #articulo.k = v
            i+=1
            print(i)
            session.add(articulo)
        session.commit()

def grabarFormatos(fichero, almacen):
    with open(fichero, 'r') as f:
        
        formatos_json = json.load(f)
        for json_item in formatos_json:
            formato = Formato(codigo=json_item["codigo"], nombre=json_item["nombre"])
            formato.almacen = almacen
            session.add(formato)
        session.commit()


'''
def grabarFamilias():
    with open('familias.json', 'r') as f:
        
        familias_json = json.load(f)
        for json_item in familias_json:
            familia = Familia(codigo=json_item["codigo"], nombre=json_item["nombre"])
            session.add(familia)
        session.commit()
'''

def grabarFamilias(fichero, almacen):
    with open(fichero, 'r') as f:
        
        familias_json = json.load(f)
        for json_item in familias_json:
            familia = Familia(codigo=json_item["codigo"], nombre=json_item["nombre"])
            familia.almacen = almacen
            session.add(familia)
        session.commit()

def subirFicheros(servidor, usuario, clave, directorioRemoto, directorioLocal, extension=".json"):
    
    print(servidor)
    print(directorioLocal)
    print(directorioRemoto)

    with FTP(servidor) as ftp:
        ftp.login(usuario, clave)
        ftp.cwd(directorioRemoto)
        rutaLocal = os.getcwd() + os.sep + directorioLocal
        
        print(rutaLocal)
        ficheros = os.listdir(rutaLocal)
        for fichero in ficheros:
            if os.path.isfile(os.path.join(rutaLocal, fichero)):
                (nom, ext) = os.path.splitext(fichero)
                if ext == extension:
                    
                    f2 = rutaLocal + fichero 
                    f = open(f2, 'rb')
                    a = 'STOR ' + fichero
                    print(f2)
                    print(a)
                    ftp.storbinary(a, f)
                    f.close()
                    os.remove(f2)


def grabarAgentes():
    with open('agentes.json', 'r') as f:
        agentes_json = json.load(f)
     
        for json_item in agentes_json:
            agente = (
            session.query(Agente)
            .filter(and_(Agente.superagente == json_item["superagente"], Agente.agente == json_item["agente"])).first()
            )

            if agente is None:
                agente = Agente(superagente=json_item["superagente"], nombre=json_item["nombre"], agente=json_item["agente"])
                session.add(agente)
                session.commit()
            else:
                print("Error: agente ya existente")
                

def inicializar():

    server = '80.28.249.31'
    user = 'nando'
    clau = 'guardiola'
    origen = '/QIBM/gasvis/json/'
    destino = 'ficheros/'

    print("descargando")
    descargarFicheros(server, user, clau, origen, destino)
    print("descargado")
    
    rellenar()


    print("Hecho")
    time.sleep(60*60)

    '''
    print("descargando")
    descargarFicheros(server, user, clau, origen, destino)
    print("descargado")
    
    borrar_visitas()
    print("borrado visitas")
    borrar_agentes()
    print("borrado agentes")
    borrar_clientes()
    print("borrado clientes")
    grabarAgentes()
    print("agentes grabados")
    grabarVisitas()
    print("visitas grabadas")
    grabarClientes()
    print("clientes grabados")
    '''

def facturasJSON():

    server = '80.28.249.31'
    user = 'nando'
    clau = 'guardiola'
    origen = '/QIBM/facturasJson/kr/'
    destino = 'facturas/'

    descargarFicheros(server, user, clau, origen, destino)
    print("descargado")
    
   


def rellenar():

    borrar_articulos()
    grabarArticulos("ficheros/articulos.json", 1)
    grabarArticulos("ficheros/articulos100.json", 100)
    grabarArticulos("ficheros/articulos501.json", 501)
    
    borrar_familias()
    grabarFamilias("ficheros/familias.json", 1)
    grabarFamilias("ficheros/familias100.json", 100)
    grabarFamilias("ficheros/familias501.json", 501)

    borrar_formatos()
    grabarFormatos("ficheros/formatos.json", 1)
    grabarFormatos("ficheros/formatos100.json", 100)
    grabarFormatos("ficheros/formatos501.json", 501)


def formatos():

    borrar_formatos()
    grabarFormatos("ficheros/formatos.json", 1)
    grabarFormatos("ficheros/formatos100.json", 100)
    grabarFormatos("ficheros/formatos501.json", 501)


class Watcher():
    DIRECTORY_TO_WATCH  = os.getcwd() + os.sep + 'ficheros'
    print(DIRECTORY_TO_WATCH)
    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = MyHandler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class MyHandler(FileSystemEventHandler):
    @staticmethod
    def on_any_event(event):
        if event.is_directory:
            return None
        elif event.event_type == 'created':
            print("created %s" %event.src_path)
            rellenar()
        elif event.event_type == 'modified':
            print("modified %s" %event.src_path)
            rellenar()


def vigilarDirectorio():
    w= Watcher()
    w.run()

#asyncio.run(vigilarDirectorio())

'''
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(inicializar())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    loop.close()

'''
facturasJSON()



'''
server = '80.28.249.31'
user = 'nando'
clau = 'guardiola'
origen = '/QIBM/gasvis/json/'
destino = 'ficheros/'

print("descargando")
descargarFicheros(server, user, clau, origen, destino)
print("descargado")
formatos()
'''



'''
server = '80.28.249.31'
user = 'nando'
clau = 'guardiola'
origen = '/QIBM/gasvis/json/'
destino = 'ficheros/'

print("descargando")
descargarFicheros(server, user, clau, origen, destino)
print("descargado")
'''

#inicializar()

#grabarFormatos()

#grabarClientes()
#borrar_visitas()
#grabarVisitas()
#grabarAgentes()

#enviarSMS()
#enviarWassap()



                
        
   




    


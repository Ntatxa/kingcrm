from fpdf import FPDF

import os

import json
from ftplib import FTP

import codecs
#import conexio

#import ebcdic


    

def descargarFicheros(servidor, usuario, clave, directorioRemoto, directorioLocal):
    
    #os.chdir(r"C:\ServidorWeb\server\kingCRM")

    with FTP(servidor) as ftp:
        ftp.login(usuario, clave)
        ftp.cwd(directorioRemoto)
        rutaLocal = os.getcwd() + os.sep +  directorioLocal

        rutaLocal = os.getcwd()
        print('--------------')
        print(rutaLocal)
        print('--------------')
        
        ficheros = ftp.nlst()

        
        for fichero in ficheros:
        
            #local_filename = rutaLocal + fichero
            print("Fichero: " + fichero)
            print("Ruta Local: " + rutaLocal)
            local_filename = rutaLocal + os.sep + fichero

            #if os.path.exists(local_filename):
                #os.remove(local_filename)
            with open(local_filename, 'wb+') as f:
                
                def callback(data):
                    f.write(data)
        
                ftp.retrbinary('RETR %s' % fichero, callback)
                #ftp.delete(fichero)
            f.close()

    ftp.close()
   

class FacturaPdf:
    
    pdf = FPDF()
    pagina = 0
    yLinea = 0
    saltoPagina = 225
    lineas = []
    jsonDecoded = ""
    textoResiduos = "El responsable de la entrega del residuo o envase usado, para su correcta gestión ambiental es el poseedor final (R.D. 782/98 art.18)"
    textoRegistro = "Inscrita en el Reg.Mercantil de Valencia, Tomo 6.630, Libro 3.934, Folio 205, Sección 8º, Hoja V-71.929, Inscr. 1ª."
    idioma = ""
    textosIdioma = {"INGLES":
                        {"albaran":"Dlv. Note:", "fecha":"Date:", "Pedido": "Order Nr.:", "bultos":"Total Cases:",
                        "pesoBruto":"Gross Weight:", "pesoNeto":"Net Weight:",
                        "cliente":"CUSTOMER NUMBER","agente":"BROKER", "numeroFactura":"INVOICE NUMBER",
                        "codigo":"ITEM Nr.","descripcion":"PRODUCT NAME", "cantidad":"CASES", "precio":"PRICE",
                        "importe":"AMOUNT","importeBruto":"GROSS AMOUNT",
                        "descuento":"DISCOUNT","descuentoPP":"%ADV PAYMENT",
                        "condicionesPago":"PAYMENT TERMS:", "totalFactura":"TOTAL INVOICE"}}
    
    
    
    def __init__(self):
        
        self.pdf = FPDF()
        self.pdf.set_font("Arial", size=9)

        
    def __del__(self):
        #del(FPDF)
        print('Destructor called')
    
  

    def leerCaracter(self, nombreFichero="factura.json", desde=1, hasta=1):
        with open(nombreFichero) as fileobj:
            i=1
            for line in fileobj:  
                for ch in line: 
                    if i>= desde and i<=hasta:
                        print(ch)
                    i += 1

    def leerJSON(self, nombreFichero="E_1270.json"):
        
        
        #os.chdir(r"C:\ServidorWeb\server\kingCRM\facturas")
        
        #script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        #print(script_dir)

        #rel_path = "facturas/" + nombreFichero
        #abs_file_path = os.path.join(script_dir, rel_path)
        rutaFichero = os.getcwd() + os.sep + 'facturas' + os.sep + nombreFichero
    

        print("Fichero a abrir: " + rutaFichero)
        f = open(rutaFichero, "r")
        
        #f = codecs.open(abs_file_path, "r", encoding="cp500")
        content = f.read()
        
        jsonDecoded = json.loads(content)
        #print(jsonDecoded)

        f.close()
        self.jsonDecoded = jsonDecoded

        lineas =  jsonDecoded["lineas"]
        if "idioma" in jsonDecoded:
            self.idioma = jsonDecoded["idioma"]

        self.lineas = lineas
        
    def anyadirPagina(self):

        self.pagina += 1
        self.pdf.add_page()
        
        #self.pdf.image("preformatoKr.png", 1, 1)


        self.pdf.image("leon_agua.png", 40, 100, 150, 150)
        self.pdf.image("LOGO_KR.jpg", 10, 1, 50, 50)
        

        

        self.pdf.rect(5, 60, 200, 15)
        self.textoImprimir(7, 64, self.idioma, "cliente", "CODIGO CLIENTE")

        self.pdf.line(40, 60, 40, 75)
        self.textoImprimir(42, 64, self.idioma, "agente", "AGENTE")

        self.pdf.line(108, 60, 108, 75)
        self.textoImprimir(110, 64, self.idioma, "fecha", "FECHA")

        self.pdf.line(168, 60, 168, 75)

        self.textoImprimir(175, 64, self.idioma, "numeroFactura", "Nº FACTURA")
        
        self.pdf.rect(5, 80, 200, 150)
        
        self.pdf.line(5, 86, 205, 86)
        self.textoImprimir(7, 84, self.idioma, "codigo", "CODIGO")
        self.pdf.line(25, 80, 25, 230)
        self.textoImprimir(42, 84, self.idioma, "descripcion", "DESCRIPCION")
        self.pdf.line(85, 80, 85, 230)
        self.textoImprimir(90, 84, self.idioma, "cantidad", "CANTIDAD")
        self.pdf.line(108, 80, 108, 230)
        self.pdf.text(110, 84, "UxCJ")
        self.pdf.line(118, 80, 118, 230)
        self.pdf.text(120, 84, "T.UDS")
        self.pdf.line(135, 80, 135, 230)
        self.textoImprimir(140, 84, self.idioma, "precio", "PRECIO UNIDAD")
        self.pdf.line(168, 80, 168, 230)
        self.pdf.text(170, 84, "% DTO")
        self.pdf.line(182, 80, 182, 230)

        self.textoImprimir(185, 84, self.idioma, "importe", "IMPORTE")
        
        self.pdf.rect(5, 235, 200, 30)

        self.yLinea = 239
        self.pdf.set_font("Arial", size=8)
        self.textoImprimir(10, self.yLinea, self.idioma, "importeBruto", "IMPORTE BRUTO")
        self.textoImprimir(40, self.yLinea, self.idioma, "descuento", "DESCUENTO")
        self.textoImprimir(70, self.yLinea, self.idioma, "descuentoPP", "DESCUENTO P.P")
        
            
        
        
        if self.idioma == "":
            self.pdf.text(110, self.yLinea, "BASE IMPONBLE")
            self.pdf.text(150, self.yLinea, "IVA")
            self.pdf.text(170, self.yLinea, "REC.EQUIVALENCIA")
        
        self.pdf.set_font("Arial", size=6)
        self.textoImprimir(10, 269, self.idioma, "condicionesPago", "CONDICIONES DE PAGO:")
        self.pdf.rect(5, 270, 140, 20)

        self.pdf.rect(155, 270, 50, 20)
        self.pdf.set_font("Arial", size=10)
        self.textoImprimir(160, 275, self.idioma, "totalFactura", "TOTAL FACTURA")
        

        
        self.pdf.set_font("Arial", size=7)
        self.pdf.text(10, 293, self.textoResiduos)
        self.pdf.text(10, 296, self.textoRegistro)
        
        self.pdf.set_font("Arial", size=10)



    def imprimirCabecera(self):

        self.pdf.set_font("Arial", size=10)

        self.pdf.line(105, 15, 110, 15)
        self.pdf.line(105, 15, 105, 20)
        
        self.pdf.line(200, 15, 205, 15)
        self.pdf.line(205, 15, 205, 20)
        
        
        self.yLinea = 20
        self.pdf.text(110, self.yLinea, self.jsonDecoded["nombre"])
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["direccion1"])
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["direccion2"])
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["direccion3"])
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["direccion4"])
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["Nif"])
        self.yLinea += 6
        
        self.pdf.line(200, self.yLinea, 205, self.yLinea)
        self.pdf.line(205, self.yLinea-5, 205, self.yLinea)
        
        self.pdf.line(105, self.yLinea-5, 105, self.yLinea)
        self.pdf.line(105, self.yLinea, 110, self.yLinea)
        
        
        
        self.yLinea = 70
        self.pdf.text(10, self.yLinea, self.jsonDecoded["codigoCliente"])
        self.pdf.text(42, self.yLinea, self.jsonDecoded["agente"])
        self.pdf.text(115, self.yLinea, self.jsonDecoded["fecha"])
        self.pdf.text(175, self.yLinea, self.jsonDecoded["factura"])

        print(self.jsonDecoded["codigoCliente"])

    def imprimirPie(self):
    
    
        self.yLinea = 246
        self.pdf.set_font("Arial", size=10)
        self.pdf.text(10, self.yLinea, self.jsonDecoded["bruto"])
        self.pdf.text(35, self.yLinea, self.jsonDecoded["descuento"])
        self.pdf.text(50, self.yLinea, self.jsonDecoded["ImporteDtc1"])
        self.pdf.text(70, self.yLinea, self.jsonDecoded["dtoPronto"])
        self.pdf.text(90, self.yLinea, self.jsonDecoded["ImporteDtpp"])
        
        self.pdf.text(110, self.yLinea, self.jsonDecoded["base1"])
        self.pdf.text(130, self.yLinea, self.jsonDecoded["porcentajeIva1"])
        self.pdf.text(155, self.yLinea, self.jsonDecoded["cuotaIva1"])
        self.pdf.text(170, self.yLinea, self.jsonDecoded["porcentajeRecargo1"])
        self.pdf.text(190, self.yLinea, self.jsonDecoded["cuotaRecargo1"])
        
        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["base2"])
        self.pdf.text(130, self.yLinea, self.jsonDecoded["porcentajeIva2"])
        self.pdf.text(150, self.yLinea, self.jsonDecoded["cuotaIva2"])
        self.pdf.text(170, self.yLinea, self.jsonDecoded["porcentajeRecargo2"])
        self.pdf.text(190, self.yLinea, self.jsonDecoded["cuotaRecargo2"])

        self.yLinea += 6
        self.pdf.text(110, self.yLinea, self.jsonDecoded["base3"])
        self.pdf.text(130, self.yLinea, self.jsonDecoded["porcentajeIva3"])
        self.pdf.text(150, self.yLinea, self.jsonDecoded["cuotaIva3"])
        self.pdf.text(170, self.yLinea, self.jsonDecoded["porcentajeRecargo3"])
        self.pdf.text(190, self.yLinea, self.jsonDecoded["cuotaRecargo3"])
        
        
        self.yLinea = 276
        
        if "formaPago" in self.jsonDecoded.keys():
            
            self.pdf.text(40, self.yLinea, self.jsonDecoded["formaPago"])
            self.yLinea += 6

        
        if "importePlazo1" in self.jsonDecoded.keys():
        
            if self.jsonDecoded["importePlazo1"].strip() != "":
                self.pdf.text(10, self.yLinea, self.jsonDecoded["fechaPlazo1"])
                self.pdf.text(35, self.yLinea, self.jsonDecoded["importePlazo1"])
    
            if self.jsonDecoded["importePlazo2"].strip() != "":
                self.pdf.text(65, self.yLinea, self.jsonDecoded["fechaPlazo2"])
                self.pdf.text(85, self.yLinea, self.jsonDecoded["importePlazo2"])
        
            if self.jsonDecoded["importePlazo3"].strip() != "":
                self.pdf.text(105, self.yLinea, self.jsonDecoded["fechaPlazo3"])
                self.pdf.text(125, self.yLinea, self.jsonDecoded["importePlazo3"])
        
        if "apagar" in self.jsonDecoded.keys():
        
            self.pdf.text(175, self.yLinea, self.jsonDecoded["apagar"])
        
    
    def textoImprimir(self, x=0, y=0, idioma="", clave="", textoInicial=""):
        texto = textoInicial
        if idioma in self.textosIdioma:
            if clave in self.textosIdioma[idioma]:
                
                texto = self.textosIdioma[idioma][clave]
        self.pdf.text(x, y, texto)



        


    def imprimirLineas(self):
        self.yLinea = 90
        self.pdf.set_font("Arial", size=10)

        if self.pagina == 1:
            primeraLineaImpresa = False    
            if self.jsonDecoded["albaran"].strip() != "":
                if self.idioma != "":
                    self.pdf.text(32, self.yLinea, "Dlv. Note:: " + self.jsonDecoded["albaran"])
                else:
                    self.pdf.text(32, self.yLinea, "Albaran: " + self.jsonDecoded["albaran"])

                primeraLineaImpresa = True
                if self.idioma != "":
                    self.pdf.text(62, self.yLinea, "Date: " + self.jsonDecoded["fechaAlbaran"])
                else:
                    self.pdf.text(62, self.yLinea, "Fecha: " + self.jsonDecoded["fechaAlbaran"])
                
                primeraLineaImpresa = True
            if self.jsonDecoded["pedido"].strip() != "":
                if self.idioma != "":
                    self.pdf.text(102, self.yLinea, "Order Nr.: " + self.jsonDecoded["pedido"])
                else:
                    self.pdf.text(102, self.yLinea, "Pedido: " + self.jsonDecoded["pedido"])
                
                primeraLineaImpresa = True
            
            if primeraLineaImpresa:
                self.yLinea += 5
        for linea in self.lineas:

            
            
            self.pdf.set_font("Arial", size=6)
            self.pdf.text(7, self.yLinea, linea["articulo"])
            self.pdf.set_font("Arial", size=8)
            self.pdf.text(32, self.yLinea, linea["descripcion"])
            self.pdf.text(98, self.yLinea, linea["cantidad"].lstrip(' 0').rjust(7))
            self.pdf.text(110, self.yLinea, linea["factor"].lstrip(' 0').rjust(7))
            self.pdf.text(120, self.yLinea, linea["unidades"])
            self.pdf.text(140, self.yLinea, linea["precio"])
            self.pdf.text(170, self.yLinea, linea["descuento"])
            self.pdf.text(185, self.yLinea, linea["importe"])

            
            self.yLinea += 5
            self.saltar()
    
    def imprimirPesos(self):
        
        self.pdf.set_font("Arial", size=8)
        
        observaciones = []
        if 'observaciones' in self.jsonDecoded.keys():
            observaciones = self.jsonDecoded["observaciones"]
        for observacion in observaciones:
            if observacion.strip() != "":
                self.yLinea = self.yLinea + 5
                self.saltar()
                self.pdf.text(32, self.yLinea, observacion)
                
            
        self.yLinea = self.yLinea + 5
        self.saltar()

        if "bultos" in self.jsonDecoded.keys():
            self.textoImprimir(7, self.yLinea, self.idioma, "bultos", "Bultos: ")
            self.pdf.text(32, self.yLinea, self.jsonDecoded["bultos"])
            
        if "pesoBruto" in self.jsonDecoded.keys():
            self.textoImprimir(58, self.yLinea, self.idioma, "pesoBruto", "Peso Bruto: ")
            self.pdf.text(80, self.yLinea, self.jsonDecoded["pesoBruto"])

        if "pesoNeto" in self.jsonDecoded.keys():
            self.textoImprimir(120, self.yLinea, self.idioma, "pesoNeto", "Peso Neto: ")
            self.pdf.text(140, self.yLinea, self.jsonDecoded["pesoNeto"])

            print(self.yLinea)

    def saltar(self):
        if self.yLinea > self.saltoPagina:
            self.anyadirPagina()
            self.imprimirCabecera()
            self.yLinea = 90



    

    def finalizarDocumento(self, documento="factura.pdf"):
        
        
        #script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
        #rel_path = "facturas\\" + documento
        #abs_file_path = os.path.join(script_dir, rel_path)

        rutaFichero = os.getcwd() + os.sep + 'facturas' + os.sep + documento
        
        print("Fichero a cerrar: " + rutaFichero)
        self.pdf.output(rutaFichero) 


    
def procesar(ficheroJson, ficheroPdf):
    
    #facturaJson = "facturas/" + ficheroJson
    #facturaPdf = "facturas/" + ficheroPdf


    '''
    server = '80.28.249.31'
    user = 'nando'
    clau = 'guardiola'
    origen = '/QIBM/facturasJson/kr/'
    destino = 'facturas\\'

    descargarFicheros(server, user, clau, origen, destino)


    os.chdir(r"C:\ServidorWeb\server\kingCRM\facturas")
    '''

    factura = FacturaPdf()

    print(ficheroJson)
    factura.leerJSON(ficheroJson)

        
    
    factura.anyadirPagina()
    factura.imprimirCabecera()
    factura.imprimirLineas()
    factura.imprimirPesos()
    factura.imprimirPie()

    print("Fichero a finalizar: " + ficheroPdf)
    factura.finalizarDocumento(ficheroPdf)
    
    #factura.close()
    #factura.output()
    #del(factura)    

     




if __name__ == '__main__':
    
    '''
    print(os.getcwd())

    
    
    server = '80.28.249.31'
    user = 'nando'
    clau = 'guardiola'
    origen = '/QIBM/facturasJson/kr/'
    destino="facturas"
    descargarFicheros(server, user, clau, origen, destino)

    
    
    
    '''


    def jsonToPDF(nombreJson, nombrePdf):
        factura = FacturaPdf()
    
        factura.leerJSON(nombreJson)
            
        factura.anyadirPagina()
        factura.imprimirCabecera()
        factura.imprimirLineas()
        factura.imprimirPesos()
        factura.imprimirPie()

        factura.finalizarDocumento(nombrePdf)
        del(factura)
        

    ruta = os.getcwd() + os.sep + 'facturas'
    with os.scandir(ruta) as ficheros:
        for fichero in ficheros:
            print(fichero.name)    
    
            
            (nom, ext) = fichero.name.split(sep='.')
            
            
            
            if ext == 'json':

                print("Entra: " + fichero.name)
                destino = nom + '.pdf'

                jsonToPDF(fichero.name, destino)
    

    
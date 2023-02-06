#ejecutar desde la carpeta, para que detecte el archivo de la interfaz grafica
from random import randint
from PyQt5 import QtCore, QtWidgets,QtGui
from PyQt5 import uic
import sys, time

class Cronometro(QtCore.QThread):
	segundo = QtCore.pyqtSignal(int)
	
	def __init__(self):
		super(Cronometro, self).__init__(None)
		
	
	#se inicia o continua el proceso
	def run(self):
		while True:
			time.sleep(1)#para que se alcancen a reflejar los cambios en la interfaz
			self.segundo.emit(1)

class VentanaPrincipal(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.ui = uic.loadUi('prueba.ui',self)#Se carga la interfaz grafica

		try:
			archivo = open("demofile.txt", "r")
			texto = archivo.read()
			self.areaDeTexto.setPlainText(texto)
			
		except:
			print("No se pudo abrir el archivo")
		finally:
			archivo.close()

		self.primerHilo = Cronometro()
		self.primerHilo.segundo.connect(self.autoGuardado)
		self.primerHilo.start()
		
	def autoGuardado(self,senial):
		try:
			if senial == 1:
				archivo2 = open("demofile.txt", "w")
				escribir = self.areaDeTexto.toPlainText()
				archivo2.write(escribir)
				archivo2.close()
		except:
			print("No se pudo guardar archivo")
		finally:
			archivo2.close()

#Iniciamos la aplicacion en bucle
app = QtWidgets.QApplication(sys.argv)
mainWindow = VentanaPrincipal()
mainWindow.show()
sys.exit(app.exec_())
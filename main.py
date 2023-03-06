from random import randint
from PyQt5 import QtCore, QtWidgets
from PyQt5 import uic
import sys, time

class HiloPrincipal(QtCore.QThread):

	porcentaje = QtCore.pyqtSignal(int)
	fila = QtCore.pyqtSignal(int)
	idProceso = QtCore.pyqtSignal(dict)
	cambiarLabel = QtCore.pyqtSignal(int)

	def __init__(self, error, cola):
		super(HiloPrincipal, self).__init__(None)
		self.error = error
		self.cola = cola

	#proceso principal
	def run(self):
		while True:
			if self.error[0] == 0:
				self.procesamiento(self.cola,self.error)

	def procesamiento(self,cola,error):
		try:
			if len(cola)>0:
				probabilidad = randint(1,3)
				if probabilidad ==1:
					hola = 1/0
				else:
					for i in range (1,101):
						self.porcentaje.emit(i)
						time.sleep(0.01)
					id = cola.pop(0)
					self.fila.emit(1)
					self.idProceso.emit({"senial":1,"id":id})
					time.sleep(0.01)
		except:
			error[0] = 1
			time.sleep(0.01)
			self.cambiarLabel.emit(1)
			time.sleep(0.01)
			
			

class HiloSecundario(QtCore.QThread):
	porcentaje = QtCore.pyqtSignal(int)
	fila = QtCore.pyqtSignal(int)
	idProceso = QtCore.pyqtSignal(dict)

	def __init__(self, error, cola):
		super(HiloSecundario, self).__init__(None)
		self.error = error
		self.cola = cola

	#proceso principal
	def run(self):
		while True:
			if self.error[0] == 1:
				self.procesamiento(self.cola)

	def procesamiento(self,cola):
		if len(cola)>0:
			for i in range (1,101):
				self.porcentaje.emit(i)
				time.sleep(0.01)
			id = cola.pop(0)
			self.fila.emit(1)
			self.idProceso.emit({"senial":1,"id":id})
			time.sleep(0.01)
		

	
class VentanaPrincipal(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QMainWindow.__init__(self)
		self.ui = uic.loadUi('prueba.ui',self)#Se carga la interfaz grafica

		self.procesosPendientes = []
		self.error = [0]
		#inicializamos los arreglos de procesos y sus datos
		for i in range(10):
			self.procesosPendientes.append(i+1)


		#llenamos la tabla de pendientes
		for i in range(len(self.procesosPendientes)):
			self.tablaPendientes.insertRow(self.tablaPendientes.rowCount())
			id = QtWidgets.QTableWidgetItem(str(self.procesosPendientes[i]))
			self.tablaPendientes.setItem(i,0,id)

		self.btnI.clicked.connect(self.correr)


	def correr(self):
		self.hiloPrincipal = HiloPrincipal(self.error,self.procesosPendientes)
		self.hiloPrincipal.porcentaje.connect(self.socketPorcentaje)
		self.hiloPrincipal.fila.connect(self.socketFila)
		self.hiloPrincipal.idProceso.connect(self.socketIdProceso)
		self.hiloPrincipal.cambiarLabel.connect(self.socketCambiarLabel)

		self.hiloSecundario = HiloSecundario(self.error,self.procesosPendientes)
		self.hiloSecundario.porcentaje.connect(self.socketPorcentajeSecundario)
		self.hiloSecundario.fila.connect(self.socketFila)
		self.hiloSecundario.idProceso.connect(self.socketIdProceso)

		self.hiloPrincipal.start()
		self.hiloSecundario.start()
	
	def socketPorcentaje(self,senial):
		self.barra_1.setValue(senial)

	def socketCambiarLabel(self,senial):
		if senial == 1:
			self.lbError.setText("Error al ejecutar tarea")
			self.barra_1.setValue(0)

	def socketPorcentajeSecundario(self,senial):
		self.barra_2.setValue(senial)

	def socketFila(self,senial):
		if senial == 1:
			self.tablaPendientes.removeRow(0)

	def socketIdProceso(self,senial):
		if senial["senial"] == 1:
			self.tablaTerminados.insertRow(self.tablaTerminados.rowCount())
			id = QtWidgets.QTableWidgetItem(str(senial["id"]))
			self.tablaTerminados.setItem(self.tablaTerminados.rowCount()-1,0,id)

#Iniciamos la aplicacion en bucle
app = QtWidgets.QApplication(sys.argv)
mainWindow = VentanaPrincipal()
mainWindow.show()
sys.exit(app.exec_())
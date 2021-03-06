# Doble importacion para evitar los conflictos de nombres entre el 
# Message de Tkinter y el de tkMessageBox, 
# vease la funcion creaVisorMensajes para mas info
import Tkinter
from Tkinter import *

from tkFileDialog import askopenfilename, asksaveasfilename
from tkColorChooser import askcolor
from tkMessageBox import *
import ImageTk
from imagen.tratamientoImagen import ImagenTratada
from brazo.acciones import Acciones
import time

class GUI(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.movimientoLibre = False
		self.tiempoInicial = 0
		self.tiempoFinal = 0
		self.tiempoDeTratamientoImagen = 0
		self.enMovimiento = False
		self.tiempoInicioMovimiento = 0
		self.angulosActuales = []
		self.angulosAnteriores = []
		self.diferenciaAngulos = [0,0,0]
		self.imagenTratada = ImagenTratada()
		self.acciones = Acciones()
		self.creaElementos()
		self.inicioCicloEjecucion()
		self.master.title('Control Experimental Brazo Robotico')
		self.master.iconname('Control Experimental Brazo Robotico')
		
	def creaElementos(self):
		self.creaBarraMenus()
		self.creaAreaSuperior()
		self.creaAreaInferior()
		self.creaAreaIntermedia()
		
		
	def creaAreaSuperior(self):
		self.areaSuperior = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaSuperior.pack(side=TOP, fill=X)	
		self.creaAreaVisorImagen(self.areaSuperior)
		self.creaAreaVisorAngulos(self.areaSuperior)
		
	def creaAreaIntermedia(self):
		self.areaIntermedia = Frame(self, cursor='hand2', 
									relief=SUNKEN, bd=2)
		self.areaIntermedia.pack(side=BOTTOM, fill=X, anchor=N)		
		self.creaAreaControlesAproximados(self.areaIntermedia)
		self.creaAreaControlesExactos(self.areaIntermedia)
		
	def creaAreaInferior(self):	
		self.areaInferior = Frame(self, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaInferior.pack(side=BOTTOM, fill=X)	
		self.creaAreaStop(self.areaInferior)
			
	def creaBarraMenus(self):
		self.menubar = Menu(self.master)
		self.master.config(menu=self.menubar)
		self.menuAjustes()
		self.menuBrazo()
		
	def menuAjustes(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Cargar Ajustes...', command=self.cargaAjustes)
		miniMenu.add_command(label='Salir...', command=self.quit)
		self.menubar.add_cascade(label='Ajustes', underline=0, menu=miniMenu)
		
	def menuBrazo(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Mover solo si se ven los marcadores', command=lambda:self.hacerMovimientoLibre(False))
		miniMenu.add_command(label='Mover siempre', command=lambda:self.hacerMovimientoLibre(True))
		self.menubar.add_cascade(label='Brazo', underline=0, menu=miniMenu)
			
	def hacerMovimientoLibre(self, decision):
		if decision == True:
			self.movimientoLibre = True
		else:
			self.movimientoLibre = False
			
	def cargaAjustes(self):	
		archivo = askopenfilename(initialdir='/imagen/MisAjustes')
		self.imagenTratada.cargaAjustes(archivo)
					
	def aunPorHacer(self):
		print "Funcion aun por implementar"
		
	def quit(self):
		if askyesno('Verificacion de Salida', 'Estas seguro de querer salir?'):
			Frame.quit(self)
			
	def creaAreaVisorImagen(self,frame):
		self.areaVisorImagen = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisorImagen.pack(side=LEFT, fill=X)
		self.creaVisorImagen(self.areaVisorImagen )
			
	def creaVisorImagen(self, frame):
		self.visorImagen = Label(frame, text='Area visor Imagen')
		self.visorImagen.pack(side=LEFT, fill=X)
		
	def creaAreaVisorAngulos(self,frame):
		self.areaVisorAngulosActuales = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisorAngulosActuales.pack(side=TOP, fill=X)
		self.creaVisoresAngulosActuales(self.areaVisorAngulosActuales )
		
		self.ponerSeparadores( frame, 1)
		
		self.areaVisorAngulosAnteriores = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisorAngulosAnteriores.pack(side=TOP, fill=X)
		self.creaVisoresAngulosAnteriores(self.areaVisorAngulosAnteriores )
		
		self.ponerSeparadores( frame, 1)
		
		self.areaVisorAngulosDiferencia = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisorAngulosDiferencia.pack(side=TOP, fill=X)
		self.creaVisoresAngulosDiferencia(self.areaVisorAngulosDiferencia )
			
			
	def creaVisoresAngulosActuales(self, frame):
		self.visorAngulosActuales = []
		self.creaVisorAngulosGenerico(self.visorAngulosActuales, 'Angulos Actuales', frame)
			
	def creaVisoresAngulosAnteriores(self, frame):
		self.visorAngulosAnteriores = []
		self.creaVisorAngulosGenerico(self.visorAngulosAnteriores,'Angulos Anteriores', frame)
			
	def creaVisoresAngulosDiferencia(self, frame):
		self.visorAngulosDiferencia = []
		self.creaVisorAngulosGenerico(self.visorAngulosDiferencia, 'Diferencia Angulos', frame)
			
	def creaVisorAngulosGenerico(self, visorAngulos,texto, frame):
		for i in range(3):
			visor = Tkinter.Message(frame)
			visor.config(font=('times', 8), width = 70, text = texto)
			visor.pack(side=LEFT, fill=X, expand=YES)
			visorAngulos.append(visor)
			
	def creaAreaControlesAproximados(self,frame):
		self.areaControlesAproximados = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesAproximados.pack(side=LEFT, fill=X)
		self.creaControlesAproximados(self.areaControlesAproximados)
		
	def creaControlesAproximados(self, frame):
		#Empiezo colocando cosas por la parte de abajo del frame 
		# para que el pack() no me de problemas
		areaAux = Frame(frame, cursor='hand2', bd=2)
		areaAux.pack(side=BOTTOM, fill=X)	
		self.ponerSeparadores(areaAux, 1)
		Button(areaAux, text = ' - ',command=lambda:self.mueveBase('izq')).pack(side=LEFT)
		Label(areaAux, text='Base ' ).pack(side=LEFT)
		Button(areaAux, text = ' + ',command=lambda:self.mueveBase('der')).pack(side=LEFT)
		Label(areaAux, text='  ').pack(side=LEFT)
		Button(areaAux, text = ' - ',command=lambda:self.muevePinza('cerrar')).pack(side=LEFT)
		Label(areaAux, text='Pinza ' ).pack(side=LEFT)
		Button(areaAux, text = ' + ',command=lambda:self.muevePinza('abrir')).pack(side=LEFT)
		Label(areaAux, text='  ').pack(side=LEFT)
		Button(areaAux, text = ' - ',command=lambda:self.luz('apagar')).pack(side=LEFT)
		Label(areaAux, text='Luz ' ).pack(side=LEFT)
		Button(areaAux, text = ' + ',command=lambda:self.luz('encender')).pack(side=LEFT)
		Label(areaAux, text='  ').pack(side=LEFT)
		
		self.tiempoMovimiento = DoubleVar()
		self.deslizableTiempo = Scale(frame, label = 'tiempo de movimiento ',
											variable=self.tiempoMovimiento,
											from_=0, to=2,
											tickinterval=0.25,
											resolution=0.05,
											orient='horizontal',
											length=320)
		self.deslizableTiempo.pack(side=TOP, fill=X)
		self.tiempoMovimiento.set(0.5)
		
		self.ponerSeparadores(frame, 1)
		self.ponerBotonesAngulo(frame,1)
		self.ponerBotonesAngulo(frame,2)
		self.ponerBotonesAngulo(frame,3)
			
	def ponerBotonesAngulo(self,frame, numAngulo):
		Button(frame, text = ' - ',command=lambda:self.disminuyeAngulo(numAngulo)).pack(side=LEFT)
		Label(frame, text='Angulo ' + str(numAngulo)).pack(side=LEFT)
		Button(frame, text = ' + ',command=lambda:self.aumentaAngulo(numAngulo)).pack(side=LEFT)
		Label(frame, text='  ').pack(side=LEFT)
		
	def iniciarMovimiento(self):
		""" Solo inicia el movimieno si tiene una lista de angulos actuales buena 
		Devuelve True si ha podido iniciar el movimiento y false en caso contrario"""
		if self.movimientoLibre :
			return True
			
		if self.angulosActuales == [] :
			print("No se puede iniciar el movimiento al no disponer de los angulos iniciales")
			return False
		else:
			self.enMovimiento = True
			self.tiempoInicioMovimiento = time.time()
			self.angulosAnteriores = self.angulosActuales[:] # Copia una lista en otra
			return True
		
	def finalizarMovimiento(self):
		if self.movimientoLibre :
			return True
			
		self.enMovimiento = False
		for i in range(3):
			self.diferenciaAngulos[i] = abs(self.angulosAnteriores[i] - self.angulosActuales[i])
		
		
	def aumentaAngulo(self, numAngulo):
		if self.iniciarMovimiento():
			print("Aumentando angulo {} con un tiempo {}".format(numAngulo, self.tiempoMovimiento.get()))	
			self.acciones.tiempo = self.tiempoMovimiento.get()	
			if numAngulo == 3:
				self.acciones.actuar('subir-hombro')
			elif numAngulo == 2:
				self.acciones.actuar('subir-codo')
			elif numAngulo == 1:
				self.acciones.actuar('subir-munneca')
			else:
				pass
			
	def mueveBase(self, comando):
		if self.iniciarMovimiento():
			self.acciones.tiempo = self.tiempoMovimiento.get()
			if comando == 'izq':
				self.acciones.actuar('base-izquierda')
			elif comando == 'der':
				self.acciones.actuar('base-derecha')
			else:
				pass
			
	def muevePinza(self, comando):
		if self.iniciarMovimiento():
			self.acciones.tiempo = self.tiempoMovimiento.get()
			if comando == 'abrir':
				self.acciones.actuar('abrir-pinza')
			elif comando == 'cerrar':
				self.acciones.actuar('cerrar-pinza')
			else:
				pass
			
	def luz(self, comando):
		if self.iniciarMovimiento():
			self.acciones.tiempo = self.tiempoMovimiento.get()
			if comando == 'encender':
				self.acciones.actuar('encender-luz')
			elif comando == 'apagar':
				self.acciones.actuar('apagar-luz')
			else:
				pass
			
		
	def disminuyeAngulo(self, numAngulo):
		if self.iniciarMovimiento():
			print("Disminuyendo angulo {} con un tiempo {}".format(numAngulo, self.tiempoMovimiento.get()))
			self.acciones.tiempo = self.tiempoMovimiento.get()	
			if numAngulo == 3:
				self.acciones.actuar('bajar-hombro')
			elif numAngulo == 2:
				self.acciones.actuar('bajar-codo')
			elif numAngulo == 1:
				self.acciones.actuar('bajar-munneca')
			else:
				pass
			
	def creaAreaControlesExactos(self,frame):
		self.areaControlesExactos = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesExactos.pack(side=LEFT, fill=X)
		self.creaControlesExactos(self.areaControlesExactos)
	
	def creaControlesExactos(self, frame):
		self.areaAngulo1 = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaAngulo1.pack(side=TOP, fill=X)
		self.creaControlAngulo1(self.areaAngulo1 )
		
		self.ponerSeparadores( frame, 1)
		
		self.areaAngulo2 = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaAngulo2.pack(side=TOP, fill=X)
		self.creaControlAngulo2(self.areaAngulo2 )
		
		self.ponerSeparadores( frame, 1)
		
		self.areaAngulo3 = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaAngulo3.pack(side=TOP, fill=X)
		self.creaControlAngulo3(self.areaAngulo3 )
		
			
	def creaControlAngulo1(self, frame):
		control1 = Label(frame, text='Angulo1')
		control1.pack(side=LEFT, fill=X, expand=YES)
		self.entradaAngulo1 = Entry(frame)
		self.entradaAngulo1.pack(side=LEFT)
		self.entradaAngulo1.bind('<Return>', (lambda event: self.imprimeEntradas()))
		
	def creaControlAngulo2(self, frame):
		control2 = Label(frame, text='Angulo2')
		control2.pack(side=LEFT, fill=X, expand=YES)
		self.entradaAngulo2 = Entry(frame)
		self.entradaAngulo2.pack(side=LEFT)
		self.entradaAngulo2.bind('<Return>', (lambda event: self.imprimeEntradas()))
		
	def creaControlAngulo3(self, frame):
		control3 = Label(frame, text='Angulo3')
		control3.pack(side=LEFT, fill=X, expand=YES)
		self.entradaAngulo3 = Entry(frame)
		self.entradaAngulo3.pack(side=LEFT)
		self.entradaAngulo3.bind('<Return>', (lambda event: self.imprimeEntradas()))
		
	def imprimeEntradas(self):
		print(self.entradaAngulo1.get())
		print(self.entradaAngulo2.get())
		print(self.entradaAngulo3.get())
		print("")
			
		
	def creaAreaStop(self,frame):
		self.areaAreaStop = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaAreaStop.pack(side=BOTTOM, fill=X)
		self.creaControlStop(self.areaAreaStop)
		
	def creaControlStop(self, frame):
		self.controlStop = Button(frame, text='Parar', command=self.acciones.actuar('parar'))
		self.controlStop.pack(side=RIGHT)
		texto = "Tiempo tratamiento: {} " .format(self.tiempoDeTratamientoImagen)
		self.etiquetaTiempo = Label(frame, text =texto) 
		self.etiquetaTiempo.pack(side = LEFT)
		
	
	def inicioCicloEjecucion(self):
		self.actualizaVisorImagen()
		
	# ------------------------------------------------------------------
	# Ejecucion en ciclica de las siguientes funciones
	
	# actualizaVisorImagen ->
	# actualizaVisorAngulos ->
	
	# actualizaVisorImagen ->
	# actualizaVisorAngulos ->
	# etc ...
	# ------------------------------------------------------------------
	
	
	def actualizaVisorImagen(self):
		self.tiempoInicial = time.time()
		
		img , self.angulosActuales = self.imagenTratada.capturaTrataYFiltraBlobsDeImagen()
												  
		photo = ImageTk.PhotoImage(img.getPIL())
		self.visorImagen.photo = photo
		self.visorImagen.configure(image=photo)
		self.visorImagen.after(10, self.actualizaVisorAngulos)
		
	
		
	def actualizaVisorAngulos(self):
		actualizarAnterioresYDiferencias = False
		if self.enMovimiento:
					tiempoEnMovimiento =  time.time() - self.tiempoInicioMovimiento
					print("Tiempo en movimiento: {}".format(tiempoEnMovimiento))
					if tiempoEnMovimiento > self.acciones.tiempo + 2*self.tiempoDeTratamientoImagen:
						if self.angulosActuales != []:
							self.finalizarMovimiento()
							actualizarAnterioresYDiferencias = True
							print("")
						
		if self.angulosActuales == []:
			for i in range(3):
				texto = "Angulo Actual {0}: --- grados ".format(str(i+1))
				self.visorAngulosActuales[i].config(text=texto)
		else:
			for i, angulo in enumerate(self.angulosActuales):
				texto = "Angulo Actual {0}: {1:0.1f} grados ".format(str(i+1), angulo)
				self.visorAngulosActuales[i].config(text=texto)
				if actualizarAnterioresYDiferencias:
					texto = "Angulo Anterior {0}: {1:0.1f} grados ".format(str(i+1), self.angulosAnteriores[i])
					self.visorAngulosAnteriores[i].config(text=texto)
					texto = "Diferencia Angulos {0}: {1:0.1f} grados ".format(str(i+1), self.diferenciaAngulos[i])
					self.visorAngulosDiferencia[i].config(text=texto)
					
		self.tiempoFinal = time.time()
		self.tiempoDeTratamientoImagen = self.tiempoFinal - self.tiempoInicial
		#print (self.tiempoDeTratamientoImagen)
		texto = "Tiempo tratamiento: {0:0.2f} segundos " .format(self.tiempoDeTratamientoImagen)
		self.etiquetaTiempo.config(text =texto) 
				
		self.actualizaVisorImagen()
		

		
	# ------------------------------------------------------------------
	# Fin de un ciclo de ejecucion
	# ------------------------------------------------------------------
		
	def ponerSeparadores(self, frame, num):
		for i in range(num):
			Label(frame, text = "                             ").pack(side=TOP, 
																	  expand=YES, 
																	  fill=X)
		
		
if __name__ == '__main__':
    
    GUI().mainloop()
        

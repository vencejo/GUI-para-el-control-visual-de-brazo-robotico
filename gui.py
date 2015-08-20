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
import time

class GUI(Frame):
	def __init__(self, parent=None):
		Frame.__init__(self, parent)
		self.pack(expand=YES, fill=BOTH)
		self.tiempoInicial = 0
		self.tiempoFinal = 0
		self.tiempoDeEjecucion = 0
		self.imagenTratada = ImagenTratada()
		self.creaElementos()
		self.inicioCicloEjecucion()
		self.master.title('Ajustes Visuales para el Control Experimental Brazo Robotico')
		self.master.iconname('Ajustes Visuales')
		
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
		self.menuArchivo()
		self.menuEditar()
		self.menuImagen()
		
	def menuArchivo(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Cargar Ajustes...', command=self.aunPorHacer)
		miniMenu.add_command(label='Guardar Ajustes...', command=self.aunPorHacer)
		miniMenu.add_command(label='Salir...', command=self.quit)
		self.menubar.add_cascade(label='Archivo', underline=0, menu=miniMenu)
		
	def menuEditar(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Copiar...', command=self.aunPorHacer)
		miniMenu.add_command(label='Pegar...', command=self.aunPorHacer)
		self.menubar.add_cascade(label='Editar', underline=0, menu=miniMenu)
			
	def menuImagen(self):
		miniMenu = Menu(self.menubar)
		miniMenu.add_command(label='Zoom +...', command=self.aunPorHacer)
		miniMenu.add_command(label='Zoom -...', command=self.aunPorHacer)
		miniMenu.add_command(label='Capturar Imagen...', command=self.quit)
		self.menubar.add_cascade(label='Imagen', underline=0, menu=miniMenu)
	
	def guardaAjustes(self):
		archivo = asksaveasfilename(defaultextension = 'json',
									initialdir='/imagen/MisAjustes')
		self.ajustes.guardaAjustes(archivo)
	
	
	
		
	def conversorRGBaHEX(self):
		rgb = (self.nivelR.get(),self.nivelG.get(),self.nivelB.get())
		return '#' + "".join(map(chr, rgb)).encode('hex')
			
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
		self.areaVisorAngulos = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaVisorAngulos.pack(side=LEFT, fill=X)
		self.creaVisorAngulos(self.areaVisorAngulos )
			
	def creaVisorAngulos(self, frame):
		self.visorAngulos = Label(frame, text='Area visor Angulos')
		self.visorAngulos.pack(side=LEFT, fill=X)
		
	def creaAreaControlesAproximados(self,frame):
		self.areaControlesAproximados = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesAproximados.pack(side=LEFT, fill=X)
		self.creaControlesAproximados(self.areaControlesAproximados)
		
	def creaControlesAproximados(self, frame):
		self.controlesAproximados = Label(frame, text='Area Controles aproximados')
		self.controlesAproximados.pack(side=LEFT, fill=X)
		
	def creaAreaControlesExactos(self,frame):
		self.areaControlesExactos = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaControlesExactos.pack(side=LEFT, fill=X)
		self.creaControlesExactos(self.areaControlesExactos)
		
	def creaControlesExactos(self, frame):
		self.controlesExactos = Label(frame, text='Area Controles exactos')
		self.controlesExactos.pack(side=LEFT, fill=X)
		
	def creaAreaStop(self,frame):
		self.areaAreaStop = Frame(frame, cursor='hand2', relief=SUNKEN, bd=2)
		self.areaAreaStop.pack(side=BOTTOM, fill=X)
		self.creaControlStop(self.areaAreaStop)
		
	def creaControlStop(self, frame):
		self.controlStop = Label(frame, text='Stop')
		self.controlStop.pack(side=BOTTOM)
		
	
	def inicioCicloEjecucion(self):
		self.actualizaVisorImagen()
		
	# ------------------------------------------------------------------
	# Ejecucion en ciclica de las siguientes funciones
	
	# actualizaAjustes ->
	# actualizaVisorImagenOriginal ->
	# actualizaVisorImagenTratada ->
	# actualizaVisorImagenBlobs ->
	# actualizaAjustes -> etc ...
	# ------------------------------------------------------------------
	
	
	def actualizaVisorImagen(self):
		self.tiempoInicial = time.time()
		
		img = self.imagenTratada.capturaTrataYFiltraBlobsDeImagen('estructura')
												  
		photo = ImageTk.PhotoImage(img.getPIL())
		self.visorImagen.photo = photo
		self.visorImagen.configure(image=photo)
		
		self.tiempoFinal = time.time()
		self.tiempoDeEjecucion = self.tiempoFinal - self.tiempoInicial
		#print (self.tiempoDeEjecucion)
		
		self.visorImagen.after(10, self.actualizaVisorImagen)
		
	
		
	def actualizaVisorMensajes(self):
		texto = "Tiempo de procesado {0:0.2f} seg ".format(self.tiempoDeEjecucion)
		self.mensaje.config(text=texto)
		self.actualizaAjustes()
		
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
        

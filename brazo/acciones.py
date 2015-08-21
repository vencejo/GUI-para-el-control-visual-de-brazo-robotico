#!/usr/bin/env python

from Tkinter import *
from tkFileDialog import askopenfilename, asksaveasfilename
from ttk import *
import random
import pickle 

from comunicacion_con_brazo import comunicacion

class Acciones:
	
	def __init__(self):
		"""iniciando la comunicacion con el brazo"""
		self.com=comunicacion()
		
		# ---------------------- Variables -------------------------
		self.tiempo = 1		#Movimientos Bruscos >1s , mov suaves 0.05s
		self.ordenesGrabadas=[]		#Ejemplo: ordenesGrabadas=[("base-izquierda", 1), ("base-derecha",1)]
		self.enGrabacion= False
		self.duration=1.0 # Duration (In seconds) for each action. Defaults to 1 second
		
	
	def actuar(self, comando):
		""" Envia el comando de movimiento al brazo y graba la orden si 
		self.enGrabacion es True """
		self.com.MoveArm(t=self.tiempo, cmd=comando)
		if self.enGrabacion:
			self.actualizarOrdenesGrabadas(comando,self.tiempo)
			
	
	# -----------------------------------------------------------	
	# Proceso de grabacion de ordenes y ejecucion de las mismas
	# -----------------------------------------------------------
	
	def iniciarGrabacion(self):
		self.enGrabacion = True
		
	def pararGrabacion(self):
		self.enGrabacion = False
	
	def actualizarOrdenesGrabadas(self,comando, tiempo):
		self.ordenesGrabadas.append((comando, tiempo))
		self.listaOrdenes.insert(END, comando + " " + str(int(tiempo)) + " seg")
		#print self.ordenesGrabadas
	
	def ejecutarOrdenesGrabadas(self):
		self.pararGrabacion()
		print self.ordenesGrabadas
		print self.enGrabacion
		for orden in self.ordenesGrabadas:
			self.tiempo = orden[1]
			self.actuar(orden[0])
			
	def guardarGrabacion(self):
		archivo = asksaveasfilename()		
		try:
			with open(archivo, 'wb') as mysavedata:
				pickle.dump(self.ordenesGrabadas, mysavedata)
		except IOError as err:
			print('File error: ' + str(err))
		except pickle.PickleError as perr:
			print('Pickling error: ' + str(perr))
		
	def cargarGrabacion(self):
		archivo = askopenfilename()
		try:
			with open(archivo, 'rb') as mysavedata:
				ordenes = pickle.load(mysavedata)
		except IOError as err:
			print('File error: ' + str(err))
		except pickle.PickleError as perr:
			print('Pickling error: ' + str(perr))
		finally:
			self.borrarOrdenesGrabadas()
			for comando in ordenes:
				self.actualizarOrdenesGrabadas(comando[0],comando[1])
			self.tiempo.set(ordenes[0][1])
			
	def borrarOrdenesGrabadas(self):
		self.ordenesGrabadas = []
		self.listaOrdenes.delete(0, self.listaOrdenes.size())
		
		
	def borrarOrden(self,event):
		indice = int(self.listaOrdenes.curselection()[0])
		self.listaOrdenes.delete(indice) 
		del(self.ordenesGrabadas[indice])
		
	
				







	




 

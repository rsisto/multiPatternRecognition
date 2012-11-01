#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Pango is a library for rendering internationalized texts
import pango 
import cairo

import gtk
import gtk.glade
from gettext import gettext as _
from jarabe.model import bundleregistry
import sys,os
import shutil 

import xml.etree.ElementTree as ET

plugin_name = 'pattern'
plugin_folder = 'pattern_detection'

turtlepath = bundleregistry.get_registry().get_bundle('org.laptop.TurtleArtButia').get_path() 
sys.path.insert(0, turtlepath + '/plugins/'+plugin_folder+'/library')


import multiPatternDetectionAPI as detectionAPI     

class ActivityWindows:
	detection = None
	
	def __init__(self, runaslib=True):
		# Load Glade XML
		self.xml = gtk.glade.XML("NewPatternsActivity.glade")
		# get Library
		self.detection = detectionAPI.detection()
		
		# Get Window
		self.w = self.xml.get_widget('window1')
		self.on_load_translate()
		self.w.connect("delete_event", gtk.main_quit)
 		
 		# Get Windows child
		self.w_child = self.w.get_child()
		# self.widget will be attached to the Activity
		# This can be any GTK widget except a window
		self.widget = self.w_child

		if not runaslib:
			self.w.show_all()
			gtk.main()
	
	def on_load_translate(self):
		#TAB 1
 		label = self.xml.get_widget('lblStep1')
  		label.set_label(_("Obtener Patt"))		
		
		txtVew = self.xml.get_widget('txtSteps')
		self.on_load_txt_steps(txtVew)
		
		#TAB 2
		label = self.xml.get_widget('lblStep2')
 		label.set_text(_("Agregar Marca"))
 		
		label = self.xml.get_widget('label5')
 		label.set_text(_("Identificador (sin espacios)"))
 		
		label = self.xml.get_widget('label4')
 		label.set_text(_("Seleccionar archivo .patt"))
 		
 		label = self.xml.get_widget('label6')
 		label.set_text(_("Seleccionar Icono SVG(opcional)"))
 		
 		label = self.xml.get_widget('lblSize')
 		label.set_text(_("Tamaño (mm)"))
		
		btn = self.xml.get_widget('btn_open_patt')
 		btn.set_label(_("Buscar Patt"))
 		btn.connect('clicked', self.file_Open_Patt)
 		
 		btn = self.xml.get_widget('btn_icono')
 		btn.set_label(_("Buscar Icono"))
 		btn.connect('clicked', self.file_Open_Icon)
 		
 		btn = self.xml.get_widget('btn_Acept')
 		btn.set_label(_("Aceptar"))
 		btn.connect('clicked', self.on_btn_accept)
 		
  		btn = self.xml.get_widget('btn_clean')
 		btn.set_label(_("Limpiar Icono"))
 		btn.connect('clicked', self.clean_icon)
 		
 		txtInp = self.xml.get_widget('txtSize')		
 		txtInp.set_text('160')
		#TAB 3
		label = self.xml.get_widget('lblStep3')
 		label.set_text(_("Quitar Marca"))
 		view = self.xml.get_widget('iconview1')
	 	self._on_load_icons(view)
	 	
	def on_btn_accept(self, *args):
		
		idMark =  None
		idMark =  self.xml.get_widget('txtID').get_text()
		if 	idMark is None or idMark == '':
			md = gtk.MessageDialog(None, 
		 	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		 	gtk.BUTTONS_CLOSE, _("Atención, debe selecionar un identificador de marcas"))
		 	md.run()
		 	md.destroy()
		 	return
		 
		if ' ' in idMark:
			md = gtk.MessageDialog(None, 
		 	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		 	gtk.BUTTONS_CLOSE, _("Atención, el identificador no puede tener espacios"))
		 	md.run()
		 	md.destroy()
		 	return
		 
		txtFilePatt = None 
		txtFilePatt = self.xml.get_widget('txtPatt').get_text()
		if 	txtFilePatt is None or txtFilePatt == '':
			md = gtk.MessageDialog(None, 
		 	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		 	gtk.BUTTONS_CLOSE, _("Atención, debes de selcionar un archivo .patt"))
		 	md.run()
		 	md.destroy()
		 	return

		txtSize = None 
		txtSize = self.xml.get_widget('txtSize').get_text()
		if 	txtSize is None or txtSize == '':
			md = gtk.MessageDialog(None, 
		 	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		 	gtk.BUTTONS_CLOSE, _("Atención, debes seleccionar un tamaño de marca valido"))
		 	md.run()
		 	md.destroy()
		 	return		 
		
		#Pongo en mayusculas la primer letra
		idMark = idMark.capitalize()
		
		#chequeco que si existe el id, se quiera sobreescribir
		
		
		
		marcas = self.detection.arMultiGetIdsMarker()
		
		if idMark in marcas:
			md = gtk.MessageDialog(None, 
		 	gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, 
		 	gtk.BUTTONS_YES_NO, _("Atención, ya tienes una marca con ese identificador, ¿deseas sobreescribirla?"))
		 	response = md.run()
		 	md.destroy()
		 	if response == gtk.RESPONSE_NO:
		 		return	
		# modifico el object_data
		lines = []
		try:
			datapath = os.path.abspath(turtlepath + '/plugins/'+plugin_folder+'/library/multiPatternDetection/Data')
			f= open(datapath + "/object_data", "r") 
			lines = f.readlines()
			f.close()
		except:
		   md = gtk.MessageDialog(None, 
		   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		   gtk.BUTTONS_CLOSE, _("Atención, problemas al abrir el archivo de marcas"))
		   md.run()
		   md.destroy()
		   return
		i=0
		try:
			
			i= lines.index("#the number of patterns to be recognized / Cantidad de marcas a ser detectadas (leidos de este mismo archivo en forma secuencial)\n") 
		   	cant = int(lines[i+1]) + 1 
			
		   	lines[i+1]=str(cant)+"\n"
		   	f = open(datapath + "/object_data", "w")
			
		   	coment="patter " + idMark
		   	idMarca=idMark
		   	patt =idMark.lower() + ".patt" 
		   	size = txtSize
			center ="0,0 0,0"
			
			lines.append("\n" )
			lines.append("# " + coment+"\n")
			lines.append(idMarca+"\n")
			lines.append(patt+"\n")
			lines.append(size +"\n")
			lines.append(center+"\n")
			f.writelines(lines)
			f.close() 
		except:
		   md = gtk.MessageDialog(None, 
		   gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, 
		   gtk.BUTTONS_CLOSE, _("Atención, problemas al actualizar el archivo de marcas"))
		   md.run()
		   md.destroy()
		   return
		#copio archivos
		copyFile = datapath + "/" + patt		
		shutil.copy(txtFilePatt, copyFile)
		txtIco = None
		txtIco = self.xml.get_widget('txtIcon').get_text()		  
		if not (txtIco == ''):
			md = gtk.MessageDialog(None, 
								gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
			gtk.BUTTONS_CLOSE, _("entro") + txtIco )
			md.run()
		   	md.destroy()
			self.copy_Icons(txtIco, idMark)
		md = gtk.MessageDialog(None, 
		gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, 
		gtk.BUTTONS_CLOSE, _("Marca agregada satisfactoriamente!"))
		md.run()
		md.destroy()
		self.clean_all()

	def clean_all (self):
		self.clean_icon("")
		self.xml.get_widget('txtSize').set_text('')
 		self.xml.get_widget('txtID').set_text('')
 		self.xml.get_widget('txtPatt').set_text('') 		
 		
 		
 			
	def on_btn_accept_test(self, *args):
		idMark = "PP"
		txtIco = None
		txtIco = self.xml.get_widget('txtIcon').get_text()
		self.copy_Icons(txtIco, idMark)		
	
			  
 	def copy_Icons(self,iconOrig,idMark):
 		
 		imageFolder =  os.path.abspath(turtlepath + '/plugins/'+plugin_folder+'/images')
 		shutil.copy(iconOrig, imageFolder + "/" + idMark + "off.svg")
 		#self.resize_icons(imageFolder + "/" + idMark + "off.svg",70) 			
 		shutil.copy(iconOrig, imageFolder + "/" + idMark + "small.svg")
 		#self.resize_icons(imageFolder + "/" + idMark + "small.svg",40)
 		 	
 	def resize_icons(self,iconToResize,size):
 		f =open(iconToResize,'rb')
 		tree = ET.parse(f)
 		f.close()
 		root = tree.getroot()
 		root.set('width','70')
 		root.set('height','70')
 		print ET.tostring(root)
 		#tree.write(iconToResize, 'UTF-8')
 			
# 		fo = file(iconToResize, 'w')
# 		surface = cairo.SVGSurface (fo, size, size)
# 		ctx = cairo.Context (surface)
# 		ctx.scale (size/1.0, size/1.0)
# 		svg = rsvg.Handle(file=iconToResize)
# 		svg.render_cairo(ctx)
# 		surface.finish() 		
# 			
	def _on_load_icons(self,view):
		model = gtk.ListStore(str, gtk.gdk.Pixbuf)
		view.set_model(model)
		view.set_text_column(0)
		view.set_pixbuf_column(1)
		view.set_columns(4)
		#obtengo la direccion del tortubots
		actBot = None
		actBot = bundleregistry.get_registry().get_bundle('org.laptop.TurtleArtButia')
#        if actBot is not None:
		files = os.listdir(actBot.get_path() + "/plugins/pattern_detection/images")
		for image in files:
			pixbuf = gtk.gdk.pixbuf_new_from_file_at_size(actBot.get_path()+"/plugins/pattern_detection/images/%s" %image, 72, 72) 
			model.append([image, pixbuf])
			model.append([image, pixbuf])
		view.set_selection_mode(gtk.SELECTION_SINGLE)
		view.connect('selection-changed', self.on_select, model)
	
	def on_select(self, icon_view, model=None):
		selected = icon_view.get_selected_items()
		if len(selected) == 0: return
		i = selected[0][0]
		category = model[i][0]
		if self.current_frame is not None:
			self.content_box.remove(self.current_frame)
			self.current_frame.destroy()
			self.current_frame = None
		 
		self.current_frame = gtk.Frame('General')  
		self.content_box.pack_end(self.current_frame, fill=True, expand=True)
		self.show_all()
		
 		
 	def on_load_txt_steps(self,txtVew):
 		buffer = "    1-" + _("Luego de generados los archivos para imprimir, se deberán generar los archivos de patrones.") +"\n"
 		buffer+= "    2-" +_("Ir a la siguiente dirección web: ")+"\n"
 		buffer+= "      " +_("http://www.fing.edu.uy/inco/proyectos/butia/mediawiki/index.php/Generador_de_patrones_para_plugin_Reconocimento_de_marcas ")+"\n"
 		buffer+= "    3-" +_("Seleccionar el origen de donde se generará el patrón. Seleccionar Camera Mode. ")+"\n"
 		buffer+= "    4-" +_("Seleccionar tamaño de patrón, por ejemplo, si el patrón (incluyendo el recuadro negro) mide 16x16 cm, seleccionar 16x16")+"\n"
 		buffer+= "    5-" +_("Seleccionar porcentaje del recuadro que representa el patrón. Por ejemplo, si todo el recuadro mide 16cm y el borde negro mide 2cm, el patrón mide 12x12cm, por lo tanto 75%.")+"\n"
 		buffer+= "    6-" +_("Una vez que se vea un recuadro rojo alrededor de la marca con el rectángulo negro, presionar el botón Get Pattern. Aparecerá un recuadro con los patrones reconocidos, navegar con el botón next al deseado y presionar Save current. Darle un nombre al archivo en minúsculas, con la extensión .patt, por ejemplo mimarca.patt")+"\n"
 		buffer+= "    " +_("Ahora puedes pasar a la siguiente pestaña")+"\n"
 		txtVew.get_buffer().set_text(buffer)
 	
 	def clean_icon(self, *args):
 		txtFileName = self.xml.get_widget('txtIcon') 
 		txtFileName.set_text('')
 		image = self.xml.get_widget('imgIco')
		image.set_property('visible', False)
		btn = self.xml.get_widget('btn_clean')
		btn.set_property('visible', False) 
	
 	def file_Open_Patt(self, *args): 		
	 	filter = gtk.FileFilter()
		filter.set_name(_("Archivos .patt"))
		filter.add_pattern("*.patt")
	 	fname=self._filechosser(_("Cargando archivos .patt"), filter)
	 	if fname != None:
	 		txtFileName = self.xml.get_widget('txtPatt')
	 		txtFileName.set_text(fname)

 	def file_Open_Icon(self, *args): 		
	 	filter = gtk.FileFilter()
		filter.set_name(_("Archivos .svg"))
		filter.add_pattern("*.svg")
	 	fname=self._filechosser(_("Cargando archivos .svg"), filter)
	 	if fname != None:
	 		txtFileName = self.xml.get_widget('txtIcon')
	 		txtFileName.set_text(fname)
	 		image = self.xml.get_widget('imgIco')
	 		pixbuf = gtk.gdk.pixbuf_new_from_file(fname)
			scaled_buf = pixbuf.scale_simple(72,72,gtk.gdk.INTERP_BILINEAR)
			image.set_from_pixbuf(scaled_buf)
			image.show()
			btn = self.xml.get_widget('btn_clean')
			btn.show()
	 	
	def _filechosser(self, ventana_titulo,filter):
		dialog = gtk.FileChooserDialog(ventana_titulo, None, \
		      gtk.FILE_CHOOSER_ACTION_OPEN, \
		     (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,gtk.STOCK_OPEN, gtk.RESPONSE_OK))    
		dialog.set_default_response(gtk.RESPONSE_OK)
		
		dialog.add_filter(filter)
		fname = None
		response = dialog.run()
		if response == gtk.RESPONSE_OK:   
			fname = dialog.get_filename()
		dialog.destroy() 
		return fname
 		
	
	def on_btn_hello(self, *args):		
		 md = gtk.MessageDialog(None, 
		 gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_QUESTION, 
		 gtk.BUTTONS_OK_CANCEL, "Are you sure to quit?")
		 md.run()
		 md.destroy()
	
	def on_btn_quit(self, *args):
		gtk.main_quit()
 
       
        			
if __name__ == '__main__':
	ActivityWindows(False)
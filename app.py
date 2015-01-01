__author__ = 'Kibur'

import os
import io
from gi.repository import Gtk
import binascii

def readImage(path):
	with open(path) as f:
		return bytearray(f.read())

class UI:
	def add_filters(self, dialog):
		filter_image = Gtk.FileFilter()
		filter_image.set_name('Image files')
		filter_image.add_mime_type('image/bmp')
		filter_image.add_mime_type('image/gif')
		filter_image.add_mime_type('image/jpeg')
		filter_image.add_mime_type('image/png')
		
		filter_image.add_pattern('*.bmp')
		filter_image.add_pattern('*.gif')
		filter_image.add_pattern('*.jpg')
		filter_image.add_pattern('*.jpeg')
		filter_image.add_pattern('*.jpe')
		filter_image.add_pattern('*.png')

		dialog.add_filter(filter_image)

	# Handlers
	def window_close(self, *args):
		Gtk.main_quit(args)

	def on_button_clicked(self, widget):
		dialog = Gtk.FileChooserDialog('Please choose an image', None,\
			 Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL,\
			 Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN,\
			 Gtk.ResponseType.OK))

		self.add_filters(dialog)

		response = dialog.run()

		if response == Gtk.ResponseType.OK:
			self.on_open_clicked(dialog)
		elif response == Gtk.ResponseType.CANCEL:
			pass

		dialog.destroy()

	def on_open_clicked(self, dialog):
		path = dialog.get_filename()

		self.lblPath.set_text(path)

		data = '0x'
		data += binascii.hexlify(readImage(path))
		textBuffer = self.txtOutput.get_buffer()

		textBuffer.set_text(data)
	# ---

	def connectHandlers(self):
		self.window.connect('delete-event', self.window_close)
		self.btnBrowse.connect('clicked', self.on_button_clicked)

	def retreiveObjects(self):
		self.window = self.builder.get_object('window1')
		self.btnBrowse = self.builder.get_object('btnBrowse')
		self.lblPath = self.builder.get_object('lblPath')
		self.txtOutput = self.builder.get_object('txtOutput')

	def __init__(self):
		self.builder = Gtk.Builder()
		self.builder.add_from_file('view.glade')

		self.retreiveObjects()
		self.connectHandlers()

		self.window.__init__(self, title='Image to byte array')

		self.window.show()

if __name__ == "__main__":
	ui = UI()
	Gtk.main()

from ._anvil_designer import ElementEditTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ElementEdit(ElementEditTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

    def file_loader_change(self, file, **event_args):
        """This method is called when a new file is loaded into this FileLoader"""
        self.item['image'] = file


from ._anvil_designer import ElementViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ElementView(ElementViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.

    def delete_element_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        if confirm("Вы действительно хотите удалить {}?".format(self.item['name'])):
            self.parent.raise_event('x-delete-element', element=self.item)


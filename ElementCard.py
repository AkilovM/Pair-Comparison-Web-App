from ._anvil_designer import ElementCardTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ElementCard(ElementCardTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.

    def add_1_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.server.call('add_1_rating', self.item, 1)
        anvil.open_form('PairComparisonForm', self.item['element']['collection'], anvil.users.get_user())
        pass


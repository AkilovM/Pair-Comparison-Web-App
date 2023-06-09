from ._anvil_designer import CollectionButtonViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CollectionButtonView(CollectionButtonViewTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run when the form opens.

    def collection_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('CollectionView', collection=self.item)


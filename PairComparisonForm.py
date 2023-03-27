from ._anvil_designer import PairComparisonFormTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class PairComparisonForm(PairComparisonFormTemplate):
    def __init__(self, collection, user, **properties):
        # Set Form properties and Data Bindings.
        self.collection = collection
        self.user = user
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.get_pair()

    def get_pair(self):
        pair = anvil.server.call('get_comparison_pair', self.collection, self.user)
        if pair != 1:
            self.element_1.item = pair[0]
            self.element_2.item = pair[1]
        else:
            self.element_1.visible = False
            self.element_2.visible = False
            self.label_1.text = 'Попарное сравнение завершено.'

    def add_one(self, rat, val):
        anvil.server.call('add_1_rating', rat, val)

    def return_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('CollectionView', self.collection)

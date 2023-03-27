from ._anvil_designer import RatingsViewTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RatingsView(RatingsViewTemplate):
    def __init__(self, collection, mode, **properties):
        # Set Form properties and Data Bindings.
        self.collection = collection
        self.mode = mode
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.get_ratings()

    def get_ratings(self):
        if self.mode == 'personal':
            self.label_2.text = 'Ваш персональный результат'
            self.repeating_panel_1.items = anvil.server.call('get_personal_ratings', self.collection, anvil.users.get_user())
        elif self.mode == 'overall':
            self.label_2.text = 'Результат среди всех пользователей'
            self.repeating_panel_1.items = anvil.server.call('get_overall_ratings', self.collection)

    def return_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('CollectionView', self.collection)

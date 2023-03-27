from ._anvil_designer import CollectionViewTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..ElementEdit import ElementEdit

class CollectionView(CollectionViewTemplate):
    def __init__(self, collection, **properties):
        self.collection = collection
        self.user = anvil.users.get_user()
        self.coll_usr = anvil.server.call('get_collection_user', self.collection, self.user)
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        self.refresh_elements()
        self.elements_repeating_panel.set_event_handler('x-delete-element', self.delete_element)
        if self.coll_usr['status'] == 'done':
            self.pair_comparison_label.text = 'Попарное сравнение завершено'
            self.pair_comparison_button.enabled = False
            self.my_rating_button.enabled = True

    def refresh_elements(self):
        self.elements_repeating_panel.items = anvil.server.call('get_elements', self.collection)
    
    def return_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('AllCollections')

    def create_element_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        new_element = {'collection':self.collection}
        if alert(content=ElementEdit(item=new_element), title='Новый элемент', 
                 buttons=[('Сохранить', True), ('Отмена', False)], large=True):
            anvil.server.call('create_element', new_element)
            self.refresh_elements()

    def delete_element(self, element, **event_args):
        anvil.server.call('delete_element', element)
        self.refresh_elements()

    def pair_comparison_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('PairComparisonForm', self.collection, self.user)

    def my_rating_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('RatingsView', self.collection, 'personal')

    def overall_rating_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.open_form('RatingsView', self.collection, 'overall')

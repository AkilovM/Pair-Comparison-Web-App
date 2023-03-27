from ._anvil_designer import AllCollectionsTemplate
from anvil import *
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..CollectionEdit import CollectionEdit

class AllCollections(AllCollectionsTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        user = anvil.users.get_user()
        if user == None:
            user = anvil.users.login_with_form()
        if user == None:
            anvil.open_form('AllCollections')
        self.init_components(**properties)

        # Any code you write here will run when the form opens.
        self.refresh_collections()


    def refresh_collections(self):
        self.colls_repeating_panel.items = anvil.server.call('get_collections')
    
    def create_collection_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        new_collection = {}
        if alert(content=CollectionEdit(item=new_collection), title='Новая коллекция', 
                 buttons=[('Сохранить', True), ('Отмена', False)], large=True):
            anvil.server.call('create_collection', new_collection)
            self.refresh_collections()

    def logout_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        anvil.users.logout()
        anvil.open_form('AllCollections')

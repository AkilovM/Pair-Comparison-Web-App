import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def get_collections():
    return tables.app_tables.collections.search()

@anvil.server.callable
def create_collection(collection_dict):
    tables.app_tables.collections.add_row(**collection_dict)

@anvil.server.callable
def get_elements(coll):
    return tables.app_tables.elements.search(collection=coll)

@anvil.server.callable
def create_element(element_dict):
    tables.app_tables.elements.add_row(**element_dict)

def create_collection_user(coll_usr_dict):
    tables.app_tables.collection_user.add_row(**coll_usr_dict)

def create_rating(rat_dict):
    tables.app_tables.rating.add_row(**rat_dict)

@anvil.server.callable
def get_collection_user(coll, usr):
    coll_usr = tables.app_tables.collection_user.get(collection=coll, user=usr)
    if coll_usr == None:
        coll_usr = {'collection':coll,
                   'user':usr,
                   'status':'comparing',
                   'max_value':1}
        create_collection_user(coll_usr)
        elements = get_elements(coll)
        for e in elements:
            rating = {'element':e,
                     'user':usr,
                     'value':0}
            create_rating(rating)
    return tables.app_tables.collection_user.get(collection=coll, user=usr)

@anvil.server.callable
def add_1_rating(rating, one):
    v = rating['value']
    rating.update(value=v+one)

@anvil.server.callable
def get_comparison_pair(coll, usr):
    coll_usr = get_collection_user(coll, usr)
    elements = list(get_elements(coll))
    max_value = coll_usr['max_value']
    comp_elems = tables.app_tables.rating.search()
    comp_elems = [x for x in comp_elems
                 if x['element'] in elements
                 and x['value'] >= max_value-1
                 and x['user'] == usr]
    n = len(comp_elems)
    while n > 1:
        for i in range(0, n-1, 2):
            if comp_elems[i]['value'] == max_value-1 and comp_elems[i+1]['value'] == max_value-1:
                return (comp_elems[i], comp_elems[i+1])
        coll_usr.update(max_value=max_value+1)
        coll_usr = get_collection_user(coll, usr)
        max_value = coll_usr['max_value']
        comp_elems = tables.app_tables.rating.search()
        comp_elems = [x for x in comp_elems
                    if x['element'] in elements
                    and x['value'] >= max_value-1
                    and x['user'] == usr]
        n = len(comp_elems)
    coll_usr.update(status='done')
    return 1

@anvil.server.callable
def get_personal_ratings(coll, usr):
    ratings = app_tables.rating.search(user=usr)
    ratings = [x for x in ratings
              if x['element']['collection'] == coll]
    ratings = sorted(ratings, key=lambda d: d['value'], reverse=True)
    res_list = list()
    for i in range(len(ratings)):
        rat_dict = {'place':i+1,
                   'image':ratings[i]['element']['image'],
                   'name':ratings[i]['element']['name'],
                   'value':ratings[i]['value']}
        res_list.append(rat_dict)
    return res_list

@anvil.server.callable
def get_overall_ratings(coll):
    elements = list(get_elements(coll))
    ratings = app_tables.rating.search()
    ratings = [x for x in ratings
               if x['element']['collection'] == coll]
    temp_list = list()
    for e in elements:
        elem_rat = [x for x in ratings
                   if x['element'] == e]
        value = 0
        for r in elem_rat:
            value += r['value']
        temp_list.append({'element':e,
                         'value':value})
    temp_list = sorted(temp_list, key=lambda d: d['value'], reverse=True)
    res_list = list()
    for i in range(len(temp_list)):
        rat_dict = {'place':i+1,
                   'image':temp_list[i]['element']['image'],
                   'name':temp_list[i]['element']['name'],
                   'value':temp_list[i]['value']}
        res_list.append(rat_dict)
    return res_list

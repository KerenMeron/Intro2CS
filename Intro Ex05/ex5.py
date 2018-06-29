#############################################################
# FILE :ex5.py
# WRITER :Keren Meron, keren.meron, 200039626
#         and  Eldan Chodorov , eldan , 201335965
# EXERCISE : intro2cs ex5 2015-2016
# DESCRIPTION:
# The program is designed to help the user find a store
# where he could buy his list of products in the cheapest price.
# The user can load XML files (supplied by the store) containing a data
# structure of items and their properties from a chosen store.
# The user can load several lists into the the program, and select different
# items which s/he is interested in comparing. The program will find
# the cheapest store for the user to shop at.
# Other features include the option to save the formed shopping cart, and
# reload a cart previously saved.
#############################################################

import xml.etree.ElementTree as ET

ITEM_CODE = 'ItemCode'
ITEM_NAME = 'ItemName'
ITEM_PRICE = 'ItemPrice'
ITEM = 'Item'
STORE_ID = 'StoreId'
NULL = 0
#1
def get_attribute(store_db, ItemCode, tag):
    '''
    :param store_db: a dictionary (store) of dictionaries (items)
    :param ItemCode: string
    :param tag: string
    :return: Returns the attribute (tag)
    of an Item with code: Itemcode in the given store
    '''
    attribute = store_db[ItemCode][tag]
    return attribute

#2
def string_item(item):
    '''
    :param item: Dictionary with the characteristics of item
    :return: Textual representation of an item in a store.
    Returns a string in the format of '[ItemCode] (ItemName)'
    '''
    if len(item) == NULL:
        return None
    else:
        item_code = []
        item_code.append(int(item[ITEM_CODE]))
        item_name = item[ITEM_NAME].strip('"').strip()
        return str(item_code) + '\t' + "{" + item_name + "}"

#3
def string_store_items(store_db):
    '''
    :param store_db: dictionary of dictionaries as created in read_prices_file
    filter_txt: the filter text as given by the user.
    :return: Returns a string in the format of:
    string representation of item1
    string representation of item2
    etc.
    '''
    items_rep = ''

    if len(store_db) == NULL:
        return items_rep

    for item in store_db:
        if len(item) == NULL:
            continue
        temp_dict = store_db[item]
        items_rep += string_item(temp_dict) + '\n'

    return items_rep

#4
def read_prices_file(filename):
    '''
    :param filename: file of items and date about the item like prices.
    The file is assumed to be in the standard XML format of "misrad hacalcala"
    :return:a tuple: store_id and a store_db,
    where the first variable is the store name
    and the second is a dictionary describing the store.
    The keys in this db will be ItemCodes of the different items and the
    values smaller dictionaries mapping attribute names to their values.
    Important attributes include 'ItemCode', 'ItemName', and 'ItemPrice'
    '''
    tree = ET.parse(filename)
    root = tree.getroot()
    store_id = root.find(STORE_ID).text
    store_inventory = dict()

    for item in root.iter(ITEM):
       list_info = dict()
       for key in item:
           list_info[key.tag] = key.text
       store_inventory[item.find(ITEM_CODE).text] = list_info

    return store_id, store_inventory

#5
def filter_store(store_db, filter_txt):
    '''
    :param store_db: dictionary of dictionaries as created in read_prices_file
    filter_txt: the filter text as given by the user.
    :param filter_txt: items that text given by the user is part of
                        their ItemName
    :return: Create a new dictionary that includes only the items
    that were filtered by user.
    '''
    filtered_store_db = {}

    for item in store_db:
        if filter_txt in store_db[item][ITEM_NAME]:
            filtered_store_db[item] = store_db[item]

    return filtered_store_db

#6
def create_basket_from_txt(basket_txt):
    '''
    :param basket_txt: text representation of few items (and maybe some
    garbage at the edges
    :return:a basket- list of ItemCodes that were included in basket_txt
    '''
    list_of_item = basket_txt.split()
    basket = []

    for item in list_of_item:
        if item[0] == "[" and item[-1] == "]":
            item = item.strip("[").strip("]").strip("'").strip()
            basket.append(item)

    return basket

#7
def get_basket_prices(store_db, basket):
    '''
    :param store_db: dictionary of dictionaries
    :param basket: a list of ItemCodes
    :return: Go over all the items in the basket and create a new list
    that describes the prices of store items
    In case one of the items is not part of the store,
    its price will be None.
    '''
    price_list = []

    for item_code in basket:
        item_code = store_db.get(item_code)
        if item_code:
            price_list.append(float(item_code[ITEM_PRICE]))
        else:
            price_list.append(item_code)

    return price_list

#8
def sum_basket(price_list):
    '''
    :param price_list: a list of prices
    :return:a tuple - the sum of the list (when ignoring Nones)
    and the number of missing items (Number of Nones)
    '''
    price_sum = NULL
    missing_items = NULL

    for price in price_list:
        if not price:
            missing_items += 1
            continue
        price_sum += price

    return price_sum, missing_items

#9
def basket_item_name(stores_db_list, ItemCode):
    '''
    :param stores_db_list:  a list of stores (list of dictionaries of
      dictionaries)
    :param ItemCode:  a str Representing a product number in the basket
    :return:the first store in the list that contains the item and return its
    string representation (as in string_item())
    If the item is not available in any of the stores return only [ItemCode]
    '''
    for (index, store) in enumerate(stores_db_list):
        item_code = stores_db_list[index].get(ItemCode)
        if item_code:
            return string_item(store[ItemCode])

    return '['+ItemCode+']'

#10
def save_basket(basket, filename):
    '''
    :param basket: list of ItemCodes that were included by the user
    :param filename: a  File name into which information of the itemcode that
    was Chosen by the user
    :return: a file The basket reresentation in the file will be
    in the following format:
    [ItemCode1]
    ...
    [ItemCodeN]
    '''
    with open (filename, 'a') as filename:
        for ItemCode in basket:
            filename.write('[' + ItemCode + ']' + '\n')
        filename.close()

#11
def load_basket(filename):
    '''
    :param filename:A file that stores data in the same way saved in function
    (save_basket(basket, filename))
    :return:a list of ItemCodes from the given file.
    The file is assumed to be in the format of:
    [ItemCode1]
    ...
    [ItemCodeN]
    '''
    item_code_list = []

    with open (filename,'r') as filename:
        new_file = (filename.readlines())
        for item_code in new_file:
            item_code_list.append(item_code.strip("[").strip("]\n"))
        filename.close()

        return item_code_list

#12
def best_basket(list_of_price_list):
    '''
    :param list_of_price_list: list of lists, where each inner list
    is list of prices as created by get_basket_prices.
    :return: the cheapest store (index of the cheapest list) given that a
    missing item has a price of its maximal price in the other stores *1.25
    '''

    #creates list of price sum for each store
    sum_list = [NULL] * len(list_of_price_list)
    for (i, store) in enumerate(list_of_price_list):
        for (j, item) in enumerate(store):
            if item:
                sum_list[i] += item

    #creates list of max price of each item
    max_list = [NULL] * len(list_of_price_list[0])
    for (i, store) in enumerate(list_of_price_list):
        for (j, item) in enumerate(store):
            if not item:
                continue
            elif item > max_list[j]:
                max_list[j] = item

    #if item doesn't exist, adds fine to price sum of store
    for (i, store) in enumerate(list_of_price_list):
        for (j, item) in enumerate(store):
            if not item:
                sum_list[i] += (max_list[j] + max_list[j]/4)

    #finds index of store with cheapest price sum
    cheapest = sum_list.index(min([k for k in sum_list]))
    return cheapest


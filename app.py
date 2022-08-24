# Create 2 databases, name fruits and clothes (create at least 2 collections and populate with 25-50 (random number in that range) items in each collection).
# Item descriptors are {name, weight, cost, size, color} if appliacable. (Price, weight, size range is 9.99 < price < 99.99)
# Get me a report of each collection:
# - how many items there are in a each collection
# - what is an average price for the item in that collection
# - report cheapest/most expensive item from those collections.
# - report heaviest/lightest item from those collections.
# - get all monetary value of all items from all collections
# All data must be aquired from running database :)

from typing import Collection
from pymongo import MongoClient
from random_word import RandomWords
from random import randint, uniform, shuffle
from datetime import datetime
from statistics import mean

def random_color() -> tuple:
    rgbl=[255,0,0]
    shuffle(rgbl)

def record_creator() -> dict:
    x = RandomWords()
    name = x.get_random_word()
    weight = round(uniform(9.99, 99.99), 2)
    cost = round(uniform(9.99, 99.99), 2)
    size = round(uniform(9.99, 99.99), 2)
    color = random_color()
    record = {'brand': name, 'weight': weight, 'cost': cost, 'size': size, 'color': color}
    return record

client = MongoClient('localhost', 37017)
db_clothes = client['Clothes']
collection_clothes = db_clothes['Most_sold']
collection_clothes_2 = db_clothes['Least_sold']

client = MongoClient('localhost', 37017)
db_fruits = client['Fruits']
collection_fruits = db_fruits['Most_sold']
collection_fruits_2 = db_fruits['Least_sold']

all_collections = [collection_clothes, collection_clothes_2, collection_fruits, collection_fruits_2]

def main():
    for _ in range(randint(25, 50)):
        collection_clothes.insert_one(record_creator())

    for _ in range(randint(25, 50)):
        collection_clothes_2.insert_one(record_creator())

    for _ in range(randint(25, 50)):
        collection_fruits.insert_one(record_creator())

    for _ in range(randint(25, 50)):
        collection_fruits_2.insert_one(record_creator())

def collection_item_count(selected_collection: Collection) -> None:
        return f"{len([x for x in selected_collection.find()])}"

def average_item_price(selected_collection: Collection) -> None:
        result = [item['cost'] for item in [x for x in selected_collection.find()]]
        return f"Collection average item price: ${round(mean(result), 2)}"

def most_expensive_item_price(selected_collection: Collection) -> None:
        result = max([item['cost'] for item in [x for x in selected_collection.find()]])
        return f"Collection most expensive item: ${result}"

def cheapest_item_price(selected_collection: Collection) -> None:
        result = min([item['cost'] for item in [x for x in selected_collection.find()]])
        return f"Collection cheapest item: ${result}"

def heaviest_item_price(selected_collection: Collection) -> None:
        result = max([item['weight'] for item in [x for x in selected_collection.find()]])
        return f"Collection heaviest item: {result}kg"

def lightest_item_price(selected_collection: Collection) -> None:
        result = min([item['weight'] for item in [x for x in selected_collection.find()]])
        return f"Collection lightest item: {result}kg"

def all_value() -> float:
    overall_value = 0
    for collection in all_collections:
        my_list = [x for x in collection.find()]
        result = sum([item['cost'] for item in my_list])
        overall_value = overall_value + result
    return f"Overall collection value ${round(overall_value, 2)}"

def write_information_to_file(data: str) -> None:
    with open("collection_report.txt", 'a') as f:
        f.write(data)

main()

write_information_to_file(f"""Information date: {datetime.now()}

Collection Clothes most sold item count: {collection_item_count(collection_clothes)} 
{average_item_price(collection_clothes)}
{most_expensive_item_price(collection_clothes)}
{cheapest_item_price(collection_clothes)}
{heaviest_item_price(collection_clothes)}
{lightest_item_price(collection_clothes)}

Collection Clothes least sold item count: {collection_item_count(collection_clothes_2)} 
{average_item_price(collection_clothes_2)}
{most_expensive_item_price(collection_clothes_2)}
{cheapest_item_price(collection_clothes_2)}
{heaviest_item_price(collection_clothes_2)}
{lightest_item_price(collection_clothes_2)}

Collection Fruits most sold item count: {collection_item_count(collection_fruits)} 
{average_item_price(collection_fruits)}
{most_expensive_item_price(collection_fruits)}
{cheapest_item_price(collection_fruits)}
{heaviest_item_price(collection_fruits)}
{lightest_item_price(collection_fruits)}

Collection Fruits least sold item count: {collection_item_count(collection_fruits_2)} 
{average_item_price(collection_fruits_2)}
{most_expensive_item_price(collection_fruits_2)}
{cheapest_item_price(collection_fruits_2)}
{heaviest_item_price(collection_fruits_2)}
{lightest_item_price(collection_fruits_2)}

{all_value()}\n\n\n""")


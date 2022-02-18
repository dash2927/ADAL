import re
import sys
import pickle
import sqlite3
from recipe import entryRecipe


def load_db(file='../data'):
    # Load and save are NOT databases, however, for the time they can
    # replace our db. These should be replaced ASAP as pickle can
    # be an unsafe method of storage.
    try:
        with open(file, 'rb') as f:
            data = pickle.load(f)
    except Exception as e:
        print(f"Error when loading data ({e}). Continung with an empty dict")
        data = {}
    return data


def save_db(data):
    with open('../data', 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


def parse_info(file):
    with open(file, 'rb') as f:
        rectxt = f.read().decode('utf-8')
    name = re.findall(r"(?<=NAME:\n)(.*)(?=\nCUISINE)", rectxt)
    cuisine = re.findall(r"(?<=CUISINE:\n)(.*)(?=\nDESCRIPTION)", rectxt)
    desc = re.findall(r"(?<=DESCRIPTION:\n)([\S\s]*)(?=\nTAGS)", rectxt)
    tags = re.findall(r"(?<=TAGS:\n)([\S\s]*)(?=\nINGREDIENTS)",
                      rectxt)
    if len(tags) > 0:
        tags = tags[0].split(", ")
    ing = re.findall(r"(?<=INGREDIENTS:\n)([\S\s]*)(?=\nRECIPE)",
                     rectxt)[0].split("\n")
    recp = re.findall(r"(?<=RECIPE:\n)([\S\s]*)", rectxt)

    new_recipe = entryRecipe(name[0])
    new_recipe.set_cuisine(cuisine[0])
    new_recipe.set_desc(desc[0])
    new_recipe.set_tags(tags)
    new_recipe.set_ingredients(ing)
    new_recipe.set_recipe(recp[0])
    return new_recipe
    '''print(new_recipe.get_recipe())
    print(new_recipe.get_desc())
    print(new_recipe.get_cuisine())
    new_recipe.add_tag("LAMB")
    print(new_recipe.get_tags())
    print(new_recipe.get_ingredients())
    print(new_recipe.get_uID())
    '''


def get_entry(entry):
    data = load_db()
    entry = int(entry)
    if entry not in data:
        lst = []
        for e in data:
            if str(e).startswith(str(entry)):
                lst.append(e)
        if len(lst) == 1:
            data[lst[0]].print()
            return
        if len(lst) > 1:
            print("Multiple entries found:")
            for i in lst:
                print_entry(data[i])
        else:
            print("No entry found with that key")
            sys.exit()
    else:
        data[entry].print()


def print_entry(rec):
    print(f'{rec.get_uID()} [{rec.name}] {rec.get_rating()} ' +
          f'{rec.get_cuisine()} {rec.get_tags()}')


def add_entry(file):
    data = load_db()
    new_recipe = parse_info(file)
    print(new_recipe.get_uID())
    if data.get(new_recipe.get_uID()):
        print("ERROR: Recipe already in the database")
    else:
        data[new_recipe.get_uID()] = new_recipe
    save_db(data)


def addtag(entry, tag):
    data = load_db()
    entry = int(entry)
    if entry not in data:
        lst = []
        for e in data:
            if str(e).startswith(str(entry)):
                lst.append(e)
        if len(lst) == 1:
            data[lst[0]].add_tag(tag)
            save_db(data)
            return
        if len(lst) > 1:
            print("Multiple entries found:")
            for i in lst:
                print_entry(data[i])
        else:
            print("No entry found with that key")
    else:
        data[entry].add_tag(tag)
        save_db(data)


def upvote(entry):
    data = load_db()
    entry = int(entry)
    if entry not in data:
        lst = []
        for e in data:
            if str(e).startswith(str(entry)):
                lst.append(e)
        if len(lst) == 1:
            data[lst[0]].inc_rating()
            save_db(data)
            return
        if len(lst) > 1:
            print("Multiple entries found:")
            for i in lst:
                print_entry(data[i])
        else:
            print("No entry found with that key")
    else:
        data[entry].inc_rating()
        save_db(data)


def downvote(entry):
    data = load_db()
    entry = int(entry)
    if entry not in data:
        lst = []
        for e in data:
            if str(e).startswith(str(entry)):
                lst.append(e)
        if len(lst) == 1:
            data[lst[0]].dec_rating()
            save_db(data)
            return
        if len(lst) > 1:
            print("Multiple entries found:")
            for i in lst:
                print_entry(data[i])
        else:
            print("No entry found with that key")
    else:
        data[entry].dec_rating()
        save_db(data)


def rm_entry(entry):
    data = load_db()
    entry = int(entry)
    if entry not in data:
        lst = []
        for e in data:
            if str(e).startswith(str(entry)):
                lst.append(e)
        if len(lst) == 1:
            data.pop(lst[0])
            save_db(data)
            return
        if len(lst) > 1:
            print("Multiple entries found:")
            for i in lst:
                print_entry(data[i])
        else:
            print("No entry found with that key")
    else:
        data.pop(entry)
        save_db(data)


def get_all():
    data = load_db()
    for entry in data:
        print_entry(data[entry])


def help():
    hlp = {'--add-entry': "Add a recipe to the database. Requires a " +
           "specifically formated text file",
           '--get-all': "Get all recipe entries",
           '--get-entry': "Get a specific entry based on the Uid",
           '--remove-entry': "Remove an entry based on the Uid",
           '--downvote': "Downvote a recipe based on Uid",
           '--upvote': "Upvote a recipe based on Uid",
           '--add-tag': "Add a 10 character tag to recipe based on Uid"}
    for h in hlp:
        print(f'{h} | {hlp[h]}')

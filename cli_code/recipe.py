import hashlib
'''
TODO:
    * finish recipe class
    * implement command line commands
    * make test cases
    * Create examples from internet (just c/p stuff)
    * implement a dictionary lookup based on uID
    * implement an easy way to save - probably pickle despite drawbacks
    ? maybe implement a dictionary lookup based on ingredients
    * clean up code
'''


class entryRecipe:
    def __init__(self, name):
        self.name = name
        self.ing = dict()
        self.cuisine = ""
        self.desc = ""
        self.__uID = -1
        self.__recipe = ""
        self.__rating = 0
        self.__tag = []
        self.__servings = 1

    def set_recipe(self, recipe):  # Use setter so we can create UID
        self.__recipe = recipe
        if self.__uID == -1:  # UID is not set, this is a new entry
            self.__uID = int(hashlib.sha256((self.name +
                                             recipe).encode('utf-8')).hexdigest()[:10],
                             16)

    def get_recipe(self, servings=1):
        return self.__recipe

    def set_ingredients(self, ings):
        for ing in ings:
            sing = ing.split(" ")
            amt = (sing[0], sing[1])
            self.ing[" ".join(sing[2:])] = amt

    def get_ingredients(self):
        ingstr = []
        for ing in self.ing:
            ingstr.append(self.ing[ing][0] + " " + self.ing[ing][1] +
                          " " + ing)
        return "\n".join(ingstr)

    def set_desc(self, desc):
        self.desc = desc

    def get_desc(self):
        return self.desc

    def set_rating(self, rating):
        assert rating >= 0, "Rank needs to be >= 0"
        self.__rating = rating

    def get_rating(self):
        return self.__rating

    def inc_rating(self):
        self.__rating += 1

    def dec_rating(self):
        if self.__rating > 0:
            self.__rating -= 1

    def set_cuisine(self, cuisine):
        self.__cuisine = cuisine

    def get_cuisine(self):
        return self.__cuisine

    def add_tag(self, tag):
        if type(tag) is not str:
            tag = str(tag)
        tag.strip()
        assert len(tag) <= 10, "Tags are meant to be short, <10 characters"
        self.__tag.append(tag)

    def set_tags(self, tag):
        self.__tag = tag

    def get_tags(self):
        return self.__tag

    def get_uID(self):
        return self.__uID



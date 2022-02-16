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


class recipe():
    def __init__(self, name):
        self.name = name
        self.__uID = -1
        self.__recipe = ""
        self.__cuisine = ""
        self.__rating = 0
        self.__tag = []
        self.__servings = 1
        self.__ingredients = set()

    def set_recipe(self, recipe):  # Use setter so we can create UID
        self.__recipe = recipe
        if self.__uID == -1:  # UID is not set, this is a new entry
            self.__uID = hash(self.name + recipe)

    def get_recipe(self, servings=self.__servings):
        pass

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

    def get_tag(self):
        return self.__tag

    def get_uID(self):
        return self.__uID


if __name__ == "__main__":
    pass



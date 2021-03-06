# Add an `Item` class in a file `item.py`.

# This will be the _base class_ for specialized item types to be declared
# later.

# The item should have `name` and `description` attributes.

# Hint: the name should be one word for ease in parsing later.

class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description
    
    def __repr__(self):
        return self.name

class Treasure(Item):
    def __init__(self, name, description, value):
        Item.__init__(self, name, description)
        self.value = value
        self.dropped = False

    def on_take(self):
        return self.value

    def on_drop(self):
        return self.value

class LightSource(Item):
    def __init__(self, name, description):
        Item.__init__(self, name, description)
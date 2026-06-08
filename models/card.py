class Card():
    def __init__(self, color:str ="", figure:str ="", value:str = "", name:str =""):
        self.color = color
        self.figure = figure
        self.value = value
        self.color_text = name
        self.name = self.figure + name

    def __str__(self):
        return self.name
    
    def get_value(self):
        """getter"""
        return self.value
    
    def set_value(self, new_value):
        """setter"""
        self.value = new_value
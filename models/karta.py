class Card():
    def __init__(self, color="", figure="", value="", name=""):
        self.color = color
        self.figure = figure
        self.value = value
        self.color_text = ""
        self.name = self.figure + name

    def __str__(self):
        return self.name
    
    def get_value(self):
        """getter"""
        return self.value
    
    def set_value(self, new_value):
        """setter"""
        self.value = new_value
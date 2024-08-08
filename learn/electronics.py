from products import Products

class Electronics(Products):
    category = "Electronics"
    category_code = "E"

    def __init__(self, name, cost_price, mrp, quantity, power_option):
        super().__init__(name, cost_price, mrp, quantity)
        self.power_option = power_option
        self.__offers = 5

    def show_details(self):
        super().show_details()
        print(f"Power: {self.power_option}")
        print("-" * 55)

    @property
    def schemes(self):
        return self.__offers
    
    @schemes.setter
    def schemes(self, newValue):
        self.__offers = newValue

    @classmethod
    def addNewItem(cls):
        name, cost_price, mrp, quantity = super().addNewItem()
        power_option = input("Power option: ")
        return cls(name, cost_price, mrp, quantity, power_option)

    def editDetails(self):
        super().editDetails()
        power = input(f"Power\t{self.power_option}:\t")
        if power:
            self.power_option = power

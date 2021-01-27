import pickle
import readchar
import time
import os


class menu_generator :

    def __init__(self) :
        self.message="q to quit"

    def visualize_menu(self, options, index, instructions="") :
        os.system('clear')
        print("")
        print(color.CYAN + self.message + color.END)
        print(color.DARKCYAN + instructions +color.END, end="\n-")

        for i in range(0,len(options)) :
            if i==index :
                print(color.PURPLE + options[i] + color.END, end=" ")
            else :
                print(options[i],end=" ")
        print("")


    def menu(self, options, instructions="") :
        menu_index=0
        while True :
            self.visualize_menu(options, menu_index, instructions=instructions)
            try :
                key=readchar.readkey()
                if key=='a' or  key == readchar.key.LEFT :
                    menu_index-=1
                elif key=='d' or key == readchar.key.RIGHT:
                    menu_index+=1
                elif key=='q' :
                    break
                elif key=='e' or key == readchar.key.ENTER:
                    return menu_index
                menu_index=menu_index%len(options)
                time.sleep(.1)

            except KeyboardInterrupt:
                pass


class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


class recipe :
    def __init__(self, name, book, page_num, method) :
        self.name=name
        self.book=book
        self.page=page_num
        self.method=method
        self.ingredients={}
        self.rating=None

    def add_ingredient(self, quantity, substance) :
            self.ingredients[substance]=quantity

    def print(self) :
        print(color.BOLD +color.BLUE+ self.name+ color.END)
        print(color.BLUE+"page "+self.page +"\nmethod " +self.method +color.END)
        print("INGREDIENTS")
        for ingredient in self.ingredients.keys() :
            print(" " + color.YELLOW +self.ingredients[ingredient] + " - " + ingredient + color.END)
        print("\n")

class drink_index :
    def __init__(self, recipes={}) :
        self.recipes=recipes

        self.curr_book=None;
        self.curr_method=None;
        self.last_page_number=None
        self.menu=menu_generator()

    def clear(self) :
         os.system('clear')


    def input_drink(self) :
        if self.curr_book==None :
            self.set_book()
        if self.curr_method==None :
            self.set_method()

        try:
            page_num=input("Please input the page number(defualt {}):\n".format(self.last_page_number))
            if page_num==None:
                page_num=self.last_page_number
            else :
                self.last_page_number=page_num

            name=input("Please input the drink name:\n")
            entry=recipe(name, self.curr_book,page_num,self.curr_method)

            ingredient=None
            while True :
                self.clear()
                entry.print()

                ingredient=input("input ingredients in format "+color.YELLOW +"quantity substance" + color.END +":\npress q to stop\n")
                if ingredient=="q" :
                    break
                else :
                    delim=ingredient.find(" ")
                    quantity=ingredient[0:delim]
                    substance=ingredient[delim:]
                    entry.add_ingredient(quantity,substance)

            if self.curr_book not in self.recipes :
                self.recipes[self.curr_book]={}

            self.recipes[self.curr_book][name]=entry

        except KeyboardInterrupt:
            pass

    def set_method(self) :
        try:
            self.curr_method=input("Please input the method:\n")
        except KeyboardInterrupt:
            pass

    def set_book(self) :
        try :
            self.curr_book=input("Please input the book:\n")
        except KeyboardInterrupt:
            pass

    def list_drinks(self) :
        for book,recipes in self.recipes.items() :
            print("Book: " + book)
            for entry in recipes.values() :
                entry.print()
        input()


    def remove_entry(self) :
        name=input("name?:\n")

        for book in self.recipes.values() :
            if name in book :
                print()
                book[name].print()

                if input("delete ?")=="y" :
                    del book[name]



    def add_entries(self) :
        while True :
            menu_options=["input drink","set book","set method", "remove entry","list drinks"]
            menu_executions=[self.input_drink,self.set_book,self.set_method,self.remove_entry,self.list_drinks]


            info="current book: {0}\ncurrent method: {1}".format(self.curr_book, self.curr_method)
            selection=self.menu.menu(menu_options, info)
            if selection!=None :
                menu_executions[selection]()
            else :
                break



def main() :
    recipes= pickle.load( open( "recipes.p", "rb" ) )
    drinks=drink_index(recipes)
    drinks.add_entries()
    # set_book()
    # print(curr_book)
    pickle.dump( drinks.recipes, open( "recipes.p", "wb" ) )


if __name__ == "__main__":
    # execute only if run as a script
    main()

import pickle
import readchar
import time
import os
import math


# holds a single recipe with ingredients and book and page information
class recipe :
	def __init__(self, name, book, page_num, method) :
		self.name=name
		self.book=book
		self.id=self.book+"_"+self.name

		self.page=page_num
		self.method=method
		self.ingredients={}
		self.rating=[]
		self.notes=""

	#adds ingredient to ingredient list
	def add_ingredient(self, quantity, unit, substance) :
			self.ingredients[substance]=[quantity, unit]

	#returns just the unit
	def get_substance_unit(self, substance) :
		return self.ingredients[substance][0]

	#returns just the quantity
	def get_substance_quantity(self, substance) :
		return self.ingredients[substance][1]


	#returns a string with all the base informtion on the drink
	def data_string(self) :
		data=color.BOLD +color.BLUE+ self.name+ color.END + "\n " +self.book+"\n "+color.CYAN+ "page "+self.page +"\n " +self.method +color.END
		rating=self.get_rating()
		if rating!=None :
			data+=" rated {}/5\n".format(rating)
		return data

	#returns a string represenation of the recipe
	def __str__(self):
		string=self.data_string()+"\n"

		ingredient_list=self.get_ingredient_list()
		for ingredient in ingredient_list :
			string+=" " + color.YELLOW +ingredient + color.END +"\n"
		# str+="\n"
		return string

	#adds a new rating to the rating list
	def add_rating(self, rating) :
		self.rating.append(rating)

	#returns an average of all rating
	def get_rating(self) :
		if len(self.rating)>0:
			return sum(self.rating)/len(self.rating)
		return None

	#adds a note to the drink entry
	def add_note(self, note) :
		self.notes+=color.GREEN+"-"+note+color.END+"\n"

	#returns a text list of ingredients
	def get_ingredient_list(self) :
		ingredient_list=[]
		for ingredient in self.ingredients.keys() :
			text="{0} {1} {2}".format(self.ingredients[ingredient][0],self.ingredients[ingredient][1],ingredient)
			ingredient_list.append(text)
		return ingredient_list

	#returns a list of just ingredients without quanities
	def get_ingredients(self) :
		return list(self.ingredients.keys())

	def remove_ingredient(self, ingredient_key) :
		del self.ingredients[ingredient_key]


	def pull_units(self, ingredient) :
		units=["oz","ounce","tsp", "teaspoon","tbl", "tablespoon", "dash", "drop"]

		for unit in units :
			if unit in ingredient :
				break_point=ingredient.find(unit)
				substance=ingredient[break_point+len(unit):].strip()
				quantity=int(ingredient[0:break_point].strip())

				if unit=="ounce" : unit="oz"
				if unit=="teaspoon" : unit="tsp"
				if unit=="tablespoon" : unit="tbl"
				return [quantity, unit, substance]

		#assume oz for some dumb reason
		break_point=ingredient.find(" ")
		quantity=int(ingredient[0:break_point].strip())
		substance=ingredient[break_point:].strip()
		return [quantity, "oz", substance]


def pull_units(ingredient) :
	units=["oz","ounce","tsp", "teaspoon","tbl", "tablespoon", "dash", "drop"]

	for unit in units :
		if unit in ingredient :
			break_point=ingredient.find(unit)
			substance=ingredient[break_point+len(unit):].strip()
			quantity=int(ingredient[0:break_point].strip())

			if unit=="ounce" : unit="oz"
			if unit=="teaspoon" : unit="tsp"
			if unit=="tablespoon" : unit="tbl"
			return [quantity, unit, substance]

	#assume oz for some dumb reason
	break_point=ingredient.find(" ")
	quantity=float(ingredient[0:break_point].strip())
	substance=ingredient[break_point:].strip()
	return [quantity, "oz", substance]




def parse_ingredient( ingredient) :
	if ingredient=="q" :
		return None
	elif ingredient=="" :
		return []
	else :
		return pull_units(ingredient)


def main() :
    recipes={}
    recipes_updated={}

    recipes= pickle.load( open( "recipes.p", "rb" ) )

    for old_recipe in recipes.values() :
        updated=recipe(old_recipe.name,old_recipe.book,old_recipe.page,old_recipe.method)
        # updated.ingredients=old_recipe.ingredients #NO
        for ingredient in old_recipe.ingredients.keys() :
            text=old_recipe.ingredients[ingredient]+" " +ingredient
            print( text )
            parsed_ingredient=parse_ingredient(text)
            updated.add_ingredient(parsed_ingredient[0],parsed_ingredient[1],parsed_ingredient[2])

        updated.add_rating(old_recipe.rating)
        updated.notes=old_recipe.notes
        recipes_updated[updated.id]=updated

    pickle.dump( recipes_updated, open( "recipes.p", "wb" ) )
    pickle.dump( recipes_updated, open( "recipes_local.p", "wb" ) )
    # pickle.dump( drinks.cabinet, open( "cabinet.p", "wb" ) )


if __name__ == "__main__":
    # execute only if run as a script
    main()

import pickle
import readchar
import time
import os

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
			data+="\n rated {}/5\n".format(rating)
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
			if(self.rating[0])==None :
				self.rating=[]
				return None
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

	#removes an ingredient
	def remove_ingredient(self, ingredient_key) :
		del self.ingredients[ingredient_key]

	#returns a list of all ingredients split by word
	def get_ingredients_keywords(self) :
		keywords=[]
		ingredients=self.get_ingredients()
		for ingredient in ingredients :
			keywords+=ingredient.split()
		return keywords

	#returns a list of keywords for searches
	def get_keywords(self) :

		keywords=self.get_ingredients_keywords()
		keywords.append(self.name)
		keywords.append(self.book)
		keywords.append(self.get_rating())
		keywords.append(self.method)
		keywords+=self.notes.split()
		return keywords

	#kinda weird, but if the name is more than one word returns a list of it for searching
	def get_name_list(self) :
		return self.name.split()



def main() :
	recipes={}
	recipes_local={}

	try :
		recipes= pickle.load( open( "recipes.p", "rb" ) )
	except Exception :
		pass

	try :
		recipes_local= pickle.load( open( "recipes_local.p", "rb" ) )

	except Exception :
		pass


	recipes.update(recipes_local) #combine backup and new

	pickle.dump( recipes, open( "recipes.p", "wb" ) )
	pickle.dump( recipes, open( "recipes_local.p", "wb" ) )


if __name__ == "__main__":
	# execute only if run as a script
	main()

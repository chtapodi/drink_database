import pickle
import time
import os
import math
import re
import numpy as np
import readchar
import readline
import csv



class menu_generator :

	def __init__(self) :
		self.message="q to return"


	def visualize_menu(self, options, index, instructions="") :
		os.system('clear')
		print("")
		print(color.CYAN + self.message + color.END)
		print(color.DARKCYAN + instructions +color.END)

		for i in range(0,len(options)) :
			if i==index :
				print(color.BOLD +color.PURPLE + "●" +str(options[i])+ color.END)
			else :
				print(" " +str(options[i]))
		# print("")


	def menu(self, options, instructions="", sideways=False) :
		menu_index=0
		while True :
			self.visualize_menu(options, menu_index, instructions=instructions)
			try :
				key=readchar.readkey()
				if(sideways==True) :
					if key=='a' or  key == readchar.key.LEFT :
						return "left"
					elif key=='d' or  key == readchar.key.RIGHT :
						return "right"
				if key=='w' or  key == readchar.key.UP :
					menu_index-=1
				elif key=='s' or key == readchar.key.DOWN:
					menu_index+=1
				elif key=='q' :
					break
				elif key=='e' or key == readchar.key.ENTER:
					return menu_index

				if len(options)>0 :menu_index=menu_index%len(options)
				time.sleep(.1)

			except KeyboardInterrupt:
				break


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


class unit_converter :
	# conversions={"oz":1.0,"ounce":1.0,"tsp":0.166, "teaspoon":0.166,"tbl":0.5, "tablespoon":0.5, "dashes":0.03125,  "dash":0.03125, "drops":0.00169, "drops":0.00169, "cube":0.166, "leaves":0.0176, "leaf":0.0176,"sprig":0.176,"barspoon":0.1666, "slices":0.07168573,"slice":0.07168573,"wedges":0.166,"wedge":0.166,"ml":0.033814,"cl":0.33814}

	def __init__(self,units="oz") :
		self.units=units
		self.conversions={"oz":1.0,"ounce":1.0,"tsp":0.166, "teaspoon":0.166,"tbl":0.5, "tablespoon":0.5, "dashes":0.03125,  "dash":0.03125, "drops":0.00169, "drops":0.00169, "cube":0.166, "leaves":0.0176, "leaf":0.0176,"sprig":0.176,"barspoon":0.1666, "slices":0.07168573,"slice":0.07168573,"wedges":0.166,"wedge":0.166,"ml":0.033814,"cl":0.33814, "egg":1.05}

	#pass in unit its coming from
	def to_oz(self,value, unit) :
		ratio=self.conversions[unit]
		return value*ratio

	#pass in unit to convert to
	def from_oz(self,value,unit) :
		ratio=self.conversions[unit]
		return value/ratio

	def convert(self, value, unit) :
		if unit is not self.units :
			in_oz=self.to_oz(value,unit)
			in_unit=self.from_oz(in_oz,self.units)
			return in_unit
		else :
			return value




class ingredient_handler :

	def __init__(self, ingredient_file="ingredients.p",synonym_file="synonyms.p", units='oz') :

		self.vector_tags=["alcohol percent","roughness","savory","sweet","acidic/sour","carbonated","dry","smokey","grassy","herby","woody","earthy","cereal","yeasty","malty","nutty","carmelized","bitter","astringent","almond/cherry/benzaldehyde","vanilla","licorice","spicy","limonene","citral","mint","floral","fruity-apple","fruity-apricot","fruity-pineapple"]

		self.synonyms=[]
		try :
			self.synonyms= pickle.load( open( synonym_file, "rb" ) )
		except:
			pass

		self.ingredients=[]
		self.update_vectors()
		try :
			self.ingredients= pickle.load( open( ingredient_file, "rb" ) )
		except:
			pass

		self.unit_converter=unit_converter(units)



	def update_vectors(self) :
		def generate_ingredient(csv_row) :
			vector=[]
			for x in csv_row[2:] :
				# print(x)
				if x=='' :x=0.0
				# print(int(x))
				x=float(x)
				vector.append(x)
			#map between 0 and 1
			alc_perc=csv_row[2]
			if alc_perc=='' :alc_perc=0.0
			attr=[x/5.0 for x in vector[1:] ]

			vector=[float(alc_perc)]
			vector.extend(attr)
			# print(vector)
			name=csv_row[0].strip().lower()
			names=self.get_synonyms(name)

			description=csv_row[1]
			# print(names)
			new_ingredient=vector_holder(names,vector,description,tags=self.vector_tags)
			return new_ingredient

		with open('ingredient_vectors.csv') as csv_file:
			csv_reader = csv.reader(csv_file, delimiter=',')
			line_count = 0
			for row in csv_reader:
				if row[0]!='' :
					new_ingredient=generate_ingredient(row)
					#check if ingredient already exists in list
					if new_ingredient in self.ingredients :
						ing_index=self.ingredients.index(new_ingredient)
						existing_ingredient=self.ingredients[ing_index]
						existing_ingredient.add_vector(new_ingredient.flavor_vectors)

					else :
						self.ingredients.append(new_ingredient)
				line_count+=1
		pickle.dump( self.ingredients, open( "ingredients.p", "wb" ) )



	#this checks if a recipe can be made with the available ingredients
	def check_recipe(self,recipe) :
		for ingredient_name in recipe.ingredients.keys() :
			# input(ingredient_name)
			if self.find_ingredient(ingredient_name)==None :
				return False
		return True

	def find_ingredient(self,name) :
		# input(self.ingredients)
		for ingredient in self.ingredients :
			# input(ingredient)
			if name in ingredient.names :
				return ingredient
		return None

	#returns all synonyms for an ingredients name
	def get_synonyms(self,name) :
		for synonym_set in self.synonyms:
			if name in synonym_set :
				return synonym_set
		return {name}

	def get_available_ingredients(self) :
		available=[]
		for ingredient in self.ingredients :
			available.extend(list(ingredient.get_names()))

		return available


	#scales the vector to match the percentage that it makes up of the recipe
	def get_scaled_vector(self,name,value,unit,drink_volume) :
		value=self.unit_converter.convert(value,unit)
		scale_factor=value/drink_volume
		# print("scale_factor",scale_factor)
		# print("name",name)
		ingredient=self.find_ingredient(name)
		if ingredient is None :
			return None
		scaled_vector=ingredient*scale_factor
		# print("Scaled vector\n",scaled_vector.names)
		return scaled_vector

	#gets the total volume of the drink
	def get_drink_volume(self,ingredient_list) :
		uc=unit_converter('oz')
		volume=0
		for ingredient, [value, unit] in ingredient_list.items() :
			value=self.unit_converter.convert(value,unit)
			# print("{} {}".format(ingredient,value))
			volume+= value
		return volume

	def get_recipe_vectors(self,recipe) :
		ingredient_vector_list=[]

		ingredient_list=recipe.ingredients
		drink_volume=self.get_drink_volume(ingredient_list)
		for ingredient, [value, unit] in ingredient_list.items() :
			ingredient_vector=self.get_scaled_vector(ingredient,value,unit,drink_volume)
			ingredient_vector_list.append(ingredient_vector)

		return ingredient_vector_list

	def sum_vectors(self,ingredient_vector_list) :
		vector_list=[]
		for ingredient_vector in ingredient_vector_list :
			vector_list.append(ingredient_vector.get_flavors())
		return np.sum(vector_list,axis=0)

	#The one stop shop. Calculates vectors for each ingredient, returns a summed vector for the whole thing
	#returns false if the required ingredients are not available
	def get_recipe_vector(self,recipe) :
		if self.check_recipe(recipe) :
			ingredient_vectors=self.get_recipe_vectors(recipe)
			recipe_vector=self.sum_vectors(ingredient_vectors)
			return recipe_vector
		return False


'''Is an ingredient, includes information about the flavors this entails'''
class vector_holder :
	def __init__(self, names, flavor_vector=None, description="",tags=None) :
		self.names=names
		self.flavor_vectors=np.array([])
		if flavor_vector is None :
			...
		else :
			flavor_vector=np.array(flavor_vector)
			if len(flavor_vector.shape)>1 :
				self.flavor_vectors=flavor_vector
			elif len(flavor_vector.shape)==1 :
				self.flavor_vectors=np.array([flavor_vector])

		self.description=description

		self.vector_tags=tags

	'''Returns the possible names assosciated with this vector'''
	def get_names(self) :
		return self.names

	def add_vector(self,new_vector) :
		new_vector=np.array(new_vector)
		self.flavor_vectors=np.append(self.flavor_vectors,new_vector,axis = 0)
		# self.flavor_vectors.append(new_vector)

	def get_flavors(self) :
		return np.average(self.flavor_vectors,axis=0)

	def get_vector_string(self,vector=None) :
		if vector is None :
			vector=self.get_flavors()

		string=list(self.names)[0]+"\n"
		for tag, value in zip(self.vector_tags,vector) :
			if value>0 :
				string+="{}: {:.4f}\n".format(tag,value)
		return string

	def all_vectors(self) :
		if len(self.flavor_vectors)<=1 :
			return self.get_vector_string()
		else :
			string = ''
			for i in range(len(self.flavor_vectors)) :
				string+="vector {}\n".format(i)
				string+=self.get_vector_string(self.flavor_vectors[i])
				string+="\n"
			string+="sum vector\n"
			string+=self.get_vector_string()
			return string


	# def __add__(self,other) :
	# 	...

	def __copy__(self) :
		new=vector_holder(self.get_names(),self.flavor_vectors,self.description,self.vector_tags)
		return new

	def __eq__(self,other) :
		if other==None :
			return False
		for name in self.names :
			if name in other.get_names() :
				return True

	def __ne__(self,other) :
		return not self==other

	def __mul__(self, other):
		multiplied=self.__copy__()
		for i in range(len(multiplied.flavor_vectors)) :
			multiplied.flavor_vectors[i]=multiplied.flavor_vectors[i]*other
		return multiplied

	def __rmul__(self, other):
		return self.__mul__(other)

	def __str__(self):
		return self.get_vector_string()


# holds a single recipe with ingredients and book and page information
class recipe :
	def __init__(self, name, book="", page_num=0, method="") :
		self.name=name
		self.book=book
		self.id=self.book+"_"+self.name

		self.page=page_num
		self.method=method
		self.ingredients={} # substance:[value, unit, (OPTIONAL) ingredient_vector]
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
		data=color.BOLD +color.BLUE+ self.name+ color.END + "\n " +self.book+"\n "+color.CYAN+ "page "+str(self.page) +"\n " +self.method +color.END
		rating=self.get_rating()
		if rating!=None :
			data+="\n rated {:.2f}/5".format(rating)
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

	def get_notes(self) :
		ansi_escape = re.compile(r'(?:\x1B[@-_]|[\x80-\x9F])[0-?]*[ -/]*[@-~]')
		return ansi_escape.sub('', self.notes)[1:]

	#returns a list of keywords for searches
	def get_keywords(self) :

		keywords=self.get_ingredients_keywords()
		keywords.extend(self.get_name_list())
		keywords.append(self.book)
		rating=self.get_rating()
		if rating!=None :
			keywords.append(str(rating))
			keywords.append(str(int(rating)))
			keywords.append("rated")
			keywords.append("has rating")
		keywords.append(self.method)
		notes=self.get_notes().split()
		if len(notes)>0 :

			keywords.extend(notes)
			keywords.append("has note")
		return keywords

	#kinda weird, but if the name is more than one word returns a list of it for searching
	def get_name_list(self) :
		return self.name.split()


class drink_index :
	def __init__(self, recipes_file="recipes.p",local_data_file="local_data.p", interactive=True) :
		self.recipes_file=recipes_file
		# self.cabinet_file=cabinet_file
		self.local_data_file=local_data_file
		self.local_recipes_file=recipes_file.strip(".p") + "_local.p"


		self.recipes={}
		self.recipes= pickle.load( open( self.recipes_file, "rb" ) )

		#load in local recipes (for syncing)
		recipes_local={}
		try :
			recipes_local= pickle.load( open( self.local_recipes_file, "rb" ) )
		except Exception :
			pass

		try :
			self.recipes.update(recipes_local)
		except Exception :
			pass

		self.curr_book=None;
		self.curr_method=None;
		self.last_page_number=None

		self.last_search=""
		self.bookmarks=[]
		self.previously_made=[]
		self.ratings={}
		try :
			local_data= pickle.load( open( self.local_data_file, "rb" ) )
			self.cabinet=local_data["cabinet"]
			self.bookmarks=local_data["bookmarks"]
			self.previously_made=local_data["previously_made"]
			self.last_search=local_data["last_search"]
			self.ratings=local_data["ratings"]
		except Exception as e:
			input(e)
			pass

		self.menu=menu_generator()

		self.ingredient_handler=ingredient_handler()
		self.unit_converter=unit_converter()



	def clear(self) :
		 os.system('clear')

	#inputs information for a drink
	def input_drink(self) :
		try:
			#optionally update book
			if(self.curr_book!=None) :
				book=input("Please input the book (defualt {}):\n".format(self.curr_book))
				if book!="" :
					self.curr_book=book
				else :
					book=self.curr_book
			else :
				book=input("Please input the book: ")
				self.curr_book=book

			#optionally update method
			if(self.curr_method!=None) :
				method=input("Please input the method (defualt {}):\n".format(self.curr_method))
				if method!="" :
					self.curr_method=method
				else :
					method=self.curr_method
			else :
				method=input("Please input the method: ")
				self.curr_method=method

			#optionally update page number
			if(self.last_page_number!=None) :
				page_num=input("Please input the page (defualt {}):\n".format(self.last_page_number))
				if page_num!="" :
					self.last_page_number=page_num
				else :
					page_num=self.last_page_number
			else :
				page_num=input("Please input the page: ")
				self.last_page_number=page_num

			name=input("Please input the drink name:\n")
			entry=recipe(name, book,page_num,method)
			#gives the option to overwrite if recipe exists
			if entry.id in self.recipes :
				if input("This entry already exists, would you like to overwrite?\n")!="y" :
					self.input_recipe_ingredients(entry)
					self.add_recipe(entry)
			else :
				self.input_recipe_ingredients(entry)
				self.add_recipe(entry)
			self.backup_recipes()

		except KeyboardInterrupt:
			pass

	#this finds the unit associated with the measurement and returns [quantity, unit, ingredient]
	# TODO make it so it doesnt do dumb shit with dashes
	def pull_units(self, ingredient) :
		units=["oz","ounce","tsp", "teaspoon","tbl", "tablespoon", "dashes",  "dash", "drops", "drops" "cube", "leaves", "leaf","sprig","barspoon", "slices","slice","wedges","wedge","egg","ml","cl", "whole"]

		for unit in units :
			if unit in ingredient :
				ingredient_string=ingredient.replace(unit,'')
				ingredient_list=ingredient_string.split(" ")
				if len(ingredient_list)>1 : #if there is a quanity and an ingredient
					quantity=0.0
					quantity_str=ingredient_list[0].strip()

					#deals with fraction strings, shamelessly stolen from the internet
					try:
						quantity= float(quantity_str)
					except ValueError:
						num, denom = quantity_str.split('/')
						try:
							leading, num = num.split(' ')
							whole = float(leading)
						except ValueError:
							whole = 0
							frac = float(num) / float(denom)
						quantity= whole - frac if whole < 0 else whole + frac


					substance=" ".join(ingredient_list[1:]).strip().lower() #this is a little weird but deals with multi word ingredients

				if unit=="ounce" : unit="oz"
				if unit=="teaspoon" : unit="tsp"
				if unit=="tablespoon" : unit="tbl"
				return [quantity, unit, substance]

		#assume oz for some dumb reason
		break_point=ingredient.find(" ")
		quantity=float(ingredient[0:break_point].strip())
		substance=ingredient[break_point:].strip()
		return [quantity, "oz", substance]



	def parse_ingredient(self, ingredient) :
		if ingredient=="q" :
			return None
		elif ingredient=="" :
			return []
		else :
			return self.pull_units(ingredient)

	def enter_ingredients(self, entry) :
		while True :
			self.clear()
			entry_data=entry.data_string()
			# print(entry_data)
			print(entry)

			ingredient=input("input ingredients in format "+color.YELLOW +"quantity unit substance" + color.END +":\nenter q to stop\n")

			try :
				parsed_ingredient=self.parse_ingredient(ingredient)
				if parsed_ingredient==None : return
				if len(parsed_ingredient)>0 :
						entry.add_ingredient(parsed_ingredient[0],parsed_ingredient[1],parsed_ingredient[2])
			except Exception :
				input("Something you typed does not comply with formatting, try again")

	#turn this into a menu
	def input_recipe_ingredients(self, entry) :
		ingredient=None
		if len(entry.get_ingredients())==0 : #if it has no ingres yet
			self.enter_ingredients(entry)
		while True :
			self.clear()
			entry_data=entry.data_string()
			print(entry_data)
			menu_options=[color.YELLOW +"+add"+color.END]+entry.get_ingredient_list()
			selection=self.menu.menu(menu_options,entry_data)
			if selection!=None :
				if selection==0 :#add ingredient
					self.enter_ingredients(entry)
					break
				else :
					key_list=entry.get_ingredients()
					# print(key_list)
					# print(selection)
					# input()
					if input("remove {}? ".format(key_list[selection-1]))=="y" :
						entry.remove_ingredient(key_list[selection-1])

			else :
				break

	#adds a recipe to the index
	def add_recipe(self, entry) :
		if entry.id in self.recipes :
			print("Something went wrong, drink exists") #if the drink already exists
			input()
		else :
			self.recipes[entry.id]=entry

	#deletes an entry
	def remove_entry(self, entry) :
		# print(entry.id)
		# print(self.recipes)
		if input("delete ? (y/n)\n")=="y" :
			del self.recipes[entry.id]
			return True

	#edits an entry page
	def edit_page(self, entry) :
		try:
			entry.page=input("new page number: ")
		except KeyboardInterrupt:
			pass

		#edits an entry page
	def edit_book(self, entry) :
		try :
			new_book=input("new book: ")
			if new_book!="" :
				del self.recipes[entry.id]
				entry.book=new_book
				entry.id=entry.book+"_"+entry.name
				self.add_recipe(entry)
		except KeyboardInterrupt:
			pass

		#edits an entry page
	def edit_method(self, entry) :
		try :
			method=input("new method: ")
			if method!="" :
				entry.method=method
		except KeyboardInterrupt:
			pass

		#edits an entry page
	def edit_name(self, entry) :
		try :
			new_name=input("new name: ")
			if new_name!="" :
				del self.recipes[entry.id]
				entry.name=new_name
				entry.id=entry.book+"_"+entry.name
				self.add_recipe(entry)

		except KeyboardInterrupt:
			pass

	#Generates and shows a menu for editing an entry
	def edit_drink_menu(self, entry) :

		menu_options=["edit name","edit ingredients","edit page", "edit book", "edit method","delete"]
		menu_executions=[self.edit_name, self.input_recipe_ingredients,self.edit_page,self.edit_book,self.edit_method,self.remove_entry]

		selection=self.menu.menu(menu_options, str(entry)+entry.notes)
		if selection!=None :
			return menu_executions[selection](entry)
		else :
			pass


	#adds notes to entry
	def add_note(self, entry) :
		try:
			entry.add_note(input("type notes below:\n"))
		except KeyboardInterrupt:
			pass

	#adds rating to entry
	def add_rating(self, entry) :
		try:
			new_rating=float(input("enter rating out of 5\n"))
			entry.add_rating(new_rating)
			self.ratings[entry.id]=new_rating
		except Exception as e:
			print(e)
			input()
			pass

	#returns string to display based on if the entry is bookmarked or not
	def get_bookmark_status(self, entry) :
		if entry.id in self.bookmarks :
			return "unbookmark"
		return "bookmark"

	def toggle_bookmark(self,entry) :
		if entry.id in self.bookmarks :
			self.bookmarks.remove(entry.id)
		else :
			self.bookmarks.append(entry.id)
		# return True


	# def

	#Shows the options for a drink as well as the recipe
	def drink_menu(self, entry) :
		is_available=self.ingredient_handler.get_recipe_vector(entry)

		while True :
			if is_available is not False:
				menu_options=["rate","add notes", "{}".format(self.get_bookmark_status(entry)),"find most similar","edit"]
				menu_executions=[self.add_rating,self.add_note,self.toggle_bookmark,self.show_most_similar,self.edit_drink_menu]
			else :
				menu_options=["rate","add notes", "{}".format(self.get_bookmark_status(entry)),"edit"]
				menu_executions=[self.add_rating,self.add_note,self.toggle_bookmark,self.edit_drink_menu]
			# menu_options=["rate","add notes", "{}".format(self.get_bookmark_status(entry)),"edit"]
			selection=self.menu.menu(menu_options, str(entry)+entry.notes)
			if selection!=None :
				return_val=menu_executions[selection](entry)
				if return_val :
					break
			else :
				break

	#This is disgustingly innefficiant, will fix
	def get_closest_recipe(self,recipe,recipe_list) :
		recipe_vector=self.ingredient_handler.get_recipe_vector(recipe)
		dist = np.linalg.norm(recipe_vector-self.ingredient_handler.get_recipe_vector(recipe_list[0]))
		closest=recipe_list[0]
		for comp_recipe in recipe_list[1:] :
			if comp_recipe.id != recipe.id :
				# comp_vector=
				new_dist = np.linalg.norm(recipe_vector-self.ingredient_handler.get_recipe_vector(comp_recipe))
				if new_dist<dist :
					dist=new_dist
					closest=comp_recipe
		return closest

	#Gets the N most similar recipes from available recipes
	def get_N_most_similar(self,entry,N=6) :
		recipe_list=self.get_vectorizable_list()
		# vector_pair_list=zip(recipe_list,vector_list)
		similar_list=[]
		# entry_vector=self.ingredient_handler.get_recipe_vector(entry)
		# entry_pair=(entry,entry_vector)

		while len(recipe_list)>0 and len(similar_list)<N:

			# current_vector=similar_list[-1]
			closest=self.get_closest_recipe(entry,recipe_list)
			# i=vector_list.index(closest)
			similar_list.append(recipe_list.pop(recipe_list.index(closest)))
			# vector_list.pop(i)

		return similar_list

	def show_most_similar(self,entry) :
		similar_list=self.get_N_most_similar(entry)
		self.list_drinks(recipe_list=similar_list, title="Most similar to {}\n".format(entry.name))



	#returns the data of all recipes that contain only ingredients with flavor profiles
	def get_vectorizable_list(self) :
		all_recipes=self.get_recipe_list()
		vectorizable=[]
		# recipe_vectors=[]
		for recipe in all_recipes :
			vector=self.ingredient_handler.get_recipe_vector(recipe)
			if vector is not False :
				vectorizable.append(recipe)
				# recipe_vectors.append(vector)

		return vectorizable



	#gets a list of all the recipes in the data_base
	def get_recipe_list(self) :
		return list(self.recipes.values())

	#shows the drinks and allows selection
	def list_drinks(self, recipe_list=None, title="") : #defualts to all recipes
		i=0
		items_per_page=3
		if(recipe_list==None) :
			recipe_list=self.get_recipe_list()

		num_pages=math.ceil(len(recipe_list)/items_per_page)
		while True :
			menu_options=recipe_list[(i*items_per_page):(i*items_per_page)+items_per_page]
			selection=self.menu.menu(menu_options,"{2}page {0}/{1}".format(i+1,num_pages,title),sideways=True)
			if selection!=None :
				if(selection=="right") :
					i+=1
				elif(selection=="left") :
					i-=1

				else :
					self.drink_menu(recipe_list[(i*items_per_page)+selection])
					# recipe_list=list(self.recipes.values()) #why did this exist?

				if num_pages!=0 : #stops modulo by 0 error
					i=i%(num_pages)
				else :
					i=1
			else :
				break


	#drinks must be a subset of provided info. e.g. you must have all the ingredient
	#TODO: make it so you can set a numbr of acceptable missing ingredients
	def subset_search(self, search_terms) :
		priority=search_terms["priority"]
		to_include=search_terms["priority"]+search_terms["standard"]
		blacklist=search_terms["blacklist"]



		found_list=[]
		search_list=self.get_recipe_list()
		# input(search_terms)
		if len(search_terms["group"])>0:
			in_group=[]
			for recipe in search_list :
				if recipe.id in search_terms["group"] :
					in_group.append(recipe)
			search_list=in_group

		if len(priority)>0 :
			has_priority=[]
			for recipe in search_list:
				ingredient_list=recipe.get_ingredients()
				synonym_list=[]
				#this is to make sure that all ingredients that are required dont require every synonym to be in it, which will not happen
				for i in ingredient_list :
					synonym_list.extend(self.ingredient_handler.get_synonyms(i))
					has_priority.append(recipe)
			search_list=has_priority #don't need to search the rest

		#checking if has all the ingredients
		for recipe in search_list:
			ingredient_list=recipe.get_ingredients()
			if(all(ingredient in to_include for ingredient in ingredient_list)): #if all ingredients are in search list
				found_list.append(recipe)


		if(len(blacklist))>0 :
			for recipe in found_list :
				for blacklisted in blacklist :
					if blacklisted in recipe.get_ingredients() :
						found_list.remove(recipe)

		return found_list


	#searches for at least one item
	def inclusive_search(self, search_terms, keyword_function) :
		priority=search_terms["priority"]
		to_include=search_terms["priority"]+search_terms["standard"]
		blacklist=search_terms["blacklist"]

		search_list=self.get_recipe_list()
		found_list=[]

		if len(search_terms["group"])>0:
			in_group=[]
			for recipe in search_list :
				if recipe.id in search_terms["group"] :
					in_group.append(recipe)
			search_list=in_group

		#priority ingredients
		if len(priority)>0 :
			has_priority=[]
			for recipe in search_list:
				ingredient_list=keyword_function(recipe)
				if(all(ingredient in ingredient_list for ingredient in priority)): #if recipe contains all required
					has_priority.append(recipe)
			search_list=has_priority #don't need to search the rest

		#standard ingredients
		for recipe in search_list :
			ingredient_list=keyword_function(recipe)
			for included in to_include :
				if included in ingredient_list:
					found_list.append(recipe)
					break
		#blacklisted ingredients
		if(len(blacklist))>0 :
			for recipe in found_list :
				for blacklisted in blacklist :
					if blacklisted in keyword_function(recipe) :
						found_list.remove(recipe)
		return self.sort_by_overlap(found_list, to_include, keyword_function)

	#searches through recipes ingredients, returns sorted list
	def ingredient_search(self, search_terms) :
		return self.inclusive_search(search_terms, recipe.get_ingredients)

	#searches through recipes ingredients, returns sorted list
	def keyword_search(self, search_terms) :
		return self.inclusive_search(search_terms, recipe.get_keywords)

		#searches through recipes ingredients, returns sorted list
	def name_search(self, search_terms) :
		return self.inclusive_search(search_terms, recipe.get_name_list)


	#sorts list by number of ingredient in the search term shared by the recipe
	def sort_by_overlap(self, recipe_list, compare_list, keyword_function) :
		overlap_list=[]
		id_list=[]
		for recipe in recipe_list :
			count=0
			recipe_keywords=keyword_function(recipe)
			for recipe_keyword in recipe_keywords :
				if recipe_keyword in compare_list :
					count+=1
			overlap_list.append(1/(count/len(compare_list)))
			id_list.append(recipe.id)

		#I don't know why this extra step is required, but it is
		sorted_list=[x for _,x in sorted(list(zip(overlap_list,id_list)))]
		return [self.recipes[id] for id in sorted_list]


	def get_cabinet(self) :
		full_cabinet=set()

		for item in self.cabinet:
			synonyms=self.ingredient_handler.get_synonyms(item)
			full_cabinet=set.union(full_cabinet,synonyms)
		# input(full_cabinet)

		return list(full_cabinet)



	#organizes search terms
	def parse_search(self, search_terms) :
		term_dict={"priority":[],"standard":[],"blacklist":[],"group":[]}
		term_list=search_terms.split(',')
		#solves white space
		term_list=[t.strip() for t in term_list]

		#here I would add a decision to not fuzzy search
		if "$cabinet" in term_list :
			term_dict["standard"].extend(self.get_cabinet())
			term_list.remove("$cabinet")

		if "$vector" in term_list :
			term_dict["standard"].extend(self.ingredient_handler.get_available_ingredients())
			term_list.remove("$vector")

		if "$bookmark" in term_list or  "$bookmarks" in term_list:
			term_dict["group"].extend(self.bookmarks)
			try :
				term_list.remove("$bookmark")
			except :
				pass
			try :
				term_list.remove("$bookmarks")
			except :
				pass

		if "$rated" in term_list :
			term_dict["group"].extend(self.ratings.keys())
			try :
				term_list.remove("$bookmark")
			except :
				pass


		for term in term_list :
			# term=term.strip()
			if '*' in term :
				term=term.replace('*','')
				#TODO: At the momment this is handled on the other end, because if they are
				#all priority, then nothing will have them.
				# synonyms=self.ingredient_handler.get_synonyms(term)
				term_dict["priority"].append(term)
			elif '!' in term :
				term=term.replace('!','')
				synonyms=self.ingredient_handler.get_synonyms(term)
				term_dict["blacklist"].extend(list(synonyms))
			else :
				synonyms=self.ingredient_handler.get_synonyms(term)
				term_dict["standard"].extend(list(synonyms))
		# input(term_dict)
		return term_dict

	#menu for search options
	def search_menu(self) :
		#This is fun
		#options for each search term, seperated by ,
		#must include
		info="use:\n*ingredient to make it required\n!ingredient to blacklist\n$cabinet to include liquor cabinet\nseperate with ,"
		while True :
			try :
				menu_options=["subset of search", "include at least one ingredient search","include at least one keyword search", "name search"]
				menu_executions=[self.subset_search,self.ingredient_search, self.keyword_search, self.name_search]
				selection=self.menu.menu(menu_options, info)
				if selection!=None :

					#Keeps previous search, not the most useful. Make it editable?
					if(self.last_search!="") :
						def hook():
							readline.insert_text(self.last_search)
							readline.redisplay()
						readline.set_pre_input_hook(hook)
						search_terms = input("search: ")
						readline.set_pre_input_hook()
						# search_terms=input("search({}): ".format(self.last_search))
						if search_terms!="" and search_terms!=" " :
							self.last_search=search_terms
						else :
							search_terms=self.last_search
					else :
						search_terms=input("search: ")
						self.last_search=search_terms


					parsed_terms=self.parse_search(search_terms)
					drink_list=menu_executions[selection](parsed_terms)
					self.list_drinks(drink_list,"{} results\n".format(len(drink_list)))
				else :
					break
			except KeyboardInterrupt :
				pass

	#shows interface for editing lists
	def edit_list(self, list_to_edit, items_per_page=6) :
		i=0
		items_per_page=6

		while True :
			num_pages=math.ceil(len(list_to_edit)/items_per_page)
			menu_options=[color.YELLOW +"+add"+color.END]+list_to_edit[(i*items_per_page):(i*items_per_page)+items_per_page]

			selection=self.menu.menu(menu_options,"page {0}/{1}".format(i+1,num_pages),sideways=True)
			if selection!=None :
				if(selection=="right") :
					i+=1
				elif(selection=="left") :
					i-=1
				else :
					if selection==0 :#or (i*items_per_page)+selection>=len(list_to_edit) :
						new_item=input("type item: ")
						if new_item!='' :
							list_to_edit.insert(0,new_item)
					else :
						if input("remove {}? ".format(list_to_edit[(i*items_per_page)+selection-1]))=="y" :
							del list_to_edit[(i*items_per_page)+selection-1]

				if num_pages!=0 : #stops modulo by 0 error
					i=i%(num_pages)
				else :
					i=0
			else :
				break

	#edit cabinet menu
	def edit_cabinet(self) :
		self.edit_list(self.cabinet,items_per_page=6)

#generates and returns a dict that has all ingredients, including and sorted by number of instances, with a list of recipes that include it
	def generate_ingredient_list(self) :
		ingredient_counts={} #ingredient;[count, [recipes]]
		for entry in self.recipes.values() :
			for ingredient in entry.get_ingredients() :
				if ingredient in ingredient_counts.keys() : #if its already been entered
					ingredient_counts[ingredient][0]+=1 #add to count
					ingredient_counts[ingredient][1].append(entry) #add entry to list
				else : #if new ingredient
					ingredient_counts[ingredient]=[1,[entry]]

		sorted_ingredients={k: v for k, v in sorted(ingredient_counts.items(), key=lambda item: item[1][0], reverse=True)}
		return sorted_ingredients


	#TODO split out and sort by completion
	def show_missing_ingredients(self) :
		all_ingredients=self.generate_ingredient_list()
		missing_ingredients_text=[]
		missing_ingredients_recipes=[]
		full_cabinet=self.get_cabinet()

		#generates lists of ingredient texts and recipes
		for ingredient in all_ingredients.keys() :
			if ingredient not in full_cabinet :
				text="{0} {1}".format(all_ingredients[ingredient][0],ingredient)
				missing_ingredients_text.append(text)
				missing_ingredients_recipes.append(all_ingredients[ingredient][1])

		#display
		i=0
		items_per_page=6
		while True :
			num_pages=math.ceil(len(missing_ingredients_text)/items_per_page)
			menu_options=missing_ingredients_text[(i*items_per_page):(i*items_per_page)+items_per_page]

			selection=self.menu.menu(menu_options,"page {0}/{1}".format(i+1,num_pages),sideways=True)
			if selection!=None :
				if(selection=="right") :
					i+=1
				elif(selection=="left") :
					i-=1
				else :
					#selected an ingredient, show recipes
					self.list_drinks(recipe_list=missing_ingredients_recipes[(i*items_per_page)+selection])
				if num_pages!=0 : #stops modulo by 0 error
					i=i%(num_pages)
				else :
					i=0
			else :
				break


	def show_bookmarked(self) :
		ids=self.bookmarks
		recipes=[self.recipes[id] for id in ids]

		self.list_drinks(recipe_list=recipes, title="bookmarked\n")


	#Runs main menu
	def main_menu(self) :
		while True :
			menu_options=["search", "show missing ingredients","show bookmarked recipes","edit cabinet", "input drink", "list drinks"]
			menu_executions=[self.search_menu, self.show_missing_ingredients,self.show_bookmarked,self.edit_cabinet,self.input_drink, self.list_drinks]


			info="current book: {0}\ncurrent method: {1}".format(self.curr_book, self.curr_method)
			selection=self.menu.menu(menu_options, info)
			if selection!=None :
				menu_executions[selection]()
			else :
				break

	#backs up recipes to local data_base
	def backup_recipes(self) :
			pickle.dump( self.recipes, open( self.recipes_file, "wb" ) )
			pickle.dump( self.recipes, open( self.local_recipes_file, "wb" ) )

	def backup(self) :
		self.backup_recipes()
		# pickle.dump( self.cabinet, open( self.cabinet_file, "wb" ) )

		local_data={}
		local_data["cabinet"]=self.cabinet
		local_data["bookmarks"]=self.bookmarks
		local_data["previously_made"]=self.previously_made
		local_data["last_search"]=self.last_search
		local_data["ratings"]=self.ratings
		pickle.dump( local_data, open( self.local_data_file, "wb" ) )

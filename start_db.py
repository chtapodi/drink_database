import pickle
import readchar
import time
import os
import math

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

# holds a single recipe with ingredients and book and page information
class recipe :
	def __init__(self, name, book, page_num, method) :
		self.name=name
		self.book=book
		self.id=self.book+"_"+self.name

		self.page=page_num
		self.method=method
		self.ingredients={} # substance:value
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
			data+="\n rated {}/5".format(rating)
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


class drink_index :
	def __init__(self, recipes={}, cabinet=[]) :

		self.recipes=recipes #if not provided defaults to empty dict
		self.cabinet=cabinet
		self.curr_book=None;
		self.curr_method=None;
		self.last_page_number=None
		self.last_search=""
		self.menu=menu_generator()



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
		units=["oz","ounce","tsp", "teaspoon","tbl", "tablespoon", "dashes",  "dash", "drops", "drops" "cube", "leaves", "leaf", "barspoon"]

		for unit in units :
			if unit in ingredient :
				# break_point=ingredient.find(unit)
				# substance=ingredient[break_point+len(unit):].strip()
				# quantity=int(ingredient[0:break_point].strip())

				ingredient_string=ingredient.replace(unit,'')
				ingredient_list=ingredient_string.split(" ")
				if len(ingredient_list)>1 : #if there is a quanity and an ingredient
					quantity=float(ingredient_list[0].strip())
					substance=" ".join(ingredient_list[1:]) #this is a little weird but deals with multi word ingredients


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

	#turn this into a menu
	def input_recipe_ingredients(self, entry) :
		ingredient=None
		if len(entry.get_ingredients())==0 : #if it has no ingres yet
			self.clear()
			entry_data=entry.data_string()
			print(entry_data)
			ingredient=input("input ingredients in format "+color.YELLOW +"quantity unit substance" + color.END +":\npress q to stop\n")
			try:
				parsed_ingredient=self.parse_ingredient(ingredient)
				if parsed_ingredient==None : return None
				if len(parsed_ingredient)>0 :

						entry.add_ingredient(parsed_ingredient[0],parsed_ingredient[1],parsed_ingredient[2])
			except Exception :
				input("Something you typed does not comply with formatting, try again")
		while True :
			self.clear()
			entry_data=entry.data_string()
			print(entry_data)
			menu_options=[color.YELLOW +"+add"+color.END]+entry.get_ingredient_list()
			selection=self.menu.menu(menu_options,entry_data)
			if selection!=None :
				if selection==0 :#add ingredient
					ingredient=input("input ingredients in format "+color.YELLOW +"quantity unit substance" + color.END +":\npress q to stop\n")
					try :
						parsed_ingredient=self.parse_ingredient(ingredient)
						if parsed_ingredient==None : break
						if len(parsed_ingredient)>0 :
								entry.add_ingredient(parsed_ingredient[0],parsed_ingredient[1],parsed_ingredient[2])
					except Exception :
						input("Something you typed does not comply with formatting, try again")
				else :
					key_list=entry.get_ingredients()
					print(key_list)
					print(selection)
					input()
					if input("remove {}? ".format(key_list[selection-1]))=="y" :
						entry.remove_ingredient(key_list[selection-1])

			else :
				break

	#adds a recipe to the index
	def add_recipe(self, entry) :
		if entry.id in self.recipes :
			print("big fuck") #if the drink already exists
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
		menu_options=["edit name","edit ingredients","edit page", "edit book", "delete"]
		menu_executions=[self.edit_name, self.input_recipe_ingredients,self.edit_page,self.edit_book,self.remove_entry]

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
			new_rating=int(input("enter rating out of 5\n"))
			entry.add_rating(new_rating)
		except Exception:
			print("ERROR: not an int")
			input()
			pass

	#Shows the options for a drink as well as the recipe
	def drink_menu(self, entry) :
		menu_options=["rate","add notes", "edit"]
		menu_executions=[self.add_rating,self.add_note,self.edit_drink_menu]

		while True :
			selection=self.menu.menu(menu_options, str(entry)+entry.notes)
			if selection!=None :
				return_val=menu_executions[selection](entry)
				if return_val :
					break
			else :
				break

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
					recipe_list=list(self.recipes.values())

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

		if len(priority)>0 :
			has_priority=[]
			for recipe in search_list:
				ingredient_list=recipe.get_ingredients()
				if(all(ingredient in ingredient_list for ingredient in priority)): #if recipe contains all required
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


	#organizes search terms
	def parse_search(self, search_terms) :
		term_dict={"priority":[],"standard":[],"blacklist":[]}
		term_list=search_terms.split(',')
		if "$cabinet" in term_list :
			term_dict["standard"]+=self.cabinet
			term_list.remove("$cabinet")

		for term in term_list :
			term=term.strip()
			if '*' in term :
				term=term.replace('*','')
				term_dict["priority"].append(term)
			elif '!' in term :
				term=term.replace('!','')
				term_dict["blacklist"].append(term)
			else :
				term_dict["standard"].append(term)
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
						search_terms=input("search({}): ".format(self.last_search))
						if search_terms!="" :
							self.last_search=search_terms
						else :
							search_terms=self.last_search
					else :
						search_terms=input("search: ")
						self.last_search=search_terms


					parsed_terms=self.parse_search(search_terms)
					drink_list=menu_executions[selection](parsed_terms)
					self.list_drinks(drink_list,"search results\n")
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

	def show_missing_ingredients(self) :
		all_ingredients=self.generate_ingredient_list()
		missing_ingredients_text=[]
		missing_ingredients_recipes=[]

		#generates lists of ingredient texts and recipes
		for ingredient in all_ingredients.keys() :
			if ingredient not in self.cabinet :
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


	#Runs main menu
	def main_menu(self) :
		while True :
			menu_options=["input drink", "search", "show missing ingredients","edit liquor cabinet", "list drinks"]
			menu_executions=[self.input_drink,self.search_menu, self.show_missing_ingredients,self.edit_cabinet, self.list_drinks]


			info="current book: {0}\ncurrent method: {1}".format(self.curr_book, self.curr_method)
			selection=self.menu.menu(menu_options, info)
			if selection!=None :
				menu_executions[selection]()
			else :
				break

	#backs up recipes to local data_base
	def backup_recipes(self) :
			pickle.dump( self.recipes, open( "recipes.p", "wb" ) )
			pickle.dump( self.recipes, open( "recipes_local.p", "wb" ) )



def main() :
	recipes={}
	recipes_local={}
	cabinet=[]
	try :
		recipes= pickle.load( open( "recipes.p", "rb" ) )
	except Exception :
		pass

	try :
		recipes_local= pickle.load( open( "recipes_local.p", "rb" ) )

	except Exception :
		pass
	try :
		cabinet= pickle.load( open( "cabinet.p", "rb" ) )
	except Exception :
		pass

	recipes.update(recipes_local)
	drinks=drink_index(recipes=recipes, cabinet=cabinet)

	# fun little test bed
	# for entry in drinks.recipes.values() :
	# 	print(entry.get_keywords())
	# input()

	#starts the UI
	drinks.main_menu()


	pickle.dump( drinks.recipes, open( "recipes.p", "wb" ) )
	pickle.dump( drinks.recipes, open( "recipes_local.p", "wb" ) )
	pickle.dump( drinks.cabinet, open( "cabinet.p", "wb" ) )


if __name__ == "__main__":
	# execute only if run as a script
	main()

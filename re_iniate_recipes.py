import pickle
import readchar
import time
import os
import math
from copy import copy

from drink_db import recipe
def main() :
	recipes={}
	recipes_updated={}

	recipes= pickle.load( open( "recipes.p", "rb" ) )

	for old_recipe in recipes.values() :
		updated=recipe(old_recipe.name,old_recipe.book,old_recipe.page,old_recipe.method)
		updated.ingredients={}#copy(old_recipe.ingredients) #NO

		for ingredient in old_recipe.ingredients.keys() :
			updated.ingredients[ingredient.strip()] = old_recipe.ingredients[ingredient]
			# del updated.ingredients[ingredient]

		updated.rating=old_recipe.rating
		updated.notes=old_recipe.notes
		recipes_updated[updated.id]=updated

	pickle.dump( recipes_updated, open( "recipes.p", "wb" ) )
	pickle.dump( recipes_updated, open( "recipes_local.p", "wb" ) )
	# pickle.dump( drinks.cabinet, open( "cabinet.p", "wb" ) )


if __name__ == "__main__":
    # execute only if run as a script
    main()

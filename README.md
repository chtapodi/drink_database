# drink_database #

## Function ##
The goal of this project is a system to document cocktail recipes and provide filtering and searching techniques.

## Features ##
Relatively easy input of new drink recipes via a hacked together command line GUI.
A "cabinet" of owned ingredients can be maintained  

Ability to perform various searches.
Ingredient searches can blacklist, or require ingredients by the prefixes ! and *, respectively.

Searching for ingredients has recently been made fuzzy by default, so it will include other common names for ingredients.

using '$cabinet' as an input inputs all items in your cabinet.

### Name search ###
Not working quite right, but searches for matching names

### Keyword search ###
Searches for just about anything in the drink, including notes, rating, name, and ingredients.

### At least one ingredient search ###
Takes in a list of ingredients, returns all recipes that have at least one of the inputted ingredients. It then sorts by the number of ingredients listed that are in the recipe.

### Subset of search search ###
Returns only recipes that only have the ingredients that have been listed.


## Syncing ##
To sync recipes to another device, copy the `recipes.p` file to the new device and run `start_db.py` to combine recipes

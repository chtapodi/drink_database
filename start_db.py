from drink_db import drink_index


def main() :
	drinks=drink_index()
	try :
		#starts the UI
		drinks.main_menu()
	except Exception as e:
		input(e)
		drinks.backup()
		pass
	drinks.backup()




if __name__ == "__main__":
	# execute only if run as a script
	main()

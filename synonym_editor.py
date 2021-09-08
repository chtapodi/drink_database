import pickle

synonyms=[]
try :
	synonyms= pickle.load( open( "synonyms.p", "rb" ) )
except:
	pass


def add_to_set(input_data) :
	for synonym_set in synonyms :
		for data_point in input_data :
			if data_point in synonym_set :
				synonym_set.update(input_data)
				return 1
	return 0


def process_synonyms(input_data) :
	if not add_to_set(input_data) :
		synonyms.append(set(input_data))

try :
	while True :
		input_data=input()
		if len(input_data)>1:
			input_data=input_data.split(",")
			input_data=[x.strip().lower() for x in input_data]
			process_synonyms(input_data)
			print(synonyms)

except KeyboardInterrupt:
	pass

pickle.dump( synonyms, open( "synonyms.p", "wb" ) )

import sys  # Used for args
import pickle # Used to create the .bin file
# Usage: lzw.py [-e[-d]] [file]



# Get a files contents
def getFile(filename): 
	filename = open(filename, 'r', encoding="utf8", errors='ignore') # Make sure its encoding is utf-8
	result = filename.readlines()
	filename.close()

	# Return the files data
	return ''.join(result)



# Save the compressed text into a binary file with the pickle.dump method
def writeBinary(filename, encoded_text):
	#filename = filename[0:str(filename).find('.')] + '.bin'

	with open(filename, 'wb') as file:
		pickle.dump(encoded_text, file)



# This will read the binary with the pickle.load method
def readBinary(filename):
	with open(filename, 'rb') as file:
		result = pickle.load(file)

	return result




# Compress a string
def compress(string):
	index = 0

	# Count starts at 256 and is the value for every key in the check_dict dictionary, it adds by one when being used
	count = 256
	output = []
	check_dict = {}

	
	for x in range(len(string)):
		# Check if the index has reached its limit
		if index == len(string) - 1:
			break


		# Add current and next value
		res = string[index] + string[index + 1]
		#print(res)

		# Check if its in the dictionary stored as a key
		if check_dict.get(res):
			for keys, vals in check_dict.items():
				if keys == res:
					value = check_dict[res]
					output.append(value)
					break


			if index + 2 < len(string):
				res += string[index + 2]
				check_dict[res] = count
				index += 1

		else:
			check_dict[res] = count
			value = ord(string[index])
			output.append(value)

		# Keep adding one until loop breaks
		index += 1
		count += 1



	# Add the last ascii value which is always left out in the algorithm
	output.append(ord(string[-1]))
	return output



# Compress files and save them in .bin format
def compressFile(filename):
	# Get the file
	string = getFile(filename)

	# Compress it
	result = compress(string)

	# Write the result to the file
	writeBinary(filename, result)


# Decompress a file, .bin files
def decompressFile(filename):
	# Get the binary data from the file (gets the ascii values back)
	result = readBinary(filename)

	# Decompress it
	result = decompress(result)

	# Write the result to the file
	with open(filename, 'w', encoding='utf8', errors='ignore') as file:
		file.write(result)

	

# Decompress the encoded string
def decompress(num_list):
	check_dict = {}
	count = 256
	index = 0
	output = []
	decoded = ''

	# Convert to str()
	for x in range(len(num_list)):
		num_list[x] = str(num_list[x])


	# Decompress algorithm
	for x in range(len(num_list)):
		# Check if it reaches index-limit
		if index == len(num_list) - 1:
			break


		# Output result which will be appended to output
		output_res = ''

		first = num_list[index]
		second = num_list[index + 1]
		#print(f'Current: {first}\nNext: {second}')



		# Before Adding to dictionary
		# Check if both is greater
		if int(first) > 255 and int(second) > 255:
			for keys, vals in check_dict.items():
				if vals == int(first):
					first = keys
					break



			for keys, vals in check_dict.items():
				if vals == int(second):
					second = keys.split('-')[0]
					break



		# Check if current or next
		else:
			if int(first) > 255:
				for keys, vals in check_dict.items():
					if vals == int(first):
						first = keys
						break



			if int(second) > 255:
				for keys, vals in check_dict.items():
					if vals == int(second):
						second = keys
						break






		# Result
		res = first + '-' + second

		# If its not in the dictionary then add it in
		if not check_dict.get(res):
			check_dict[res] = count
			count += 1


		output_res = first.split('-')

		for x in output_res:
			output.append(int(x))




		index += 1

	# -1 index is the last index in an array
	output.append(int(num_list[-1]))
	#print(output)
	
	for i in output:
		decoded += chr(i)

	return decoded


# Command line arguements
if len(sys.argv) == 3:  # An option and then the file
	mode = sys.argv[1]
	file = sys.argv[2]

	if mode == '-e':
		compressFile(file)

	elif mode == '-d':
		decompressFile(file)


else:
	print('Usage: lzw.py [-e[-d]] [file]') # If None of these options have been specified display the usage 
	sys.exit() # Terminate the program



'''
# Tests
word_list = ['thisisthe']
#word_list = ['thisisthe']
for x in word_list:
	text = x                            
	res = compress(text)
	print(res)
	res = decompress(res)
	print(res)
	print()
	print()
'''
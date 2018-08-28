import os

'''

This script checks the pupil co-ordinates
It can be run to verify if all the data was processed correctly
Use total to check if any missing
Use count to check how many wrong

'''

path = "Coordinates/Data/RPack/"
count = 0
total = 0
for filename in os.listdir(path):
	if os.path.exists(path + filename):
		print (path + filename)
		if (filename == ".DS_Store"):
			continue

		curr = open(path + filename, 'r')
		total = total + 1
		right = curr.readline().split(" ")
		left = curr.readline().split(" ")
		if (not right[0] or not right[1] or not left[0] or not left[1]):
			print ("----- WRONG ------")
			print (filename)
			print (right)
			print(left)
			count = count + 1
	else:
		print (filename)
		count = count + 1

print ("Total: " + str(total))
print ("Wrong:" + str(count))
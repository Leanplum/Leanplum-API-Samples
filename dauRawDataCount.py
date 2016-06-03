# Parses through the raw data
# This script assumes that you used the dataExport.py from Leanplum
#(c) Leanplum 2016

def dau_count(date_analyze, num_files):
	""" This function is to get a count of unique users of a DAU """ 

	unique_users = set()
	for num in range(int(num_files)):
		file_name = str(date_analyze) + "DataExport" + str(num)
		print "Looking into " + file_name
		currentFile = open(file_name, "r")
		for line in currentFile.readlines(): 
			data = json.loads(line)
			if data['isSession']==True: 
				unique_users.add(data['userId'])

	new_unique_users = list(unique_users)
	confirm = raw_input('Would you like a list of userIds saved? Y/N  ')
	if 'y' in confirm.lower():
		unique_file_name = 'NewuniqueUsersListDataExport' + str(date_analyze)
		for line in range(len(new_unique_users)):
			f = open(unique_file_name, 'a')
			f.write(new_unique_users[line]+'\n')
			f.close
	else:
		print "There were " + str(len(new_unique_users)) + " users on " + str(date_analyze)

def main():
	date_analyze = raw_input('Date of files: ')
	num_files = raw_input('Number of files: ')
	dau_count(date_analyze, num_files)

if __name__ == "__main__":
    main()
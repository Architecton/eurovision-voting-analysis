import csv
import numpy as np

file_name = "eurovision-final.csv"

# TODO: Add trace for testing/debugging
def read_file(file_name):
	# Open data file
	with open(file_name, "rt", encoding="latin1") as f:

		# Read lines from csv file into numpy array
		raw_data = np.array(list(csv.reader(f)))

		# Get names of countries (as names of rows 17-63)
		country_names = raw_data[0, 16:63]

		# Trim whitespace from start and end.
		country_names = list(map(lambda x: x.strip(), country_names))

		# Handle country name conflict between name in rows and name in columns
		country_names[country_names.index("Serbia & Montenegro")] = "Serbia and Montenegro"
		
		# Create empty dictionary for storing cleaned data.
		processed_data = dict()

		# There are 47 countries participating/voting.
		NUM_COUNTRIES = 47

		# Get names of columns.
		col_names = list(map(lambda x: x.strip(), raw_data[0, :]))

		# Handle country name conflict between name in rows and name in columns
		col_names[col_names.index("Serbia & Montenegro")] = "Serbia and Montenegro"

		# Create rows in processed data matrix.
		for country in country_names:
			bins = np.zeros([1, NUM_COUNTRIES], dtype = int) 		# Create bins.
			index_row = col_names.index(country) 					# Get index of column representing votes from this country.

			# Go over performing countries across all years.
			for i in range(1, raw_data.shape[0]):
				bin_index = country_names.index(raw_data[i, 1].strip()) 	# Compute index of bin for next performance
				val = raw_data[i, index_row] 								# Get number of points awarded by country A (If data exists).
				try:
					points = int(val) 								# Try to convert value to an integer.
					bins[0, bin_index] += points 					# If successfully converted, add to bin.
				except ValueError:
					pass
			processed_data[country] = bins 							# Add country data to dictionary representing the processed data.

		# Return dictionary representing the processed data
		return processed_data

data = read_file(file_name)

# Notes to self:
"""
	Rows are countries (columns in original file (Q - BK / 17 - 63/) - 47 columns)
	in list comprehension: l[0][16:63] # select names of countries -> keys

	Note that country names are sometimes ended with a space -> trim.

	For each country A:
		- make bins corresponding to each other country i.
		- in each bin, sum votes from country A for this country i.

	Summing votes for each country i from country A:
		- There are 47 countries voting.
		- Make a tuple of names of countries (column names 17 - 63).
		- indices of names of countries are also indices in the bins list.
		- go over all rows representing votes.
		- get name (and from name, the index) from row name.
		- add value in row to appropriate bin.
		- add entry to data dict
"""
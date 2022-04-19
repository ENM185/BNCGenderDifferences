import os

'''
ORIGINAL DATA IS PULLED FROM BNC CORPUS VIA:
MALE = [lemma != ".*_(PUNC|STOP|UNC)"] :: match.u_sex = 'male';
FEMALE = [lemma != ".*_(PUNC|STOP|UNC)"] :: match.u_sex = 'female';

total male = 5654348
total female = 3825804
total tokens with u_sex being male or female = 9480152

m/t = 0.5964
f/t = 0.4036
tolerance = 0.10
m-proportionate if in [0.4964, 0.6964]
f-proportionate if in [0.3036, 0.5036]
'''

MALE_TO_TOTAL = 0.5964
FEMALE_TO_TOTAL = 0.4036
TOLERANCE = 0.10

# Step 0: Ensure data directories
INPUT_DIR = os.path.join('.', 'input')
OUTPUT_DIR = os.path.join('.', 'output')
for directory in [INPUT_DIR, OUTPUT_DIR]:
	if not os.path.exists(directory):
		os.makedirs(directory)

# Step 1: Congreate all the data
token_sex_counts = {} # { token: { male: int, female: int }, ... }
for file in ['male_bnc.csv', 'female_bnc.csv']:
	sex = file.split('_')[0]
	with open(os.path.join(INPUT_DIR, file), mode='r', encoding='utf+8') as f:
		lines = f.readlines()
		for line in lines:
			token, count = line.split(',')
			if token not in token_sex_counts:
				token_sex_counts[token] = { 'male': 0, 'female': 0 }
			token_sex_counts[token][sex] = int(count)

# Step 2: Determine which words are disproportionate
with open(os.path.join(OUTPUT_DIR, 'disproportionate.csv'), mode='w', encoding='utf+8') as f:
	print('hw_pos,mcount,fcount', file=f)
	for token, counts in token_sex_counts.items():
		total = sum(counts.values())

		# Mutually exclusive proportions -> only need to check one of the sexes
		male_proportion = counts['male'] / total
		is_lower = male_proportion < MALE_TO_TOTAL - TOLERANCE
		is_higher = male_proportion > MALE_TO_TOTAL + TOLERANCE

		if is_lower or is_higher: # i.e. outside proportion range
			print(f"{token},{counts['male']},{counts['female']}", file=f)

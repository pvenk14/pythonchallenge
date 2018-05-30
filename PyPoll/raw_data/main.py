# Modules
import os
import csv
import operator

election_csv = os.path.join("election_data_2.csv")

# Lists to store data
Candidate_name_vote ={}

Total =0
winner =0

with open(election_csv, newline="") as csvfile:
    csvreader = list(csv.reader(csvfile, delimiter=","))
    for row in csvreader[1:]:
    	name = row[2]
    	if name in Candidate_name_vote:
    		Candidate_name_vote[name] += 1

    	else: 
    		Candidate_name_vote[name] =1
    	Total = Total +1



with open("Output.txt", "w") as textfile:
	print (f'Election Results',file=textfile)
	print(f'-------------------------',file=textfile)
	print (f'Total Votes: {Total}',file=textfile)
	print(f'-------------------------')
	for CandidateName,Vote in Candidate_name_vote.items():
		print(f'{CandidateName} : {(Vote/Total)*100}%  ({Vote})',file=textfile)
	
	print(f'-------------------------',file=textfile)

	print (f'Winner: {max(Candidate_name_vote.items(), key=operator.itemgetter(1))[0]}',file=textfile)

	print(f'-------------------------',file=textfile)

print (f'Election Results')
print(f'-------------------------')
print (f'Total Votes: {Total}')
print(f'-------------------------')
for CandidateName,Vote in Candidate_name_vote.items():
	print(f'{CandidateName} : {(Vote/Total)*100}%  ({Vote})')


print(f'-------------------------')

print (f'Winner: {max(Candidate_name_vote.items(), key=operator.itemgetter(1))[0]}')

print(f'-------------------------')
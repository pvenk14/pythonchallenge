# Modules
import os
import csv
import operator
import datetime

emp_csv = os.path.join("employee_data1.csv")
employee_record =[]

us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


with open(emp_csv, newline="") as csvfile:
    csvreader=list(csv.reader(csvfile, delimiter=","))
    for row in csvreader[1:]:
    	# Add emp id
    	emp_id = row[0]
    	first_name,last_name = row[1].split(' ')
    	dob= datetime.datetime.strptime(row[2], "%Y-%m-%d").strftime('%d/%m/%Y')
    	ssn = row[3].split('-')
    	ssn_new= '***-**-'+ssn[2]
    	state = us_state_abbrev[row[4]]

    	employee_record.append([emp_id,first_name,last_name,dob,ssn_new,state])

output_file = os.path.join("output.csv")

#  Open the output file
with open(output_file, "w", newline="") as datafile:
    writer = csv.writer(datafile)

    # Write the header row
    writer.writerow(["EMPID", "First Name", "Last Name", "DOB",
                     "SSN", "State"])

    # Write in zipped rows
    writer.writerows(employee_record)
print(employee_record)



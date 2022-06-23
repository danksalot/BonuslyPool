import requests
import csv
import math

USERNAME = 0
EMAIL = 1
TOKEN = 2
BALANCE = 3

participants = []

with open('users.csv') as users_file:
	csv_reader = csv.reader(users_file)
	for line in csv_reader:
		token = line[1]
		response = requests.get("https://bonus.ly/api/v1/users/me?access_token=" + token)
		data = response.json()
		if data['success']:
			participants.append([
					data['result']['username'],
					data['result']['email'],
					token,
					data['result']['giving_balance']
				])

for participant in participants:
	recipients = [x for x in participants if x[USERNAME] != participant[USERNAME]]
	if len(recipients) > 0:
		amount = math.floor(participant[BALANCE]/len(recipients))
		for recipient in recipients:			
			tmpHeaders = { 'Authorization' : 'Bearer ' + participant[TOKEN] }
			tmpData = { 
					'receiver_email': recipient[EMAIL], 
					'amount': amount, 
					'hashtag': '#connection', 
					'reason': 'for contributing to the group'
				}
			response = requests.post('https://bonus.ly/api/v1/bonuses', headers = tmpHeaders, data = tmpData)
			data = response.json()
			if data['success']:
				print('Sent ' + str(amount) + ' from ' + participant[USERNAME] + ' to ' + recipient[USERNAME])
			else:
				print(data)


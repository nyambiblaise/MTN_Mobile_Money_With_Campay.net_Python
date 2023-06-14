import requests
import json
import uuid
import time

import warnings
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

class Client():

	def __init__(self, kwargs):
		self.app_username = kwargs["app_username"]
		self.app_password = kwargs["app_password"]
		self.environment = kwargs["environment"] #DEV, PROD
		self.host = "https://demo.campay.net" if self.environment == 'DEV' else "https://www.campay.net"
		self.debug = True if self.environment == 'DEV' else False

		# print(kwargs)

	def get_token(self):
		#Get Access token

		token_headers = {
			"Content-Type":"application/json"
		}
		
		data = {
			"username":self.app_username,
			"password":self.app_password
		}

		json_data = json.dumps(data)
		token_response = requests.post(self.host+'/api/token/', data=json_data, headers=token_headers, verify=False)
		
		got_json_response = False
		try:
			json_token_response = token_response.json()
			got_json_response = True
		except:
			pass

		if got_json_response:
		
			token_response_response_status_code = int(token_response.status_code)

			if token_response_response_status_code == 200:
				token = json_token_response['token']
				is_successful = True
			else:
				token = None
				is_successful = False

				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", json_token_response)
			
			return {"token":token, "is_successful":is_successful}

		else:
			return {"token":None, "is_successful":False}

	
	def collect(self, values):
		if self.debug:
			print(">>>>>>>>>>>>>>>>>>: ", "Collecting...")

		token = self.get_token()["token"]
		
		if token:

			#### Request collect
			collect_data = {
				"amount":str(values["amount"]),
				"currency": str(values["currency"]),
				"from":str(values["from"]),
				"description":str(values["description"]),
				"external_reference":str(uuid.uuid4())
			}
			collect_payload = json.dumps(collect_data)
			collect_headers = {
				'Authorization': 'Token '+token,
				'Content-Type': 'application/json'
			}
			collect_response = requests.post(self.host+'/api/collect/', data=collect_payload, headers=collect_headers, verify=False)
			
			got_json_response = False
			try:
				collect_response_json = collect_response.json()
				got_json_response = True
			except:
				pass
			
			if got_json_response:
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", collect_response_json)
					
				collect_response_status_code = int(collect_response.status_code)
				if collect_response_status_code == 200:
					reference = collect_response_json['reference']
					print(">>>>>>>>>>>>>>>>>>: Confirm on phone...")
					is_successful = True
				else:
					reference = None
					is_successful = False

				if is_successful:
					####Check Transaction Status
					status_headers = {
						'Authorization': 'Token '+token,
						'Content-Type': 'application/json',
					}
					
					status = "PENDING"
					while status == "PENDING":
						time.sleep(5)
						status_response = requests.get(self.host+"/api/transaction/"+reference, headers=status_headers, verify=False)
						
						got_json_response = False
						try:
							status_response_json = status_response.json()
							got_json_response = True
						except:
							pass
						
						if got_json_response:
							status_response_status_code = int(status_response.status_code)
							if status_response_status_code == 200:
								status = status_response_json['status']
								
								if status != "PENDING":
									if self.debug:
										print(">>>>>>>>>>>>>>>>>>: ", status_response_json)
									return status_response_json
							else:
								pass

				else:
					message = collect_response_json["message"]
					if self.debug:
						print(">>>>>>>>>>>>>>>>>>: ", message)
					return {"status":"FAILED", "message": message}

			else:
				message = "Collect error"
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", message)
				return {"status":"FAILED", "message":message}

		else:
			message = "Token error. Please check your App Username and Pass password. Also check your environment"
			if self.debug:
				print(">>>>>>>>>>>>>>>>>>: ", message)
			return {"status":"FAILED", "message":message}


	def disburse(self, values):
		if self.debug:
			print(">>>>>>>>>>>>>>>>>>: ", "Disbursing...")
		token = self.get_token()["token"]
		if token:

			#### Request withdraw
			withdraw_data = {
				"amount":str(values["amount"]),
				"currency": str(values["currency"]),
				"to":str(values["to"]),
				"description":str(values["description"]),
				"external_reference":str(uuid.uuid4())
			}
			withdraw_payload = json.dumps(withdraw_data)
			withdraw_headers = {
				'Authorization': 'Token '+token,
				'Content-Type': 'application/json'
			}
			withdraw_response = requests.post(self.host+'/api/withdraw/', data=withdraw_payload, headers=withdraw_headers, verify=False)
			
			got_json_response = False
			try:
				withdraw_response_json = withdraw_response.json()
				got_json_response = True
			except:
				pass
			
			if got_json_response:
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", withdraw_response_json)
					
				withdraw_response_status_code = int(withdraw_response.status_code)
				if withdraw_response_status_code == 200:
					reference = withdraw_response_json['reference']
					is_successful = True
				else:
					reference = None
					is_successful = False

				if is_successful:
					####Check Transaction Status
					status_headers = {
						'Authorization': 'Token '+token,
						'Content-Type': 'application/json',
					}
					
					status = "PENDING"
					while status == "PENDING":
						time.sleep(5)
						status_response = requests.get(self.host+"/api/transaction/"+reference, headers=status_headers, verify=False)
						
						got_json_response = False
						try:
							status_response_json = status_response.json()
							got_json_response = True
						except:
							pass
						
						if got_json_response:
							status_response_status_code = int(status_response.status_code)
							if status_response_status_code == 200:
								status = status_response_json['status']
								
								if status != "PENDING":
									if self.debug:
										print(">>>>>>>>>>>>>>>>>>: ", status_response_json)
									return status_response_json
							else:
								pass

				else:
					message = withdraw_response_json["message"]
					if self.debug:
						print(">>>>>>>>>>>>>>>>>>: ", message)
					return {"status":"FAILED", "message": message}

			else:
				message = "Disburse error"
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", message)
				return {"status":"FAILED", "message":message}

		else:
			message = "Token error. Please check your App Username and Pass password. Also check your environment"
			if self.debug:
				print(">>>>>>>>>>>>>>>>>>: ", message)
			return {"status":"FAILED", "message":message}


	def get_balance(self):
		if self.debug:
			print(">>>>>>>>>>>>>>>>>: ", "Getting balance...")
		token = self.get_token()["token"]
		if token:
			status_headers = {
				'Authorization': 'Token '+token,
				'Content-Type': 'application/json',
			}
			response = requests.get(self.host+"/api/balance/", headers=status_headers, verify=False)
									
			got_json_response = False
			try:
				response_json = response.json()
				got_json_response = True
			except:
				pass

			if got_json_response:
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", response_json)
				return response_json
				
			else:
				message = "Balance error"
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", message)
				return {"status":"FAILED", "message":message}

		else:
			message = "Token error. Please check your App Username and Pass password. Also check your environment"
			if self.debug:
				print(">>>>>>>>>>>>>>>>>>: ", message)
			return {"status":"FAILED", "message":message}



	def get_payment_link(self, values):
		if self.debug:
			print(">>>>>>>>>>>>>>>>>>: ", "Getting payment link...")

		token = self.get_token()["token"]
		
		if token:

			#### Request collect
			collect_data = {
				"amount":str(values["amount"]),
				"currency": str(values["currency"]),
				"description":str(values["description"]),
				"external_reference":str(values["external_reference"]),
				"redirect_url":str(values["redirect_url"])
			}
			collect_payload = json.dumps(collect_data)
			collect_headers = {
				'Authorization': 'Token '+token,
				'Content-Type': 'application/json'
			}
			collect_response = requests.post(self.host+'/api/get_payment_link/', data=collect_payload, headers=collect_headers, verify=False)
			
			got_json_response = False
			try:
				collect_response_json = collect_response.json()
				got_json_response = True
			except:
				pass
			
			if got_json_response:
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", collect_response_json)
					
				collect_response_status_code = int(collect_response.status_code)
				if collect_response_status_code == 200:
					link = collect_response_json['link']
					if self.debug:
						print(">>>>>>>>>>>>>>>>>>: Redirect your customer to the payment link...")
					is_successful = True
				else:
					link = None
					is_successful = False

				if is_successful:
					####Check Transaction Status
					return {"status":"SUCCESSFUL", "link": link}

				else:
					message = collect_response_json["message"]
					if self.debug:
						print(">>>>>>>>>>>>>>>>>>: ", message)
					return {"status":"FAILED", "message": message}

			else:
				message = "Collect error"
				if self.debug:
					print(">>>>>>>>>>>>>>>>>>: ", message)
				return {"status":"FAILED", "message":message}

		else:
			message = "Token error. Please check your App Username and Pass password. Also check your environment"
			if self.debug:
				print(">>>>>>>>>>>>>>>>>>: ", message)
			return {"status":"FAILED", "message":message}


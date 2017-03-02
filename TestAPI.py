import json  
import requests
import sys
import logging as log
import os


class TestAPI():	
	def preconfig(self):		
		filename = 'D:\example1.log'
		try:
			os.remove(filename)
		except OSError:
			pass
		log.basicConfig(filename='D:\example1.log',level=log.INFO)
		
	def list_all_user(self, url, total, exp_code):	
		try:
			#Step 1: - Get all users from url
			log.info("Step 1: - Get all users from url")
			response = requests.get(url)
			json_obj = json.loads(response.text)
			response.close()
			#Step 2: - Verify status code			
			
			if response.status_code == exp_code:
				log.info("Pass: Server returns status code: " + str(exp_code))
			else:
				log.info("Fail: Server returns status code:" + str(response.status_code))
				return 0
			
			
			#- Verify the number of user. If count = total then test case Pass, else test case Fail
			count = len(json_obj)
			
			if count == total:
				log.info("Pass: The number of users are correct: " + str(count))
				return 1
			else:
				log.info("Fail: The number of users are wrong: " + str(count))
				return 0		
			
		except:
			e = sys.exc_info()[0]
			print e
			log.info(e)

	def lookup(self, dic, keys):
		'''
		This function is used to look up a value in a nested dictionary	
		'''	
		tmp_dic = dic
		for key in keys:
			tmp_dic = tmp_dic[key]
		
		return tmp_dic	 
		
		
	def update_value(self, dic, keys, value):
		'''
		This function is used to update a value in a nested dictionary	
		'''	
		tmp_dic = dic
		for index in range(len(keys)-1):
			tmp_dic = tmp_dic[keys[index]]
			
		tmp_dic[keys[-1]] = value
		
		return 	 	
		
		
	def find_user(self, url, keywords, exp_code):
		'''
		keywords is defined as dictionary with 1 or multiple parameters
		Example:
			keywords = {"address.street":"Kattie Turnpike", "name":"Clementina DuBuque"}
		'''
		try:
			#Step 1: Set up the new url to find user
			log.info("Step 1: Set up the new url to find user") 
			tmp_url = "?" 
			for key in keywords.keys():
				tmp_url = tmp_url + key + "=" + keywords[key].replace(" ","+") + "&"					
			tmp_url = url + tmp_url
			#- Get result from the server
			response = requests.get(tmp_url)
			json_obj = json.loads(response.text)
			response.close()	
			
			#Step 2: - Verify status code
			print response.status_code
			if response.status_code == exp_code:
				log.info("Pass: Server returns status code: " + str(exp_code))
			else:
				log.info("Fail: Server returns status code:" + str(response.status_code))
				return 0
				
			#- Verify the result is correct
			result = True
			for key in keywords.keys():
				tmp_key = key.split('.')
				for record in json_obj:
					ret_value = self.lookup(record,tmp_key) #Get value from response
					if ret_value != keywords[key]:
						result = False
						break
			
			if result:
				log.info("Pass Find "+ str(len(json_obj)) +" user")
				return 1
			else:
				log.info("Fail: Cannot find user")
				return 0		
			
		except:
			e = sys.exc_info()
			print e
			log.info(e)
		
		
	def update_user(self, url, user_id, keywords, exp_code):
		'''
		keywords is defined as dictionary with 1 or multiple parameters
		Example:
			keywords = {"address.street":"Kattie Turnpike", "name":"Clementina DuBuque"}
		'''
		try:
			# Get the record need to be updated
			tmp_url = url+"/"+str(user_id)		
			response = requests.get(tmp_url)
			json_obj = json.loads(response.text)
			response.close()
			#Update record with new value
			for key in keywords:
				tmp_key = key.split('.')
				self.update_value(json_obj,tmp_key,keywords[key])
			
			#Send updated user to server
			response = requests.put(tmp_url,json_obj)
			json_obj = json.loads(response.text)
			response.close()
			
			#Step 1: Verify status code
			if response.status_code == exp_code:
				log.info("Pass: Server returns status code: " + str(exp_code))
			else:
				log.info("Fail: Server returns status code: " + str(response.status_code))
			
		except:
			e = sys.exc_info()
			print e
			log.info(e)	


	
def main():
	try:
		TestAPI().preconfig()
		url = "https://jsonplaceholder.typicode.com/users"
		log.info("------------------------------------------")
		log.info("Test case 1. List all user")		
		TestAPI().list_all_user(url,10,200)		
		log.info("------------------------------------------")
		
		log.info("------------------------------------------")
		log.info("Test case 2. Find a user")
		TestAPI().find_user(url,{"address.street":"Kattie Turnpike", "name":"Clementina DuBuque"},200)
		log.info("------------------------------------------")
		
		log.info("------------------------------------------")
		log.info("Test case 3. Update a user")
		TestAPI().update_user(url,1,{"address.street":"Test Test", "name":"This is updated"},200)
		log.info("------------------------------------------")
		
		log.info("------------------------------------------")
		log.info("Test case 4. Negative test case: update user who does not exist : id=20")
		TestAPI().update_user(url,20,{"name":"New name"},404)
		log.info("------------------------------------------")	

		
	except:
		e = sys.exc_info()
		print e
		log.info(e)
	

if __name__ == "__main__":
	main()





	
	

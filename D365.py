from locust import HttpUser, task, between, TaskSet
import time,sys,json
from faker import Faker

# variables.
#just declare these global to make things easy.
global d365,clientid,secret,tokendpoint

d365 = 'https://jaldev09017a96d09905665265devaos.cloudax.dynamics.com'
clientid = ''
secret = '' 
tenant = ''

tokenendpoint = f'https://login.microsoftonline.com/{tenant}/oauth2/token'  #oauth token endpoint
tokenpost = {
	'client_id':clientid,
	'client_secret':secret,
	'grant_type':'client_credentials',
	'resource':d365
	}

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def readcustomergroups(self):
        print("get CustomerGroups")
        CustomerGroups = self.client.get("/data/CustomerGroups", headers=requestheaders)
        CustomerGroups_response_dict = CustomerGroups.json()
        print("CustomerGroups",CustomerGroups_response_dict)

    @task
    def createcustomergroup(self):
        faker = Faker()
        name = faker.first_name()
        print("add CustomerGroups")
        CustomerGroup = {
            'dataAreaId':'usmf',
            'CustomerGroupId':name,
            'Description':name
        }
        CustomerGroups = self.client.post("/data/CustomerGroups", headers=requestheaders, json=CustomerGroup)
        CustomerGroups_response_dict = CustomerGroups.json()
        print("CustomerGroups",CustomerGroups_response_dict)

    @task
    def updatecustomergroup(self):
        faker = Faker()
        name = faker.first_name()
        print("add CustomerGroups")
        CustomerGroup = {
            'dataAreaId':'usmf',
            'CustomerGroupId':name,
            'Description':name
        }
        CustomerGroups = self.client.post("/data/CustomerGroups", headers=requestheaders, json=CustomerGroup)
        CustomerGroups_response_dict = CustomerGroups.json()
        print("CustomerGroups",CustomerGroups_response_dict)
        #start the update
        CustomerGroup = {
            'dataAreaId':'usmf',
            'CustomerGroupId':name,
            'Description': name,
        }
        body = json.dumps({
            "Description": "updated"
        })
        print(f"Updating customer group {name}")
        CustomerGroups = self.client.patch(f"/data/CustomerGroups(dataAreaId=\'usmf\',CustomerGroupId=\'{name}\')", headers=requestheaders,data=body)

    @task
    def deletecustomergroup(self):
        faker = Faker()
        name = faker.first_name()
        print("add CustomerGroups")
        CustomerGroup = {
            'dataAreaId':'usmf',
            'CustomerGroupId':name,
            'Description':name
        }
        CustomerGroups = self.client.post("/data/CustomerGroups", headers=requestheaders, json=CustomerGroup)
        CustomerGroups_response_dict = CustomerGroups.json()
        print("CustomerGroups",CustomerGroups_response_dict)
        self.client.delete(f"/data/CustomerGroups(dataAreaId=\'usmf\',CustomerGroupId=\'{name}\')", headers=requestheaders)
        print("deleted %s" % (name))

    def on_start(self):
        print("logging in")
        token = self.client.post(tokenendpoint, tokenpost)
        global accesstoken
        accesstoken = token.json()['access_token']
        print(accesstoken)
        global requestheaders
        requestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'content-type': 'application/json'
        }

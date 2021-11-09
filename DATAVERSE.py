from locust import HttpUser, task, between, TaskSet
import time,sys,json
from faker import Faker

# variables.
#just declare these global to make things easy.
global d365,clientid,secret,tokendpoint,authurl

d365 = 'https://operations-jal2018.crm.dynamics.com'
clientid = ''
secret = ''
version = '9.1' 
webapiurl = f'{d365}/api/data/v{version}'
tenant = 'jlarsondemo.onmicrosoft.com'
tenantid = ''
scope = f"{d365}/.default"
authurl = f'https://login.microsoftonline.com/{tenantid}/oauth2/v2.0/token'
webapiurl = f'{d365}/api/data/v{version}'

tokenpost = {
	'client_id':clientid,
	'client_secret':secret,
	'grant_type':'client_credentials',
	'scope':scope
	}

class QuickstartUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def readaccounts(self):
        print("get accounts")
        accounts = self.client.get(f'{webapiurl}/accounts?$top=3', headers=requestheaders)
        accounts_response_dict = accounts.json()
        print("accounts",accounts_response_dict)

    def on_start(self):
        print("logging in")
        print(authurl)
        print(tokenpost)
        token = self.client.post(authurl, tokenpost)
        print(token)
        #global accesstoken
        accesstoken = token.json()['access_token']
        #print(accesstoken)
        global requestheaders
        requestheaders = {
            'Authorization': 'Bearer ' + accesstoken,
            'content-type': 'application/json'
        }

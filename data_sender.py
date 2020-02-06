import requests, json

class Data_sender():

    def __init__(self, url):
        self.url = url

    def send_data(self, measurements):
        response = requests.post(self.url, data=json.dumps(measurements))
        print("-"*20)
        print(response)
        print("")
        print (response.content)
        print("-"*20)
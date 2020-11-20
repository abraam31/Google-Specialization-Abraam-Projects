
import os 
import requests

def http_post_request(url, path):
    os.chdir(path)
    feedbacks=os.listdir()

############ The feedback is inserted in separate file, with title, name,
########### date, content, each in a separate line. A 4-line file.
    for feedback in feedbacks:
        with open(feedback) as f:
            content=f.readlines()
            data_dic=dict()
########## In this step, fetching each attribute and assign to a variable
            title=content[0].strip("\n")
            name=content[1].strip("\n")
            date=content[2].strip("\n")
            feedback=content[3].strip("\n")
######### In this step, collecting the attributes, and inserting it in a    
######### appropriate json dictionary

            data_dic["title"]=title
            data_dic["name"]=name
            data_dic["date"]=date
            data_dic["feedback"]=feedback

########### After the data is organised, json dic is pushed in a http post request 
            response=requests.post(url, data=data_dic)
########### Print the status code
            print(response.status_code)

url=str(input("Enter your website API URL: "))
path=str(input("Enter the path for your feedback directory"))
http_post_request(url, path)

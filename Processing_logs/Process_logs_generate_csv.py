import os
import re
from operator import itemgetter
import csv
import subprocess
from collections import OrderedDict

def count_logs(filename):
    #Creating dictionaries to be used in log processing
    error_dic={} ### Count occurence of each error message
    error_user_dic={} ### Count occurence when each user caused an error message
    debug_user_dic={} ### Count occurence of debugged logs from each user

    ########### Opening the syslog file to fetch the logs
    with open(filename, "r") as syslog:
        error_logs=syslog.readlines()

    #### Iterating over each log in the log file
        for line in error_logs:
            arranged=" ".join(line.split()) ##Removing the new line chars and re-joining the lines

    ### Catching error in 2 different pattern: 1 for error message, and 1 for user causing the error
            
            general_error=re.search(r' ERROR .*', arranged)
            exact_error=re.search(r'ERROR ([\w ]*)', arranged) 

    #### Skip if no error regex found. Else assign the error in the error var.
            if exact_error==None:
                continue
            else:
                error=exact_error[0]
            
    ###### Skipping the error word, and take over from after and insert it in the error dic
            if error[6:] in error_dic:
                error_dic[error[6:]]+=1
            else:
                error_dic[error[6:]]=1

    ##### (oriented with the project logging style) -- Catching error from Users
    ####  Find a specific pattern in the 2nd error var (Only word chars) in between ()
    #### repeting any number of time then assign what is in between of the ()

            new=re.search (r'\([\w\.]*\)', general_error[0])
            if new==None:
                continue
            else:
                name=new[0]
                user=name[name.find("(")+1:name.find(")")]

    #### Add number of errors to each user
                if user in error_user_dic:
                    error_user_dic[user]+=1
                else:
                    error_user_dic[user]=1

    #### Repeating same thing but for Debugged log instead of error logs and insert 
    ### it in the debug dictionary

        for line in error_logs:
            arranged=" ".join(line.split())
            debug=re.search(r' INFO .*', arranged)
            if debug==None:
                continue
            else:
                info=re.search(r'\(([\w\.]*)\)', debug[0])
                if info==None:
                    continue
                else:
                    temp=info[0]
                    user_info=temp[1:-1]
                    if user_info in debug_user_dic:
                        debug_user_dic[user_info]+=1
                    else:
                        debug_user_dic[user_info]=1
### Ordering the dictionary for presentation purposes
    temp_error_dic=sorted(error_dic.items(), key=itemgetter(1), reverse=True)
    temp_error_user_dic=sorted(error_user_dic.items())
    temp_info_dic=sorted(debug_user_dic.items())
    sorted_error_dic = OrderedDict(temp_error_dic)
    sorted_error_user_dic = OrderedDict(temp_error_user_dic)
    sorted_info_dic = OrderedDict(temp_info_dic)

    ########### The function can be modified to match any expressions
    return sorted_error_dic, sorted_error_user_dic, sorted_info_dic

######## Creating the csv file with number of error occurence
########## From values in sorted_error_dic
def error_csv_generate():
    with open("error_message.csv", "w+", newline='') as file:
        fieldnames = ['Error', 'Count']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for key in sorted_error_dic:
            writer.writerow({'Error': key, 'Count': sorted_error_dic[key]})
        file.close()

########### Creating a user stats csv file with number of logs per user
############# and number of error logs per user also

def user_stats_generate():
    with open("user_statistics.csv", "w+", newline='') as file1:
        fieldnames1 = ['Username', 'INFO', 'ERROR']
        writer = csv.DictWriter(file1, fieldnames=fieldnames1)
        writer.writeheader()
        for key in sorted_error_user_dic:
            writer.writerow({'Username': key, 'INFO': sorted_info_dic.get(key, 0), 'ERROR': sorted_error_user_dic[key]})
        file.close()

#### Taking the log file in stdin
logfile=str(input("Enter the log file you want to process .. "))

#### Catching returned dicts
sorted_error_dic, sorted_error_user_dic, sorted_info_dic = count_logs(logfile)

error_csv_generate()
user_stats_generate()
### EOF

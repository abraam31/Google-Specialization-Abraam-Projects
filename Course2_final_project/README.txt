The project was to process the syslog on the Webserver and find the following
	1- Most occuring error generated in the log file
	2- User generating the highest number of errors
	3- Create a csv report with the most occuring errors in an ordered way
	4- create a csv report for each user with number of errors and number of debugs caused by the user, also in an ordered way

Code is consisted of 3 functions: 
	- count_logs() for processing logs, counting and inserting data in dictionaries 
	- error_csv_generate to generate the error csv file from data return of 1st function 
	- user_stats_generate to do the same for user stats

This project is about parsing an XML file with some data in it. 
The XML file holds here data about songs, album and artists, and some other related data.

After data is fetched and assigned to vars, it is inserted in a local sqllite database with created database and table in the script as well.

3 functions in the script
	1- lookup. Take key as input for function and search for the value of this key, and return it.
	2- manip_database. Simply connect to dba and create tables and database.
	3- parsing_xml. The main function where the data is processed by the help of the lookup function and inserted in the database created 
	   in the manip_database function

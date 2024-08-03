# RocketBot
Discord bot for Rocket League Lithuania league tournaments. Uses PostgreSQL for storing team information in a database (no sensitive data).


# PostgreSQL set-up
Install PostgreSQL on your server/computer. If hosted externally, make sure that it is possible to connect with IPs outside the local range.

In the root folder of the repository, create a file named `database.ini` and paste the following information:
```
[postgresql]
host=<server ip address (defaults to port 5432)>
database=<database name>
user=postgres
password=<password>
```

Database schema will be provided in later commits, however can be derived from sql_helper.py file.

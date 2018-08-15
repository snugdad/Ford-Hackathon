	
	Have as few as possible endpoints in some schema designed to locate URI resource for download
	https://fordappstore.42king.com/api/listapps?ford_only=y&

TABLES
	>AppList Table
		>contains a list of apps on the store
	>Application metadata
	>To be computed on server side:
		> SHA256 hash of zip file
			*Do not extract if hash does not match server cache
		> Walk extracted directory obtaining SHA256 of each file
			hex add all of the values together - TOTAL = total checksum
		>contains all relevant metadata
		for apps
	>User metadata
	>HMAC cache of relational data that is generated on the fly per session via endpoint access

CAN scale horizontally with cassandra indexing on Users & APP Ids

Endpoints:

	verifyapps?ids=<appid>,<appid>,<appid>

	Has an in memory store in redis of each apps most updated version. will make queries from clients who have just installed the app or need to verify integrity of local files. Be passing a list of apps or a task_list of apps to verify. example(at boot verify all things that are installed)
.




	listapps?
	conn = redis_connect(127.0.0.1, 2366)

	if (query = redis_query(conn, apps))
		return (query)
	
	if (!mysql_conn = mysql_connect(127.0.0.1, 3306))
		return ("CONNECTION ERROR SQL")
	query = mysql_query(mysql_conn, AppList_Table)
	response = redis_set(conn, apps, query)
	

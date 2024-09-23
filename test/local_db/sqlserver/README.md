**Local SQL Server Setup**

**Prerequisites**

-  Ensure you have docker desktop or wsl in you own PC
-  Docker and Docker Compose installed in wsl
-  ODBC Driver 17 for SQL Server installed in Windows

**Steps**
1. Open WSL/Docker Desktop
2. Execute command :`cd test/local_db/sqlserver` 
3. Execute `./build.sh` to build sqlserver_local image 
4. Execute `./startDB.sh` to start docker container
5. Set Local Connect String
   ```
        "local" : {
                "username" : "fc_read",
                "password" : "SQBoard!Passw0rd",
                "host":"127.0.0.1,1433",
                "DB.host":"127.0.0.1,1433",
                "database":"LOCAL_DEV"
            },

       "fc_db" : {
           "username" : "fc_ddl",
           "password" : "SQBoard!Passw0rd",
           "host":"127.0.0.1,1433",
           "DB.host":"127.0.0.1,1433",
           "database":"LOCAL_DEV"
       }
```
6. Execute `./stopDB.sh` to stop local DB


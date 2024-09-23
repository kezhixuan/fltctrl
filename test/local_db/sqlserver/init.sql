-- Create the LOCAL_DEV database
CREATE DATABASE LOCAL_DEV;
GO
-- Create the fc_read user with read-only access
CREATE LOGIN fc_read WITH PASSWORD = 'SQBoard!Passw0rd';
GO
CREATE LOGIN fc_ddl WITH PASSWORD = 'SQBoard!Passw0rd';
GO

-- Switch to the LOCAL_DEV database
USE LOCAL_DEV;
GO
CREATE USER fc_read FOR LOGIN fc_read;
GO
CREATE USER fc_ddl FOR LOGIN fc_ddl;
GO
ALTER ROLE db_datareader ADD MEMBER fc_read;
GO
ALTER ROLE db_owner ADD MEMBER fc_ddl;
GO

CREATE SCHEMA SQ AUTHORIZATION dbo;
GO
GRANT CONTROL ON SCHEMA::SQ TO fc_ddl;
GO
GRANT SELECT ON SCHEMA::SQ TO fc_read;
GO
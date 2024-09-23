# Use the official SQL Server image from Microsoft
FROM mcr.microsoft.com/mssql/server:2017-latest

# Set environment variables for SQL Server
ENV SA_PASSWORD=SQBoard!Passw0rd
ENV ACCEPT_EULA=Y

# Copy the initialization script into the container
COPY init.sql /usr/src/app/init.sql

CMD /bin/bash -c "/opt/mssql/bin/sqlservr & while ! /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -Q 'SELECT 1' > /dev/null 2>&1; do echo 'Waiting for SQL Server to start...'; sleep 5; done && /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P $SA_PASSWORD -i /usr/src/app/init.sql && tail -f /dev/null"

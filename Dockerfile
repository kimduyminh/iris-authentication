# Start from the official PostgreSQL image
FROM postgres:latest

# Copy the initialization SQL file into the container
COPY init.sql /docker-entrypoint-initdb.d/

# Set the proper permissions for the initialization script
RUN chmod 644 /docker-entrypoint-initdb.d/init.sql

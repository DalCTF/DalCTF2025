FROM postgres:15

# Copy the initialization script
COPY init.sql /docker-entrypoint-initdb.d/init.sql

# Set environment variables
ENV POSTGRES_DB=movie_reviews
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres 
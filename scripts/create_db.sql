\set user :user
\set pass :pass

DROP DATABASE IF EXISTS magazine_db;
CREATE DATABASE magazine_db;
CREATE USER :user; 
ALTER USER :user WITH PASSWORD :'pass';
GRANT ALL PRIVILEGES ON DATABASE magazine_db TO :user;
ALTER DATABASE "magazine_db" SET DATESTYLE TO "European";
\c magazine_db
CREATE EXTENSION IF NOT EXISTS vector;

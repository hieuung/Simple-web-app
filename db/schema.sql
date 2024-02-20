CREATE DATABASE bookstore;

CREATE SCHEMA webapp;

CREATE TABLE webapp.app_users (
  user_id SERIAL PRIMARY KEY,
  user_name VARCHAR(45) NULL,
  user_email VARCHAR(45) NULL,
  user_password VARCHAR(255) NULL,
  created_time BIGINT NOT NULL,
  latest_signed_in_time BIGINT NULL,
  updated_time BIGINT NOT NULL 
);

CREATE DATABASE datalake;

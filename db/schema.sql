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

-- CREATE OR REPLACE PROCEDURE sp_createUser(
--     p_name VARCHAR(20),
--     p_email VARCHAR(20),
--     p_password VARCHAR(255),
-- 	p_created_time BIGINT,
-- 	p_updated_time BIGINT
-- )
-- LANGUAGE plpgsql
-- AS
-- $$
-- BEGIN
--     IF EXISTS (SELECT 1 FROM webapp.app_users WHERE user_name = p_name AND user_email = p_email) THEN
--         RAISE NOTICE 'User Exists !!';
--     ELSE
--         INSERT INTO webapp.app_users (user_name, user_email, user_password, created_time, updated_time)
--         VALUES (p_name, p_email, p_password, p_created_time, p_updated_time);
--     END IF;
-- END;
-- $$
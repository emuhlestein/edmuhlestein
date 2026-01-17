-- Optional: Remove the table if you want to start fresh
-- DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS users (
    -- Auto-incrementing primary key
    user_id SERIAL PRIMARY KEY,
    
    -- Text fields with constraints
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    
    -- Fixed-length or variable-length text
    password_hash TEXT NOT NULL,
    
    -- Date and Time with a default value
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    
    -- Boolean flags
    is_active BOOLEAN DEFAULT TRUE
);

ALTER TABLE users
ADD COLUMN role VARCHAR(20) NOT NULL DEFAULT 'user';
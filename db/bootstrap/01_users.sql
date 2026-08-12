-- Thorne-EQ bootstrap 01: local dev database user (localhost only, not sensitive).
-- Run as root against the server (not a specific DB).
CREATE USER IF NOT EXISTS 'eq'@'localhost' IDENTIFIED BY 'eqemu';
CREATE USER IF NOT EXISTS 'eq'@'127.0.0.1' IDENTIFIED BY 'eqemu';
GRANT ALL PRIVILEGES ON quarm.* TO 'eq'@'localhost';
GRANT ALL PRIVILEGES ON quarm.* TO 'eq'@'127.0.0.1';
FLUSH PRIVILEGES;

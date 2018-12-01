CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  login VARCHAR(40) UNIQUE,
  name VARCHAR(60),
  passw VARCHAR(60),
  admin BOOL DEFAULT FALSE
);

CREATE TABLE connections (
  user_id INT,
  connected INT,
  FOREIGN KEY (user_id) REFERENCES users (user_id),
  FOREIGN KEY (connected) REFERENCES users (user_id)
);

CREATE INDEX index1
ON connections (user_id, connected);

CREATE INDEX index2
ON connections (connected, user_id);

INSERT INTO users (login, name, passw, admin)
    VALUES ('admin', 'John Smith', 'secret', TRUE );

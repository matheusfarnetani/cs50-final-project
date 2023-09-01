CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    hash TEXT NOT NULL,
    user_type TEXT CHECK(user_type IN ('student', 'collaborator', 'visitor'))
);
CREATE UNIQUE INDEX username ON users (username);
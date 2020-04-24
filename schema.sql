CREATE TABLE IF NOT EXISTS traits(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    source TEXT
);

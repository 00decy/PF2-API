CREATE TABLE IF NOT EXISTS traits(
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    description TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS feats(
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    action TEXT,
    level INTEGER,
    prerequisites TEXT,
    archetype TEXT,
    frequencey TEXT,
    requirements TEXT,
    trigger TEXT,
    description TEXT,
    source TEXT
);

CREATE TABLE IF NOT EXISTS feat_traits(
    trait_id INTEGER REFERENCES traits(id),
    feat_id INTEGER REFERENCES feats(id),
    trait_value TEXT
);

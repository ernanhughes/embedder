DROP TABLE IF EXISTS setting;
CREATE TABLE setting (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	section TEXT NOT NULL,
	name TEXT NOT NULL,
	value TEXT NOT NULL,
	description TEXT,
	seq INTEGER,
	username TEXT,
	created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS setting_history;
CREATE TABLE setting_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_id INTEGER,
	section TEXT NOT NULL,
	name TEXT NOT NULL,
	value TEXT NOT NULL,
	description TEXT,
	seq INTEGER,
	username TEXT,
	created TEXT,
	updated TEXT
);

DROP TRIGGER IF EXISTS setting_trigger;
CREATE TRIGGER setting_trigger
   AFTER UPDATE ON setting
BEGIN
	INSERT INTO setting_history (
			setting_id,
			section,
			name,
			value,
			description,
			seq,
			username,
			created,
			updated
		)
	VALUES
		(
			new.id,
			new.section,
			new.name,
			new.value,
			new.description,
			new.seq,
			new.username,
			new.created,
			strftime('%Y-%m-%dT%H:%M:%f','now')
		);
END;

DROP TABLE IF EXISTS attribute;
CREATE TABLE attribute (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	objectId INTEGER NOT NULL,
	objectType TEXT NOT NULL,
	name TEXT NOT NULL,
	value TEXT NOT NULL,
	description TEXT,
	seq INTEGER,
	username TEXT,
	created TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS attribute_history;
CREATE TABLE attribute_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    attribute_id INTEGER,
	section TEXT NOT NULL,
	name TEXT NOT NULL,
	value TEXT NOT NULL,
	description TEXT,
	seq INTEGER,
	username TEXT,
	created TEXT,
	updated TEXT
);

DROP TRIGGER IF EXISTS attribute_trigger;
CREATE TRIGGER attribute_trigger
   AFTER UPDATE ON attribute
BEGIN
	INSERT INTO attribute_history (
			attribute_id,
			section,
			name,
			value,
			description,
			seq,
			username,
			created,
			updated
		)
	VALUES
		(
			new.id,
			new.section,
			new.name,
			new.value,
			new.description,
			new.seq,
			new.username,
			new.created,
			strftime('%Y-%m-%dT%H:%M:%f','now')
		);
END;

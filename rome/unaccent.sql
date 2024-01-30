-- unaccent.sql
CREATE VIRTUAL TABLE unaccented USING fts5(tokenize=unicode61 "remove_diacritics=1");

CREATE TRIGGER unaccented_ai AFTER INSERT ON your_table
BEGIN
    INSERT INTO unaccented (rowid, content)
    SELECT rowid, your_text_column FROM your_table WHERE rowid = NEW.rowid;
END;

CREATE TRIGGER unaccented_ad AFTER DELETE ON your_table
BEGIN
    INSERT INTO unaccented (rowid, content, content='delete')
    SELECT rowid, your_text_column FROM your_table WHERE rowid = OLD.rowid;
END;

CREATE TRIGGER unaccented_au AFTER UPDATE ON your_table
BEGIN
    INSERT INTO unaccented (rowid, content, content='delete')
    SELECT rowid, your_text_column FROM your_table WHERE rowid = OLD.rowid;
    INSERT INTO unaccented (rowid, content)
    SELECT rowid, your_text_column FROM your_table WHERE rowid = NEW.rowid;
END;

CREATE TRIGGER unaccented_bd BEFORE DELETE ON your_table
BEGIN
    INSERT INTO unaccented (rowid, content, content='delete')
    SELECT rowid, your_text_column FROM your_table WHERE rowid = OLD.rowid;
END;

CREATE TRIGGER unaccented_bu BEFORE UPDATE ON your_table
BEGIN
    INSERT INTO unaccented (rowid, content, content='delete')
    SELECT rowid, your_text_column FROM your_table WHERE rowid = OLD.rowid;
    INSERT INTO unaccented (rowid, content)
    SELECT rowid, your_text_column FROM your_table WHERE rowid = NEW.rowid;
END;

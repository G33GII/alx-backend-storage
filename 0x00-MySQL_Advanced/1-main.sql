-- Inserting Values
INSERT INTO
    users (email, name, country)
VALUES
    ("bob@dylan.com", "Bob", "US");

INSERT INTO
    users (email, name, country)
VALUES
    ("sylvie@dylan.com", "Sylvie", "CO");

INSERT INTO
    users (email, name, country)
VALUES
    ("jean@dylan.com", "Jean", "FR");

INSERT INTO
    users (email, name)
VALUES
    ("john@dylan.com", "John");

SELECT
    *
FROM
    users;
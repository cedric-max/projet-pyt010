DROP TABLE IF EXISTS todos;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS todos (
    ToDo NVARCHAR(50) NOT NULL 
        CHECK (ToDo <> ''),
    UserId INTEGER NOT NULL,
    FOREIGN KEY (UserId) REFERENCES users(oid)
        ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE IF NOT EXISTS users
(
    UserName NVARCHAR(50) NOT NULL 
        CHECK (UserName <> ''),
    UserPassword NVARCHAR(255) NOT NULL 
        CHECK (UserPassword <> '')
);
CREATE INDEX [IDX_UserName] ON users([UserName]);

INSERT INTO users VALUES ('Tibow', 'pbkdf2:sha256:260000$RKKOdIKFmtoRa4Xt$2dfcdb963ce6b6ab1db2fe80c1765f87e9172f686efff2ac373c7785e013346f'),
('Cédric', 'pbkdf2:sha256:260000$RKKOdIKFmtoRa4Xt$2dfcdb963ce6b6ab1db2fe80c1765f87e9172f686efff2ac373c7785e013346f'),
('Thibaut', 'pbkdf2:sha256:260000$RKKOdIKFmtoRa4Xt$2dfcdb963ce6b6ab1db2fe80c1765f87e9172f686efff2ac373c7785e013346f');
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

INSERT INTO users(UserName, UserPassword) VALUES('Riri', 'pbkdf2:sha256:260000$vDjptUV5HLrL5XuS$bcf9d4fe32ce099d5fb7e449e95a2b8dacde2f539d9d9d7c3a5db8467360d210');
INSERT INTO users(UserName, UserPassword) VALUES('Roro', 'roro');
INSERT INTO users(UserName, UserPassword) VALUES('Titi', 'titi');
INSERT INTO users(UserName, UserPassword) VALUES('Toto', 'toto');
INSERT INTO users(UserName, UserPassword) VALUES('Arthur', 'arthur');

INSERT INTO todos(ToDo, UserId) VALUES("Faire la vaisselle",4);
INSERT INTO todos(ToDo, UserId) VALUES("Appeler maman",4);
INSERT INTO todos(ToDo, UserId) VALUES("Libérer le Kraken",4);
INSERT INTO todos(ToDo, UserId) VALUES("Faire la vaisselle",4);
INSERT INTO todos(ToDo, UserId) VALUES("Fendre du bois",2);
INSERT INTO todos(ToDo, UserId) VALUES("Prendre Fany",2);
INSERT INTO todos(ToDo, UserId) VALUES("Faire le ménage",2);
INSERT INTO todos(ToDo, UserId) VALUES("Retrouver Dédé au PMU",2);
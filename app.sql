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
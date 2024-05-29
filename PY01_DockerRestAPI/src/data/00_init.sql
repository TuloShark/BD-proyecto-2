CREATE DATABASE surveys;

\c surveys;

CREATE TABLE TipoUsuario (
    id SERIAL PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

CREATE TABLE GeneralUser (
    id SERIAL PRIMARY KEY,
    username VARCHAR(256) NOT NULL,
    password VARCHAR(1024) NOT NULL,
    idTipo INTEGER REFERENCES TipoUsuario(id)
);

INSERT INTO TipoUsuario (name) VALUES
    ('Administrador'),
    ('Encuestador');

INSERT INTO GeneralUser (username, password, idTipo) VALUES 
    ('Esteban', '1234', 1),
    ('Manuel', '2710', 1),
    ('Maria', '2003', 2),
    ('Marco', '2021', 2);
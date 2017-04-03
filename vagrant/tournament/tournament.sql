-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS PLAYERS;
DROP TABLE IF EXISTS MATCHES;
DROP TABLE IF EXISTS players;
DROP TABLE IF EXISTS matches;

CREATE TABLE PLAYERS(
    ID serial PRIMARY KEY not null,
    NAME TEXT NOT NULL
);
CREATE TABLE MATCHES(
    ID serial REFERENCES PLAYERS(ID),
    PLAYED INT NOT NULL DEFAULT 0,
    WINS INT NOT NULL DEFAULT 0,
    LOSSES INT NOT NULL DEFAULT 0
);
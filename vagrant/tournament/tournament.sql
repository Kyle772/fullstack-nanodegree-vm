-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP TABLE IF EXISTS MATCHES;
DROP TABLE IF EXISTS PLAYERS;

CREATE TABLE PLAYERS(
    ID serial PRIMARY KEY NOT NULL,
    NAME TEXT NOT NULL
);
CREATE TABLE MATCHES(
    ID serial PRIMARY KEY NOT NULL,
    WINNER serial REFERENCES PLAYERS(ID),
    LOSER serial REFERENCES PLAYERS(ID)
);
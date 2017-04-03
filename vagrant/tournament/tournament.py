#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    conn = psycopg2.connect("dbname=tournament")
    cur = conn.cursor()
    print("\nOpening new connection")
    print("------------------------")
    return cur, conn

def close(conn, close=False, commit=False):
    if commit:
        conn.commit()
        print("Committing changes")
    if close:
        conn.close()
        print("Closing current connection")
    

def deleteMatches():
    """Remove all the match records from the database."""
    cur, conn = connect()
    print("Deleting matches")
    cur.execute("""DELETE FROM MATCHES;""")
    close(conn, commit=True, close=False)
    cur.execute("""SELECT * FROM MATCHES""")
    rows = cur.fetchall()
    print("Current Matches data:\n {}".format(rows))
    close(conn, commit=True, close=True)
    

def deletePlayers():
    """Remove all the player records from the database."""
    cur, conn = connect()
    print("Deleting players")
    cur.execute("""SELECT ID FROM PLAYERS;""")
    rows = cur.fetchall()
    for row in rows:
        print("Deleting id {} from Matches due to dependency".format(row[0]))
        cur.execute("""DELETE FROM MATCHES WHERE ID='{}'""".format(row[0]))
        close(conn, commit=True, close=False)
        cur.execute("""SELECT * FROM MATCHES""")
        rows = cur.fetchall()
        print("Current Matches data:\n {}".format(rows))
    cur.execute("""DELETE FROM PLAYERS;""")
    close(conn, commit=True, close=False)
    cur.execute("""SELECT * FROM PLAYERS""")
    rows = cur.fetchall()
    print("Current Players data:\n {}".format(rows))
    close(conn, commit=False, close=True)


def countPlayers():
    """Returns the number of players currently registered."""
    cur, conn = connect()
    print("Counting Players")
    
    cur.execute("""SELECT count(NAME) as count from PLAYERS;""")
    row = cur.fetchone()
    count = row[0]
    print("Row results: {}".format(row))
    
    print("Count is currently {}".format(count))
    if count == None:
        count = 0
    
    print("Player count: " + str(count))
    close(conn, commit=True, close=True)
    return count
    


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    cur, conn = connect()
    print("Registering Players with data({})".format(name))
    print("Adding player name to t:players")
    cur.execute("""INSERT INTO PLAYERS(NAME) VALUES(%s);""", (name,))
    print("Getting id for Matches")
    cur.execute("""SELECT ID from PLAYERS WHERE NAME=%s""", (name,))
    currentID = cur.fetchone()
    print("Adding ID {} to t:matches".format(currentID[0]))
    cur.execute("""INSERT INTO MATCHES(ID) VALUES(%s)""", (currentID[0],))
    print("Added player {} to both tables".format(name))
    cur.execute("""SELECT NAME from PLAYERS;""")
    name = cur.fetchall()
    print("Current table data:\n {}".format(name))
    close(conn, close=True, commit=True)
    
    

def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    
    cur, conn = connect()
    print("Checking current standings")
    cur.execute("""SELECT * FROM MATCHES;""")
    rows = cur.fetchall()
    print("Current Matches data:\n {}".format(rows))
    
    cur.execute("""SELECT * FROM PLAYERS;""")
    rows = cur.fetchall()
    print("Current Players data:\n {}\n".format(rows))
    
    cur.execute("""SELECT PLAYERS.ID,
                          PLAYERS.NAME,
                          coalesce(sum(MATCHES.WINS), 0) as wins,
                          coalesce(sum(MATCHES.PLAYED), 0) as played
                   from PLAYERS
                   left join MATCHES on PLAYERS.ID = MATCHES.ID
                   group by PLAYERS.ID
                   order by wins desc;""")
    rows = cur.fetchall()
    print("ID, Name, Sum Wins, Sum played: \n {}\n".format(rows))
    close(conn, close=True, commit=False)
    return rows



def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    cur, conn = connect()
    print("Adding results of game data(Winner: {}, Loser:{})".format(winner, loser))
    cur.execute("""INSERT INTO MATCHES(ID, PLAYED, WINS) VALUES(%s, 1, 1);""", (winner,))
    close(conn, commit=True, close=False)
    cur.execute("""INSERT INTO MATCHES(ID, PLAYED, LOSSES) VALUES(%s, 1, 1);""", (loser,))
    close(conn, commit=True, close=False)
    cur.execute("""SELECT * FROM MATCHES WHERE ID=%s and ID=%s;""", (winner, loser))
    rows = cur.fetchall()
    print("Changed entries:\n %s", (rows))
    close(conn, commit=True, close=True)
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    print("Getting pairings")
    rows = playerStandings()
    toRet = []
    l = []
    for row in rows:
        if rows.index(row)%2 == 0:
            l.append(row[0])
            l.append(row[1])
        elif rows.index(row)%2 == 1:
            l.append(row[0])
            l.append(row[1])
            toRet.append(tuple(l))
            l = []
    
    return toRet


print("""
====================================\n
New Execution\n
====================================""")

import sqlite3

database = "user_cookie.db"
connection = sqlite3.connect(database)
c = connection.cursor()

def search_user_by_qq(sender: int):
    c.execute("SELECT * from user_cookie")
    for row in c:
        if row[2] == sender:
            return row
        else:
            pass
    return False

def search_user_by_role(game_role_id: str):
    c.execute("SELECT * from user_cookie")
    for row in c:
        if row[1] == int(game_role_id):
            return row
        else:
            pass
    return False


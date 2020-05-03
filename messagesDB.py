import sqlite3
from sqlite3 import Error
from message import message


class messagesDB(object):
    """description of class"""

    def __init__(self):
        self.__dbName = "messages.db"
        con = self.create_connection()
        if con is not None:

            messages_tbl = 'CREATE TABLE IF NOT EXISTS messages (message_id text PRIMARY KEY,session_id text NOT NULL,' \
                           'application_id integer NOT NULL,content text NOT NULL); '
            participants_tbl = 'CREATE TABLE IF NOT EXISTS participants ( participant_id INTEGER PRIMARY KEY ' \
                               'AUTOINCREMENT,name text); '
            messages_participants_tbl = 'CREATE TABLE IF NOT EXISTS participants_of_messages (participant_id INTEGER,' \
                                        'message_id text,PRIMARY KEY (participant_id, message_id),' \
                                        'FOREIGN KEY (participant_id) REFERENCES participants (participant_id) ' \
                                        'ON DELETE CASCADE ,' \
                                        'FOREIGN KEY (message_id) REFERENCES messages (' \
                                        'message_id) ON DELETE CASCADE); '
            self.create_table(con, messages_tbl)
            self.create_table(con, participants_tbl)
            self.create_table(con, messages_participants_tbl)
        else:
            print("Error! cannot create the database connection.")

    def create_connection(self):
        con = None
        try:
            con = sqlite3.connect(self.__dbName)
            return con
        except Error as e:
            print(e)

    def create_table(self, con, create_tbl):
        try:
            c = con.cursor()
            c.execute(create_tbl)
        except Error as e:
            print(e)

    def create_message(self, message_id, session_id, application_id, participants, content):
        con = sqlite3.connect(self.__dbName)
        c = con.cursor()
        c.execute(''' INSERT INTO messages VALUES(?,?,?,?) ''', (message_id, session_id, application_id, content))
        con.commit()
        message_row_id = c.lastrowid
        for p in participants:
            c.execute(''' INSERT INTO participants (name) VALUES(?) ''', [p])
            con.commit()
            c.execute('''SELECT participant_id FROM participants WHERE name=?''', [p])
            id = c.fetchone()
            c.execute("INSERT INTO participants_of_messages VALUES(?,?)", [id[0], message_id])
            con.commit()
        return message_row_id

    def get_messages(self, key, id):
        con = sqlite3.connect(self.__dbName)
        all_messages_cursor = con.cursor()
        all_participants_cursor = con.cursor()
        all_messages_cursor.execute(('SELECT DISTINCT\n'
                                     '           m.application_id as application_id,\n'
                                     '           m.session_id as session_id,\n'
                                     '           m.message_id as message_id,\n'
                                     '           m.content as content,\n'
                                     '           p.name as participants\n'
                                     '           FROM messages m join participants_of_messages pm \n'
                                     '           on m.message_id=pm.message_id \n'
                                     '           join participants p \n'
                                     '           on pm.participant_id=p.participant_id\n'
                                     '           WHERE m.') + key + """=? GROUP BY m.message_id""", [id])
        all_messages_for_key = all_messages_cursor.fetchall()
        response = []
        for item in all_messages_for_key:
            message_id = item[2]
            participants = []
            all_participants_cursor.execute("""SELECT 
               p.name as participants
               FROM messages m join participants_of_messages pm 
               on m.message_id=pm.message_id 
               join participants p 
               on pm.participant_id=p.participant_id
               WHERE m.""" + key + """=? AND pm.message_id=?
               GROUP BY p.name""", (id, message_id,))
            get_participants = all_participants_cursor.fetchone()
            while get_participants:
                participants.append(get_participants[0])
                get_participants = all_participants_cursor.fetchone()
            response.append(message(item[0], item[1], item[2], item[3], participants).serialize())
        con.commit()
        con.close()
        return response

    def delete_messages(self, key, id):
        con = sqlite3.connect(self.__dbName)
        all_message_cursor = con.cursor()
        c = con.cursor()
        all_message_cursor.execute(('SELECT DISTINCT\n'
                                     '           m.*,pm.*,p.*\n'
                                     '           FROM messages m join participants_of_messages pm \n'
                                     '           on m.message_id=pm.message_id \n'
                                     '           join participants p \n'
                                     '           on pm.participant_id=p.participant_id\n'
                                     '           WHERE m.') + key + """=? GROUP BY m.message_id""", [id])

        res = all_message_cursor.fetchone()
        if res is None:
            con.close()
            return  False
        while res:
            c.execute("DELETE FROM participants WHERE participant_id=?", (res[6],))
            res = all_message_cursor.fetchone()
        all_message_cursor.execute("DELETE FROM messages WHERE " + key + "=?", [id])
        con.commit()
        con.close()
        return True

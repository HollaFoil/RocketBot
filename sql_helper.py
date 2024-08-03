from configparser import ConfigParser
import psycopg2

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    # get section, default to postgresql
    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))

    return config

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

class SQLConnection:
    connection = None
    def __init__(self):
        config = load_config()
        self.connection = connect(config)

    def commit(self):
        self.connection.commit()

    def get_user_team_id(self, user_id):
        statement = """SELECT team_id FROM user_in_team 
                      WHERE user_in_team.user_id = %s;"""
        team_id = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (user_id,))
            team_id = cursor.fetchone()
        return team_id
    
    def get_team_name(self, team_id):
        if team_id == None:
            return None
        
        statement = """SELECT name FROM teams
                       WHERE teams.team_id = %s;"""
        team_name = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (team_id,))
            team_name = cursor.fetchone()[0]
        return team_name
    
    def get_team_owner(self, team_id):
        if team_id == None:
            return None
        
        statement = """SELECT owner_id FROM teams
                       WHERE teams.team_id = %s;"""
        owner_id = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (team_id,))
            owner_id = cursor.fetchone()[0]
        return owner_id
    
    def get_team_members(self, team_id):
        if team_id == None:
            return None
        
        statement = """SELECT user_id FROM user_in_team
                       WHERE user_in_team.team_id = %s;"""
        team_members = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (team_id,))
            team_members = cursor.fetchall()
        return team_members
    
    def get_team_invitations(self, team_id):
        statement = """SELECT * FROM invitations 
                       WHERE %s = invitations.team_id"""
        
        result = []
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (team_id, ))
            result = cursor.fetchall()
        return result

    def create_team(self, team_name, owner_id):
        statement = """INSERT INTO teams(owner_id, name) 
                       VALUES(%s, %s) RETURNING team_id;"""
        team_id = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (owner_id, team_name))
            team_id = cursor.fetchone()
        return team_id
    
    def add_player_to_team(self, user_id, team_id):
        statement = """INSERT INTO user_in_team(user_id, team_id) 
                       VALUES(%s, %s);"""
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (user_id, team_id))

    def add_player_invitation(self, user_id, team_id, invited_by_user_id):
        statement = """INSERT INTO invitations(user_id, team_id, invited_by) 
                       VALUES(%s, %s, %s);"""
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(statement, (user_id, team_id, invited_by_user_id))
        except:
            print("User was already invited")

    def check_player_invited(self, user_id, team_id):
        statement = """SELECT * FROM invitations 
                       WHERE %s = invitations.user_id AND %s = invitations.team_id"""
        
        result = None
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (user_id, team_id))
            result = cursor.fetchone()
        
        return True if result != None else False
    
    def check_player_has_team(self, user_id):
        result = self.get_user_team_id(user_id)
        return True if result != None else False
    
    def check_player_in_team(self, user_id, team_id):
        result = self.get_user_team_id(user_id)
        return True if result == team_id else False
    
    def count_team_players(self, team_id):
        result = self.get_team_members(team_id)
        if result == None:
            return 0
        return len(result)
    
    def count_team_invitations(self, team_id):
        result = self.get_team_invitations(team_id)
        return len(result)
    
    def get_total_team_size(self, team_id):
        return self.count_team_invitations(team_id) + self.count_team_players(team_id)
    
    def delete_player_from_team(self, team_id, user_id):
        if team_id == None:
            return
        
        statement = """DELETE FROM user_in_team
                       WHERE user_in_team.user_id = %s;"""
        
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (user_id,))

    def change_team_owner(self, team_id):
        if team_id == None:
            return
        
        statement = """UPDATE teams
                       SET teams.owner_id = %s
                       WHERE teams.team_id = %s;"""
        
        new_owner = self.get_team_members(team_id)[0][0]

        with self.connection.cursor() as cursor:
            cursor.execute(statement, (new_owner, team_id))

    def delete_team(self, team_id):
        if team_id == None:
            return
        
        statement = """DELETE FROM teams
                       WHERE teams.team_id = %s;"""
        
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (team_id, ))

    def delete_invites(self, user_id):
        if user_id == None:
            return
        
        statement = """DELETE FROM user_in_team
                       WHERE user_in_team.user_id = %s;"""
        
        with self.connection.cursor() as cursor:
            cursor.execute(statement, (user_id, ))
        
    
        
        




from database.DB_connect import DBConnect
from model.team import Team


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT distinct(t.year)
                    FROM teams t 
                    WHERE year > 1980"""

        cursor.execute(query)

        for row in cursor:
            result.append(row["year"])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getTeamsOfYear(year):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)

        query = """SELECT *
                    FROM teams t
                    WHERE t.year = %s"""

        cursor.execute(query, (year,))

        for row in cursor:
            result.append(Team(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getSalariesTeam(year, idMapTeams): #prendere salari delle squadre, bisogna vedere anche in quale squadra il giocatore ha giocato (piò aver giocato in più squadre)
        conn = DBConnect.get_connection()

        cursor = conn.cursor(dictionary=True)

        query = """SELECT t.ID, t.teamCode, sum(s.salary) as totSalary
                    FROM salaries s, teams t, appearances a 
                    WHERE s.`year` = t.`year` AND s.`year` = a.`year` AND a.`year` = %s
                    AND t.ID = a.teamID AND s.playerID = a.playerID
                    GROUP BY t.ID, t.teamCode"""

        cursor.execute(query, (year,))

        mapSalary = {}

        for row in cursor:
           mapSalary[idMapTeams[row["ID"]]] = row["totSalary"] #chiave oggetto di tipo team, valore salario

        cursor.close()
        conn.close()
        return mapSalary

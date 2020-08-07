import sqlite3

con = sqlite3.connect("flowers2019.db")

con.execute("DROP TRIGGER updater")
#con.execute("CREATE TRIGGER updater AFTER UPDATE ON flowers WHEN New.comname NOT IN (SELECT comname FROM flowers) BEGIN UPDATE sightings SET name = New.comname WHERE name = Old.comname; END;")

con.close()

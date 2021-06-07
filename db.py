import sqlite3


class Records:

    def __init__(self):
        self.conn = sqlite3.connect('records.db')
        self.conn.row_factory = sqlite3.Row
        self.c = self.conn.cursor()
        self.id = 0

    def createTable(self):
        query = '''CREATE TABLE  IF NOT EXISTS records
                    (id integer NOT NULL PRIMARY KEY AUTOINCREMENT,name varchar(255),
                    phone varchar(20), projects TEXT, skills TEXT, linkedin varchar(255),
                    designation varchar(255), degree varchar(255), certifications TEXT, 
                    accomplishments TEXT,total_exp varchar(20),grade varchar(10), email varchar(255) );'''
        self.c.execute(query)
        print("Table created Successfully.")

    def get_records(self):
        query = '''SELECT * from records;'''
        self.c.execute(query)
        records = []
        for cv_data in self.c.fetchall():
            records.append(cv_data)
        return records

    def insert_record(self, name, phone, projects, skills, linkedin, designation, degree, certifications, accomplishments, total_exp, grade, email):
        print(name, phone, projects, skills, linkedin, designation, degree, certifications, accomplishments, total_exp, grade, email)
        query = ''' INSERT INTO records(name, phone, projects, skills, linkedin, designation,
                    degree,certifications, accomplishments, total_exp, grade, email)
                    values(?,?,?,?,?,?,?,?,?,?,?,?);'''
        self.c.execute(query, (name, phone, projects, skills, linkedin, designation, degree, certifications, accomplishments, total_exp, grade, email))
        self.conn.commit()


if __name__ == "__main__":
    record = Records()
    record.createTable()
    for data in record.get_records():
        print(dict(data))
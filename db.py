import sqlite3


class db():

    def get_connection(self):
        conn = sqlite3.connect('test_results')
        return conn

    def get_rows_for_build_number(self, build_number):
        conn = self.get_connection()
        cur = conn.cursor()
        cur.execute('SELECT build_number FROM results where build_number = {}' .format(build_number))
        rows = cur.fetchall()
        conn.close()
        return rows

    def insert_results(self, result):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('insert into results values (?,?,?,?,?,?,?)', result)
        conn.commit()
        conn.close()

    def read_results_for_build_number(self, build_number):
         conn = self.get_connection()
         c = conn.cursor()
         c.execute('SELECT  id, name, result, message  FROM results WHERE build_number = {} group by id order by id asc' .format(build_number))
         #'Select distinct * from results where build_number, Select * from results where id in (select distinct id from results) and build_number '
         #'SELECT * FROM `statstable` WHERE `ipaddy` IN (SELECT DISTINCT `ipaddy` FROM `statstable`)'
         #'SELECT * FROM table WHERE email in(SELECT email FROM table GROUP BY email HAVING COUNT(email)=1)'
         rows = c.fetchall()
         return rows

    def read_results_for_date(self, date):
         conn = self.get_connection()
         c = conn.cursor()
         datelike = str(date+'%')
         c.execute('SELECT  id, name, result, message  FROM results WHERE start_time like ? group by id order by id asc',('{}%' .format(datelike),))
         rows = c.fetchall()
         return rows

    def get_build_number_for_date(self, date):
         conn = self.get_connection()
         c = conn.cursor()
         datelike = str(date+'%')
         c.execute('SELECT  build_number FROM results WHERE start_time like ? limit 1',('{}%' .format(datelike),))
         rows = c.fetchall()
         buildnumber = [x[0] for x in rows]
         if len(buildnumber)>0:
             return buildnumber[0]
         else:
            return " Tests were not run on the selected date, please select another date from 20th July 2018"


    def get_passed_tests_count(self, build_number):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(
            'select  count (*) from results where result = "success" and build_number = {} group by id order by id asc'.format(
                build_number))
        count = c.fetchall()
        return len(count)

    def get_passed_tests_count_for_date(self, date):
        conn = self.get_connection()
        c = conn.cursor()
        datelike = str(date + '%')
        c.execute('select  count (*) from results where result = "success" and start_time like ? group by id order by id asc',
                  ('{}%'.format(datelike),))
        count = c.fetchall()
        return len(count)


    def get_all_build_numbers(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute('Select distinct build_number from results')
        rows = c.fetchall()
        print(rows)
        return rows


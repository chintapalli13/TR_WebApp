from flask import Flask, render_template, request
import db
import pandas as pd
import datetime
import getresultsfromci

app = Flask(__name__)




def read_results(buildnumber):
    return db.db().read_results_for_build_number(buildnumber)

@app.route("/home", methods =['GET'])
def home():
    return  get_default_view()


@app.route("/fetch_new_results", methods =['GET'])
def get_new_results_from_CI():
    re = getresultsfromci.getresultsfromci()
    message = re.save_results_in_db()
    return  render_template('index.html', message= message)


@app.route('/select_date', methods =['GET', 'POST'])
def select_date():
    date = request.form['test_date']
    res = db.db().read_results_for_date(date)
    buildnum = db.db().get_build_number_for_date(date)
    totaltests = int(len(res))
    passcount = int(db.db().get_passed_tests_count_for_date(date))
    failedcount = totaltests - passcount
    return get_view(res, buildnum, passcount, failedcount, date)


def get_view(res, buildnum, passcount, failedcount, date):
    labels = ['Jira Id', 'Test case name', 'Result', 'Failure message']  # , 'Start time', 'Stop time']
    pd.set_option('display.max_colwidth', -1)
    rt = pd.DataFrame.from_records(res, columns=labels)
    return render_template('index.html', tables=[rt.to_html(border=True)], build=buildnum, total_tests=(len(res)),
                           passed=passcount, failed=failedcount, dt= date)

def get_default_view():
    date = datetime.datetime.today().strftime('%Y-%m-%d')
    buildnum = db.db().get_build_number_for_date(date)
    res = db.db().read_results_for_date(date)
    totaltests = int(len(res))
    passcount = int(db.db().get_passed_tests_count(buildnum))
    failedcount = totaltests - passcount
    labels = ['Jira Id', 'Test case name', 'Result', 'Failure message']  # , 'Start time', 'Stop time']
    pd.set_option('display.max_colwidth', -1)
    rt = pd.DataFrame.from_records(res, columns=labels)
    return render_template('index.html', tables=[rt.to_html(border=True)], build=buildnum, total_tests=(len(res)),
                           passed=passcount, failed=failedcount, dt=date)




if __name__ == "__main__":
    app.run(debug=True)

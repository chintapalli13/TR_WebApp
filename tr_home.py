from flask import Flask, render_template
import db
import pandas as pd
app = Flask(__name__)


def read_results(buildnumber):
    return db.db().read_results_for_build_number(buildnumber)



@app.route("/")
@app.route("/home")
def home():
    buildnum = 3380
    res = read_results(buildnum)
    labels = ['Id', 'Name', 'Result', 'Message']#, 'Start time', 'Stop time']
    rt = pd.DataFrame.from_records(res, columns=labels)
    print (rt)
    return render_template('index.html', tables = [rt.to_html()], build=buildnum)
        # "Automated Test Result Dashboard"



if __name__ == "__main__":
    app.run(debug=True)

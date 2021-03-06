import getbuild
import getTestData
import db



class getresultsfromci():

    def get_processed_results(self):
        build = getbuild.build().get_last_build()
        print(build['build_number'])
        results = getTestData.test_results().get_test_results(build['build_number'])
        return  {'build_data':build, 'all_results':results}


    def get_test_object(self):
        resdata = self.get_processed_results()
        results = resdata['all_results']
        build = resdata['build_data']
        all_results = []
        for result in results:
            # t = test(build['build_number'], result['id'], result['name'], result['result'], result['message'],
            #          build['start_time'], build['stop_time'])
            all_results.append([build['build_number'], result['id'], result['name'], result['result'], result['message'],
                     build['start_time'], build['stop_time']])
            # all_results.append([t.build_number, t.id, t.name, t.result, t.message, t.start_date, t.stop_date])
        return all_results


    def save_results_in_db(self):
        resultobj = self.get_test_object()
        d = db.db()
        rows = d.get_rows_for_build_number(resultobj[0][0])
        if len(rows) < 1:
            for obj in resultobj:
                d.insert_results(obj)
            return "Results successfully fetched for the last test run"
        else:
            print("Results already exists in db for the build number")
            return "Results already exists for the last test run, try again after 20.30 Hrs est"


    def read_results(self, buildnumber):
        return db.db().read_results_for_build_number(buildnumber)


    # def __init__(self, build_number, id, name, result, message, start_date, stop_date):
    #     self.build_number = build_number
    #     self.id = id
    #     self.name = name
    #     self.result = result
    #     self.message = message
    #     self.start_date = start_date
    #     self.stop_date = stop_date






# def main():
#       save_results_in_db()
     #  resultsTable = read_results(3328)
     #  ids = []
     #  for result in resultsTable:
     #      ids.append(result[0])
     #      print(list(set(ids)))

     #(3328,), (3336,), (3342,), (3344,), (3358,), (3366,), (3373,)
     #print(sorted(db.db().get_all_build_numbers()))

# if __name__ == "__main__":
#     main()

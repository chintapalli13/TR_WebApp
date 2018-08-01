import request
import  re


class test_results():

    def get_test_meta_data(self, build_num,):
        if not build_num:
            return 0
        metadata_url = 'https://circleci.com/api/v1.1/project/github/aldo-dev/mfind/' + str(build_num) + '/tests?circle-token=03dc9a9f0a2cfe00c80f27aaf0405e810680702d'
        print (metadata_url)
        r_json = request.get_request().get_json_from_request(metadata_url)
        return r_json

    def get_test_jira_id(self, testcase_name):
        tcname = testcase_name
        tcsplit = tcname.split("_")
        if len(tcsplit) > 2:
            jiraid_b = tcsplit.pop()
            jiraid_a = tcsplit.pop(-1)
            jira_id = jiraid_a + "-" + jiraid_b
            return jira_id

    def process_test_class_names(self, class_names):
        unique_class_name_list_set = list(set(class_names))
        regex_text = re.compile(".*mFindUITests")
        filtered_class_names = list(filter(regex_text.match, unique_class_name_list_set))
        return filtered_class_names

    def get_test_results(self, build_num):
        test_meta_data = self.get_test_meta_data(build_num)
        test_cases = []
        if test_meta_data != 404:
            tests = test_meta_data['tests']
            all_test_classes = map(lambda test: test['classname'], tests)
            unique_test_classes = self.process_test_class_names(all_test_classes)
            allcases = [(build_num, self.get_test_jira_id(t['name']), t['name'], t['result'], t['message'],)
                        for tclass in unique_test_classes
                        for t in tests
                        if tclass == t['classname'] and
                        self.get_test_jira_id(t['name']) != None]

            # print(allcases)

            for testclass in unique_test_classes:
                for test in tests:
                    if testclass == test['classname']:
                        jira_id = self.get_test_jira_id(test['name'])
                        if not jira_id == None:
                            test_cases.append(
                                {'id':jira_id, 'name':test['name'], 'result':test['result'], 'message':test['message']})
        else:
            print ("Test meta data not received")
                        # print (get_test_results_ci['name'], get_test_results_ci['result'], get_test_results_ci['message'])
        return test_cases

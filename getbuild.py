import request


class build():

    def get_last_build(self):
        build_url = 'https://circleci.com/api/v1.1/recent-builds?circle-token=03dc9a9f0a2cfe00c80f27aaf0405e810680702d&limit=100'
        req = request.get_request()
        build_start_times = []
        response_json = req.get_json_from_request(build_url)
        for branch in response_json:
            if branch['branch'] == 'mfind-aws' and branch['build_parameters']['CIRCLE_JOB'] == 'run-ui-tests':
                build_start_times.append(branch['start_time'])
        for build in response_json:
            if build['start_time'] == sorted(build_start_times, reverse=True)[0]:
                build_number = (build['build_num'])
                build_start_time = build['start_time']
                build_stop_time = build['stop_time']
                return {'build_number':build_number, 'start_time':build_start_time, 'stop_time':build_stop_time}

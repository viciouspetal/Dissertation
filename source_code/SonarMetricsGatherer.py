class SonarMetricsGatherer:
    username = None
    password = None

    def __init__(self, username, password):
        self.username = username
        self.password = password

    server_url = 'http://10.60.142.206:9000'
    component_api_url = '/api/measures/component?componentKey='
    metrics_to_pull = '&metricKeys=' # actual list of keys have been omitted for brevity

    def make_url(self, target_file, server_url=server_url, component_url=component_api_url, metrics=metrics_to_pull):
        return server_url + component_url + target_file + metrics

    def main(self, target_file, repo_name):
        url = self.make_url(target_file)
        resp = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
        metrics_map = {}
        if resp.status_code != 200:
            print('File that errored out: {0}'.format(target_file))
            # raise ApiError('Sonar server responded with {} code'.format(resp.status_code))
        else:

            resp_component = resp.json().get('component')
            formatted_file_path = self.format_target_file_path_for_display(target_file)

            metrics_map = self.filter_metrics(self.convert_metrics_to_map(resp_component))
            metrics_map['file_path'] = formatted_file_path

        return metrics_map

    def format_target_file_path_for_display(self, file_path):
        return file_path.replace('%3A', '/').replace('%2F', '/')

    def sonar_component_name_generator(self, component_key, file_name_from_jira):
        try:
            component, branch = component_key.rsplit(':', 1)
            module_name, path = file_name_from_jira.split('/', 1)
            test_url = ''
            if 'unified-ui' in component_key:
                test_url = component + ':' + branch + ':' + module_name + '/' + path
            else:
                test_url = component + ':' + module_name + ':' + branch + ':' + path
           
            return test_url.replace(':', '%3A').replace('/', '%2F')
        except ValueError:
            print('Couldn\'t generate name for component {0} filename {1}'.format(component_key, file_name_from_jira))
            return ''
        # %3A = :
        # %2F = /

    def search_for_project_by_name(self, project_name):
        search_url = 'http://10.60.142.206:9000/api/projects/index?search={0}%20develop'.format(project_name)
        resp = requests.get(search_url, auth=HTTPBasicAuth(self.username, self.password))

        if resp.json() is '[]':
            search_url = 'http://10.60.142.206:9000/api/projects/index?search={0}%20master'.format(project_name)
            resp = requests.get(search_url, auth=HTTPBasicAuth(self.username, self.password))
        return resp

    def get_project_key_by_project_name(self, project_name):
        project_data_from_server = self.search_for_project_by_name(project_name)
        converted_to_json = json.loads(project_data_from_server.text)
        if len(converted_to_json) > 0:
            return converted_to_json[0]['k']
        else:
            print('Couldn\'t get the Sonar project key for {0} '
            'given project data retrieved {1}'.format(project_name,
                                                                                                        project_data_from_server.text))
            return ''

    def save_to_csv(self, list_of_metric_dicts, header_printed, out_path='file_report.csv'):
        keys = self.get_headers()
        with open(out_path, 'a') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            if header_printed is False:
                dict_writer.writeheader()

            for file in list_of_metric_dicts:
                dict_writer.writerow(file)

    def get_headers(self):
        headers = []
        for item in SonarMetricsEnum:
            headers.append(item.value)
        return headers

    def basic_save_to_csv(self, map_to_csv):
        keys = map_to_csv.keys()
        with open('basic_file_report.csv', 'a') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerow(map_to_csv)

    def convert_metrics_to_map(self, comp_json):
        metrics_map = {}
        for measure in comp_json.get('measures'):
            metrics_map[measure.get('metric')] = measure.get('value')
        return metrics_map

    def filter_metrics(self, metrics_map):
        filtered_metrics = {}
        for metric in SonarMetricsEnum:
            if metric.value not in metrics_map:
                filtered_metrics[metric.value] = -1
            else:
                filtered_metrics[metric.value] = metrics_map[metric.value]
        return filtered_metrics
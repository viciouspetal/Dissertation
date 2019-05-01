class Gatherer:

    def __init__(self):
        self.header_printed = False

    def main(self, username, password, jira_keys, is_bug_file):
        for jira_key in jira_keys:
            jira_obj = JiraConnector(username, password)
            # get metrics from JIRA
            files, commit_details = jira_obj.main(jira_key)

            sonar_obj = SonarMetricsGatherer(username, password)
            output = []
            bb = Bitbucket(username, password)
            # get information about previous commits
            prev_commit_details = bb.get_prev_commit_details_per_filepath(commit_details)
            # encode author's fullname for identity protection
            prev_commit_details = AuthorDetailsTransformer().transform_names_into_codenames(prev_commit_details)

            for file in files.keys():
                repo_file_is_in = files[file]
                component_key = sonar_obj.get_project_key_by_project_name(repo_file_is_in)

                # check if component key was generated correctly
                if len(component_key) <= 0:
                    self.log_jira_error(jira_key)
                    continue

                # get component_name
                component_name = sonar_obj.sonar_component_name_generator(component_key, file)
               
                # check if component name was generated correctly
                if len(component_name) <= 0:
                    self.log_jira_error(jira_key)
                    continue

                sorted_metrics_dict = sonar_obj.main(component_name, repo_file_is_in)
               
                # check if metrics were generated correctly
                if len(sorted_metrics_dict) > 0:
                    sorted_metrics_dict['source_repo'] = repo_file_is_in
                    sorted_metrics_dict['is_bug'] = is_bug_file
                    sorted_metrics_dict['issue_key'] = jira_key
                    combined = sorted_metrics_dict.copy()
                    combined.update(prev_commit_details[file])
                    output.append(combined)

                    sonar_obj.save_to_csv(header_printed=self.header_printed, list_of_metric_dicts=output,
                                          out_path='results.csv')
                    self.header_printed = True  # ensure that header is only appended once to target CSV
                else:
                    self.log_jira_error(jira_key)

    def log_jira_error(self, jira_key):
        print('Error with processing JIRA: {0}'.format(jira_key))

    def load_jira_key_files(self, file_location):
        values = []
        with open(file_location) as f:
            for line in f:
                line = line.replace('\n', '')
                values.append(line)
        return values


if __name__ == '__main__':
    start_time = time.time()
    urllib3.disable_warnings()
    username = None
    password = None
    if len(sys.argv) > 2:
        username = sys.argv[1]
        password = sys.argv[2]
    try:
        obj = Gatherer()
        # get data from bug tickets
        jira_keys = obj.load_jira_key_files('src/resources/bug_issue_key_list.dat')
        obj.main(username, password, jira_keys, True)

        # get data from regular tickets
        jira_keys = obj.load_jira_key_files('src/resources/story_issue_key_list.dat')
        obj.main(username, password, jira_keys, False)
        print('Operation duration: {0}'.format(time.time() - start_time))
    except Exception as e:
        print('Operation completed with an error. Duration: {0}'.format(time.time() - start_time))
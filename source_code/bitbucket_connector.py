 class Bitbucket:
    bitbucket_url_sample = 'https://gssd-stash.isus.emc.com/rest/api/latest/projects/{0}/repos/{1}'\
    '/commits?followRenames=true&path={2}&until=refs%2Fheads%2Fdevelop&start=0&limit={3}'
    username = ''
    password = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def executor(self):
        resp = self.get_last_two_commits()
        if resp.status_code != 200:
            raise ApiError('Bitbucket server responded with {} code'.format(resp.status_code))

    def get_last_two_commits(self, project_key='CFG', project_name='oberon-asset-management',
                             project_file_path='', no_of_commits_to_pull=2):
        url = self.bitbucket_url_sample.format(project_key, project_name, project_file_path, no_of_commits_to_pull)
        resp = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
        return resp

    def get_prev_commit_details_per_filepath(self, jira_details_json):
        url = 'https://gssd-stash.isus.emc.com/rest/api/1.0/projects/{0}/repos/{1}/commits/{2}'
        complete_results = {}
        for file in jira_details_json:
            result_items = {}
            item = jira_details_json[file]
            target_url = url.format(item['repo_code'], item['target_repo'], item['commitId'])
            resp = requests.get(target_url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
            result = resp.json()
            author_name = result['author']['name']
            timestamp = result['authorTimestamp']
            parent_section = result['parents'][0]
            prev_author = parent_section['author']['name']
            prev_timestamp = parent_section['authorTimestamp']

            result_items['author'] = author_name
            result_items['timestamp'] = timestamp
            result_items['prev_author'] = prev_author
            result_items['prev_timestamp'] = prev_timestamp
            complete_results[file] = result_items
        return complete_results

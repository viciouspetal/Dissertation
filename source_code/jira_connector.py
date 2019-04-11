import re
import sys

import requests
from requests.auth import HTTPBasicAuth


class JiraConnector:
    server_url_base = 'https://cksvnprd01.corp.emc.com/jira'
    url = 'https://cksvnprd01.corp.emc.com/jira/rest/webResources/1.0/resources'

    username = ''
    password = ''

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def main(self, issue_key='ZZZ-1234'):
        issue_id = self.get_jira_id_from_jira_key(issue_key)

        resp = self.get_commit_details_for_a_jira_id(issue_id)
        return self.get_filenames_from_commits(resp)

    def is_valid_project(self, project_name):
        exclusions_pattern = '.*-ng-api$|.*-ui-components$|.*kaa.*|^titan-client$|^titan-gradle-plugin$|^workflow-libs$|^archive.*|^jenkins-config-tasks$|^configuration-user-journeys$|randummy|workflow-libs3|.*gulp_tasks.*'
        exclusions_re = re.compile(exclusions_pattern)

        if exclusions_re.match(project_name):
            return False
        else:
            return True

    def get_jira_details_url(self, key):
        base_url = self.server_url_base + '/rest/api/2/issue/{0}'
        return base_url.format(key)

    def get_jira_id_from_jira_details(self, jira_details):
        id_key = 'id'
        return jira_details.get(id_key)

    def get_jira_id_from_jira_key(self, jira_key):
        url = self.get_jira_details_url(jira_key)

        jira_details_resp = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
        if (jira_details_resp.status_code == 404):
            backup_url = 'https://cksvnprd01.corp.emc.com:4443/joanna/rest/api/2/issue/{0}'.format(jira_key)
            jira_details_resp = requests.get(backup_url, auth=HTTPBasicAuth(self.username, self.password), verify=False)
            print(backup_url)
            print(jira_details_resp.text)
        return self.get_jira_id_from_jira_details(jira_details_resp.json())


    def get_commit_details_for_a_jira_id(self, jira_id):
        resp = requests.get(self.get_commit_details_url(jira_id), auth=HTTPBasicAuth(self.username, self.password),
                            verify=False)
        return resp.json()

    def get_commit_details_url(self, id):
        url_base = self.server_url_base + '/rest/dev-status/1.0/issue/detail?issueId={0}&applicationType=stash&dataType=repository&_=1549641890823'
        return url_base.format(id)

    def get_repositories_from_json_response(self, json_details):
        repositories_section = json_details['detail'][0]['repositories']
        return repositories_section

    def get_repo_slug_from_repo_url(self, repo_url):
        slug_expr = re.compile('http.?://gssd-stash.isus.emc.com/projects/(\w+)\/.*')
        return slug_expr.match(repo_url).group(1)

    def get_commits_from_json_response(self, input_json):
        repositories_section = self.get_repositories_from_json_response(input_json)

        commits_in_repo = {}
        for repo in repositories_section:
            repo_name = repo['name']
            if self.is_valid_project(repo_name):
                repo_slug = self.get_repo_slug_from_repo_url(repo['url'])
                for commit in repo['commits']:
                    if commit['merge'] is False:

                        commit['repo_slug'] = repo_slug
                        if repo_name not in commits_in_repo.keys():
                            current_commits = [commit]
                            commits_in_repo[repo_name] = []
                            commits_in_repo[repo_name] = current_commits
                        else:
                            current_commits = commits_in_repo[repo_name]
                            current_commits.append(commit)
                            commits_in_repo[repo_name] = current_commits
        return commits_in_repo

    def get_filenames_from_commits(self, json):
        repo_to_commits_dict = self.get_commits_from_json_response(json)
        filenames = {}
        commit_details = {}
        java_exclusions = '.*Test.*.java|.*Interface.*\.java|.*NameToIndex\.java$|.*\.jar$|.*\.war$|.*.gradle$|.*Config.java'
        kotlin_exclusions = '.*Test.*.kt|.*Interface.*\.kt|.*Config.kt|.*Dto.*kt$|.*Enum.*kt$'
        javascript_exclusions = '.*\.?factory.js$|.*\.html$|.*\.e2e-spec.js$|.*\.stub.js$|.*\.po.js$|.*spec.js$|.*\.scss$' \
                                '|.*\.css$|.*\.svg$|.*\.ico$|.*\.npmrc$|.*\.conf.js$|.*gulpfile.js$|.*factories.js$|.*.config.js$' \
                                '|.*ColumnDefs.js$|.*ColumnDef.js$|.*Spec.js$|.*Decorator.js|\.eslintrc'
        other_exclusions = '\.gitignore$|.*\.md$|.*\.properties$|.*\.gitattributes$|.*\.sql|.*\.csv|.*\.xlsx$|.*\.json$' \
                           '|.*\.lock$|.*\.gz$|.*\.txt$|.*\.xlsm$|.*\.yaml$|.*\.yml$|.*Jenkinsfile.*|.*\.xml$|.*CreateService.*' \
                           '|.*ReadService.*|.*WriteService.*|.*DeleteService.*'
        java_re = re.compile(java_exclusions)
        kotlin_re = re.compile(kotlin_exclusions)
        javascript_re = re.compile(javascript_exclusions)
        other_re = re.compile(other_exclusions)
        for repo in repo_to_commits_dict.keys():
            for commit in repo_to_commits_dict[repo]:
                for file in commit['files']:
                    if java_re.match(file['path']) or kotlin_re.match(file['path']) or javascript_re.match(
                            file['path']) or other_re.match(file['path']):
                        pass
                    else:
                        filenames[file['path']] = repo
                        commit_id = commit['id']
                        repo_slug = commit['repo_slug']
                        partial = {}
                        partial['commitId'] = commit_id
                        partial['target_repo'] = repo
                        partial['repo_code'] = repo_slug
                        commit_details[file['path']] = partial
        return filenames, commit_details

    def get_repo_name(self, json):
        return self.get_repositories_from_json_response(json)[0]['name']


if __name__ == '__main__':
    password = None
    if len(sys.argv) > 1:
        password = sys.argv[1]
    obj = JiraConnector()
    obj.main('wojcij1', password)

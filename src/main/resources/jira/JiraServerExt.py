#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import string
import com.xhaus.jyson.JysonCodec as Json
from util import error
from xlrelease.HttpRequest import HttpRequest


class JiraServerExt:

    def __init__(self, jira_server, username, password, encoding='utf-8'):
        if jira_server is None:
            error('No server provided.')

        self.jira_server = jira_server
        self.username = username
        self.password = password
        self.encoding = encoding

    def queryIssues(self, query, options=None):

        if not query:
            error('No JQL query provided.')

        # Create POST body
        content = {
            'jql': query,
            'startAt': 0,
            'fields': ['summary', 'status', 'assignee']
        }
        # Do request
        request = self._createRequest()
        response = request.post('/rest/api/2/search', self._serialize(content), contentType='application/json')
        # Parse result
        if response.status == 200:
            issues = {}
            data = Json.loads(response.response)
            for item in data['issues']:
                issue = item['key']
                issues[issue] = {
                    'issue'   : issue,
                    'summary' : item['fields']['summary'],
                    'status'  : item['fields']['status']['name'],
                    'assignee': item['fields']['assignee']['displayName'],
                    'link'    : "{1}/browse/{0}".format(issue, self.jira_server['url'])
                }
            return issues
        else:
            error(u"Failed to execute search '{0}' in JIRA.".format(query), response)

    def checkQuery(self, query):
        if not query:
            error('No JQL query provided.')

        # Create POST body
        content = {
            'jql': query,
            'startAt': 0,
            'fields': ['summary', 'status']
        }

        # Do request
        request = self._createRequest()
        response = request.post('/rest/api/2/search', self._serialize(content), contentType='application/json')
        # Parse result
        if response.status == 200:
            data = Json.loads(response.response)

            issues = {}
            for item in data['issues']:
                issue = item['key']
                issues[issue] = (item['fields']['summary'], item['fields']['status']['name'])
            return issues

        else:
            error(u"Failed to execute search '{0}' in JIRA.".format(query), response)

    def _getUpdatedIssueData(self, summary, comment):
        updated_data = {}

        if comment:
            updated_data.update({
                "comment": [
                    {
                        "add": {
                            "body": comment
                        }
                    }
                ]
            })

        if summary:
            updated_data.update({
                "summary": [
                    {
                        "set": summary
                    }
                ]
            })

        return updated_data
    # End _getUpdatedIssueData

    def _updateIssue(self, issue_id, updated_data):

        # Create POST body
        request_data = {"update": updated_data}

        # Do request
        request = self._createRequest()
        response = request.put(self._issueUrl(issue_id), self._serialize(request_data), contentType='application/json')

        # Parse result
        if response.status != 204:
            error(u"Unable to update issue {0}. Please make sure the issue is not in a 'closed' state.".format(self._link(issue_id)), response)
    # End _updateIssue

    def _transitionIssue(self, issue_id, new_status):

        issue_url = self._issueUrl(issue_id)

        # Find possible transitions
        request = self._createRequest()
        response = request.get(issue_url + "/transitions?expand=transitions.fields", contentType='application/json')

        if response.status != 200:
            error(u"Unable to find transitions for issue {0}".format(self._link(issue_id)), response)

        transitions = Json.loads(response.response)['transitions']

        # Check  transition
        wanted_transaction = -1
        for transition in transitions:
            if transition['to']['name'].lower() == new_status.lower():
                wanted_transaction = transition['id']
                break

        if wanted_transaction == -1:
            error(u"Unable to find status {0} for issue {1}".format(new_status, self._link(issue_id)))

        # Prepare POST body
        transition_data = {
            "transition": {
                "id": wanted_transaction
            }
        }

        # Perform transition
        response = request.post(issue_url + "/transitions?expand=transitions.fields", self._serialize(transition_data), contentType='application/json')

        if response.status != 204:
            error(u"Unable to perform transition {0} for issue {1}".format(wanted_transaction, self._link(issue_id)), response)

    def _createRequest(self):
        return HttpRequest(self.jira_server, self.username, self.password)

    def _link(self, issue_id):
        return "[{0}]({1}/browse/{0})".format(issue_id, self.jira_server['url'])

    def _issueUrl(self, issue_id):
        return "/rest/api/2/issue/" + issue_id

    def _checkIssue(self, issue_id):
        request = self._createRequest()
        response = request.get(self._issueUrl(issue_id), contentType='application/json')

        if response.status != 200:
            error(u"Unable to find issue {0}".format(self._link(issue_id)), response)

    def _serialize(self, content):
        return Json.dumps(content).encode(self.encoding)


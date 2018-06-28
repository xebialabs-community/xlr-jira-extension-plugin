#
# Copyright 2018 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import com.xhaus.jyson.JysonCodec as Json
from jira import JiraServer
from util import error


class JiraServerExt(JiraServer):
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

    def getVersionIdsForProject(self, projectId):
        print "Executing jira.getVersionIdsForProject\n"
        if not projectId:
            error("No project id provided.")
        request = self._createRequest()
        response = request.get(self._versionsUrl(projectId), contentType="application/json")
        if response.status != 200:
            error(u"Unable to find versions for project id %s" % projectId, response)
        versionIds = []
        for item in Json.loads(response.response):
            versionIds.append(item['id'])
        print str(versionIds) + "\n"
        print "Exiting jira.getVersionIdsForProject\n"
        return versionIds

    def _versionsUrl(self, projectId):
        return "/rest/api/2/project/%s/versions" % projectId

    def queryForFields(self, query, fields):
        if not query:
            error('No JQL query provided.')

        # Create POST body
        content = {
            'jql': query,
            'startAt': 0,
            'fields': fields,
            'maxResults': 1000
        }

        # Do request
        request = self._createRequest()
        response = request.post('/rest/api/2/search', self._serialize(content), contentType='application/json')

        # Parse result
        if response.status == 200:
            data = Json.loads(response.response)

            issues = []
            for item in data['issues']:
                issue = {}
                for field in fields:
                    issue[field] = item[field]
                issues.append(issue)
            return issues
        else:
            error(u"Failed to execute search '{0}' in JIRA.".format(query), response)

    def queryForIssueIds(self, query):
        issues = self.queryForFields(query, ["id"])
        # for backwards compatibility, return a flat list with ids
        return [x["id"] for x in issues]

    def get_boards(self, board_name):
        if not board_name:
            error("No board name provided.")
        request = self._createRequest()
        response = request.get("/rest/agile/1.0/board?name=%s" % board_name, contentType="application/json")
        if response.status != 200:
            error(u"Unable to find boards for {0}".format(board_name), response)
        return Json.loads(response.response)['values']

    def get_all_sprints(self, board):
        if not board:
            error("No board id provided")
        request = self._createRequest()
        response = request.get("/rest/agile/1.0/board/%s/sprint" % board["id"], contentType="application/json")
        sprints = {}
        if response.status != 200:
            error(u"Unable to find sprints for board {0}".format(board["name"]), response)
        sprints_json = Json.loads(response.response)['values']
        for sprint_json in sprints_json:
            sprints[sprint_json["name"]] = sprint_json["id"]
            print "| %s | %s | %s | %s |" % (sprint_json["name"], sprint_json["id"],
                                             sprint_json["startDate"] if sprint_json.has_key(
                                                 "startDate") else "not defined",
                                             sprint_json["endDate"] if sprint_json.has_key(
                                                 "endDate") else "not defined")
        return sprints

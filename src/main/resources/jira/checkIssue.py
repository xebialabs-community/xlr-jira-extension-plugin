#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import sys, string
import com.xhaus.jyson.JysonCodec as json
import time

ISSUE_RETREIVED_STATUS = 200

if jiraServer is None:
    print "No server provided."
    sys.exit(1)

request = HttpRequest(jiraServer, username, password)

statusTask = '/rest/api/2/issue/' + issueId

while True:
    response = request.get(statusTask, contentType = 'application/json')

    # if response received from Jira
    if response.getStatus() == ISSUE_RETREIVED_STATUS:
        # retrieve issue status
        data = json.loads(response.getResponse())['fields']['status']
        issueStatus = data['name']
        print "\nIssue %s status is %s." % (issueId, issueStatus)
        if issueStatus == expectedStatus:
            print "\nThe status of issue %s is 'Resolved'" % (issueId)
            break
        else:
            print "\nIssue is not correct status"
            time.sleep(pollInterval)
    else:
        print "Error from JIRA, HTTP Return: %s" % (response.getStatus())
        response.errorDump()
        sys.exit(1)

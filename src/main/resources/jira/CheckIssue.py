#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#

import sys
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

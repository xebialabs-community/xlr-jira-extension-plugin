#
# Copyright 2019 XEBIALABS
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

def _serialize(content):
    return json.dumps(content).encode("utf-8")

def link(issue_id):
    return "[{0}]({1}/browse/{0})".format(issue_id, jiraServer['url'])

def error(text, response=None):
    print
    print u"#### Error: {0} ".format(text)
    if response is not None:
        response.errorDump()
    print
    raise Exception(text)

request = HttpRequest(jiraServer, username, password)

# Do request
response = request.post('/rest/api/2/issue', jsonObj, contentType='application/json')

# Parse result
if response.status == 201:
    data = json.loads(response.response)
    issueId = data.get('key')
    print u"Created {0} in JIRA.".format(link(issueId))
else:
    print u"Failed to create issue in JIRA. (%s)" % response.status
    error("Failed to create issue in JIRA.", response)
    sys.exit(1)

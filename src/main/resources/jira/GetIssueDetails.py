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

ISSUE_RETREIVED_STATUS = 200

def subDic( myObj, parrentKey ):
    localObject = {}
    for key in myObj.keys():
        if( parrentKey == "__ROOT__" ):
            compKey = "%s" % ( key )
        else:
            compKey = "%s.%s" % ( parrentKey, key )
        if( type(myObj[key]).__name__ == 'dict' ):
            localObject.update(subDic( myObj[key], compKey ))
        else:
            localObject[compKey] = myObj[key]
    return localObject


if jiraServer is None:
    print "No server provided."
    sys.exit(1)

request = HttpRequest(jiraServer, username, password)

statusTask = '/rest/api/2/issue/' + issueId

response = request.get(statusTask, contentType = 'application/json')

# if response received from Jira
if response.getStatus() == ISSUE_RETREIVED_STATUS:
    # retrieve issue status
    data = json.loads(response.getResponse())
    issueDetails = {}
    issueDetails = subDic( data, "__ROOT__" )

else:
    print "Error from JIRA, HTTP Return: %s" % (response.getStatus())
    response.errorDump()
    sys.exit(1)

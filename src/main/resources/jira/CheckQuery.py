#
# Copyright 2017 XEBIALABS
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#


import time
from jira.JiraServerExt import JiraServerExt

jira = JiraServerExt(jiraServer, username, password)

tickets = jira.checkQuery(query)

issues = {}
count = 0
matchedStatus = 0
while  len(tickets) != matchedStatus :
     matchedStatus = 0
     tickets = jira.checkQuery(query)
     for key, value in tickets.items():
         if value[1] == expectedStatus:
              matchedStatus + 1
         # End if
         issues[key] = "%s - (%s)" % value
     # End for
     time.sleep( pollInterval )
     count = count + 1
# End while 

print "#### Issues found"
for key, value in issues.items():
     print u"* {0} - {1}".format(jira._link(key), value)
# End for


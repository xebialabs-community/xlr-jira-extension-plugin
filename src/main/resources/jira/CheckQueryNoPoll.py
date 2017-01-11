#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import time
from jira.JiraServerExt import JiraServerExt

jira = JiraServerExt(jiraServer, username, password)

tickets = jira.checkQuery(query)

issues = {}
count = 0
matchedStatus = 0
tickets = jira.checkQuery(query)

for key, value in tickets.items():
    count = count + 1
    issues[key] = "%s - (%s)" % value
    # end if
# End for


if count > 0:
   print "#### Issues found"
   for key, value in issues.items():
       print u"* {0} - {1}".format(jira._link(key), value)
   sys.exit(1)
else:
     print "#### No issues found"
# end if

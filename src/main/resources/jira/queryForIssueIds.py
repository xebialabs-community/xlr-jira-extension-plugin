#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

print "Executing jira/queryForIssueIds.py\n"

from jira.JiraServerExt import JiraServerExt

jira = JiraServerExt(jiraServer, username, password)

issueIds = jira.queryForIssueIds(query)

print "End of jira/queryForIssueIds.py\n"


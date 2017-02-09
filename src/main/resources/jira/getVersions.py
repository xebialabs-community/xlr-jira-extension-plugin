#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

print "Executing jira/getVersions.py\n"

from jira.JiraServerExt import JiraServerExt

jira = JiraServerExt(jiraServer, username, password)

versions = jira.getVersionIdsForProject(projectId)

print "End of jira/getVersions.py\n"


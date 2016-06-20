# Preface #

This document describes the functionality provided by the xlr-jira-extension-plugin.

See the **XL Release Reference Manual** for background information on XL Release and release concepts.

# Overview #

The xlr-jira-extension-plugin provides additional Jira tasks beyond the default Create Issue and Update Issue supplied by default with XL Release. Currently only Check Status is provided by this plugin

## Installation ##

Place the latest released version under the `plugins` dir.

## Types ##

+ Check Status - Polls Jira to check the status of a Issue, will complete once the issue is in the correct state
  * `jiraServer` - Jira server from the Configuration screen in XL Release
  * `username` - Optional username override for the connection to Jira
  * `password` - Optional password override for the connection to Jira
  * `issueId` - Jira issue ID to check, e.g. SAN-672
  * `expectedStatus` - This is the Jira status to complete on, the task will poll until this status is met. This checks for a status name, e.g. "Resolved". To double check the case of a status, export an issue to XML and check the value of the status field.
  * `pollInterval` - Inteval in seconds between polling actions

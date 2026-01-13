---
title: Troubleshooting
description: "Information about monitoring and logging tools of Flows."
---

## Video Tutorial

Watch this comprehensive walkthrough of troubleshooting GitLab Duo workflows:

{{< youtube "T1KWz_xthEY" >}}

## Tools

Duo Flows uses the following logging and monitoring tools:

1. [LangSmith](https://smith.langchain.com/o/477de7ad-583e-47b6-a1c4-c4a0300e7aca/projects/p/5409132b-2cf3-4df8-9f14-70204f90ed9b?timeModel=%7B%22duration%22%3A%227d%22%7D) - collects logs scoped to underlaying graph execution, including information like: LLM completions or tool calls
1. [Google Cloud (GCP) logs explorer](https://cloudlogging.app.goo.gl/wqUxHXbqYzQ7ebb6A) are the logs from the Duo Workflow Service
   1. Users can provide you with a "session ID" and you can search for this in these GCP logs. For example if the user has a session ID of `123` then you can perform a [search for `resource.labels.service_name="duo-workflow-svc" and jsonPayload.workflow_id="1234"`](https://console.cloud.google.com/logs/query;query=resource.labels.service_name%3D%22duo-workflow-svc%22%20and%20jsonPayload.workflow_id%3D%221234%22;duration=PT30M?project=gitlab-runway-production) to get all log entries related to that user session.
1. In the GCP logs you will also see the `correlation_id`. This `correlation_id` can be used to correlate to logs from Rails and workhorse. You can find these logs at <https://log.gprd.gitlab.net/>. In the dropdown on the top left corner you can select `pubsub-rails-inf-gprd-*` for rails logs or `pubsub-workhorse-inf-gprd-*` for workhorse logs.
1. In Kibana, use the plus button next to the search bar to filter by `json.correlation_id.keyword`. You can find more Kibana tips at <https://handbook.gitlab.com/handbook/engineering/monitoring/#logs> and <https://handbook.gitlab.com/handbook/support/workflows/kibana/>.
1. Sentry error tracking collects error traces for:
   1. [Duo Workflow Service](https://new-sentry.gitlab.net/organizations/gitlab/issues/?limit=5&project=36&query=&sort=freq&statsPeriod=14d)
   1. [Duo Workflow Executor](https://new-sentry.gitlab.net/organizations/gitlab/issues/?limit=5&project=40&query=&sort=freq&statsPeriod=14d)
1. Runway monitoring [dashboard](https://dashboards.gitlab.net/d/runway-service/runway3a-runway-service-metrics?from=now-24h&orgId=1&timezone=utc&to=now&var-PROMETHEUS_DS=mimir-runway&var-environment=gprd&var-region=$__all&var-type=duo-workflow) - this a grafana dashboard that tracks hardware resource consumption for Duo Workflow Service
1. [Tableau dashboard for internal events tracking](https://10az.online.tableau.com/#/site/gitlab/views/DuoRequestWorkflow/DuoWorkflow) - displays aggregated data collected with internal event tracking, showing additional product metrics like total number of workflows, or distribution between differnt workflow outcomes

### Google Cloud (GCP) Logs explorer

Following projects hold logs for different pieces of Runway deployments:

1. `gitlab-runway-production` - holds logs for production runway deployments
1. `gitlab-runway-staging` - holds logs for staging runway deployments

When browsing Runway logs, you can narrow scope to piece of infrastructure that is of interest to you using following filters:

1. To filter only load balancer logs use:

   ```plain
   resource.type="http_load_balancer"
   resource.labels.forwarding_rule_name="duo-workflow-https"
   ```

1. To filter only Duo Workflow Service deployment logs use:

   ```plain
   resource.labels.service_name="duo-workflow-svc"
   ```

### gRPCurl

The [grpcurl](https://github.com/fullstorydev/grpcurl) is a cli tool that enables you to interact with gRPC servers just like `curl` does for http ones.

An example usage of `grpcurl` for Agent Foundations is shown in the example below:

1. Agent Foundations credentails can be obtained via `curl`

```bash
curl -X POST -H "Authorization: Bearer $GITLAB_API_PRIVATE_TOKEN" https://gitlab.com/api/v4/ai/duo_workflows/direct_access
```

1. With credentials assigned to environment variables `grpcurl` can be used to start bidirectional channel to Duo Workflow Service

```bash
grpcurl -keepalive-time 20 -H "x-gitlab-global-user-id":"$GLOBAL_USER_ID" \
   -H "x-gitlab-instance-id":"ea8bf81......." -H "x-gitlab-realm":"saas" \
   -H "x-gitlab-authentication-type":"oidc" \
   -H authorization:"bearer $GRPC_TOKEN" -d @ -vv -proto ../duo-workflow-service/contract/contract.proto
   -import-path ../duo-workflow-service/contract cloud.gitlab.com:443 DuoWorkflow/ExecuteWorkflow


Resolved method descriptor:
rpc ExecuteWorkflow ( stream .ClientEvent ) returns ( stream .Action );

Request metadata to send:
authorization: bearer eyJhbGc.....
x-gitlab-authentication-type: oidc
x-gitlab-global-user-id: Rf9.........
x-gitlab-instance-id: ea8bf810-..........
x-gitlab-realm: saas
```

1. With channel being established messages can be sent via stdin

```json
{
  "startRequest": {
    "workflowID": "12344",
    "goal": "create hello world in go",
    "workflowMetadata":  "{\"extended_logging\":true,\"git_sha\":\"e621c52bb0f3af0a102a06cf2e485aa961f60d8c\",\"git_url\":\"gitlab.com/gitlab-org/analytics-section/analytics-instrumentation/metric-dictionary.git\"}"
  }
}
```

## Enhanced Logging for Team Members

### Enabling Enhanced Logging

To enable enhanced logging for better troubleshooting, use the following Slack command within the `#production` slack channel:

```bash
/chatops run feature set duo_workflow_extended_logging --user=your_user_name true
```

> Replace `your_user_name` with your actual GitLab username.

This will enable detailed tracing in LangSmith, which provides the most comprehensive view of workflow execution including LLM completions, tool calls, and execution flow.

#### Important Privacy and Security Considerations

**⚠️ Data Privacy Warning**: Extended logging captures detailed workflow execution data in LangSmith, including LLM completions, tool calls, prompts, and model responses.

* **NO [RED](/handbook/security/policies_and_standards/data-classification-standard#red) DATA**: Do not use Agentic Chat with [RED](/handbook/security/policies_and_standards/data-classification-standard#red) data when the `duo_workflow_extended_logging` feature flag is enabled
* **Forward-only logging**: This feature only logs new interactions after it's enabled. If you experienced an issue before enabling the flag, you'll need to reproduce the issue after enabling the enhanced logging
* **Access restrictions**: Only GitLab AI Engineering team members have access to the LangSmith logs for troubleshooting purposes

### What to Share with AI Engineers

When requesting assistance, please provide:

* **Workflow ID**: Essential for tracing the specific execution
* **Expected vs. Actual behavior**: What you expected to happen vs. what actually happened
* **Steps to reproduce**: If the issue is reproducible
* **Timestamp**: When the issue occurred (helps narrow down logs)
* **Any error messages**: Screenshots or copied text of error messages

### Getting Your Workflow ID

The `workflow_id` is the same as the `session_id`. For Agentic Duo Chat, it can be found in the UI.

## Tips and tricks

A typical investigation around problematic Agent Foundations execution follows steps listed below:

Based on a user report:

1. Ask the user for the `workflow_id` for the problematic workflow which is displayed in the list of workflows
2. Use the `workflow_id` from previous step to filter down [langsmith traces](https://smith.langchain.com/o/477de7ad-583e-47b6-a1c4-c4a0300e7aca/projects/p/a86cfa18-72b2-4729-844e-94d4ffb7f54a?timeModel=%7B%22duration%22%3A%227d%22%7D) by applying a filter for `metadata` and `thread_id=[workflow_id]`
3. Use the `workflow_id` from 1st step to filter down logs in gcp logs explorer `jsonPayload.workflow_id="123456789"`

Based on a Sentry issue:

1. Use Agent Foundations Sentry issue to locate problematic workflow's `correlation_id`.
2. Use the `correlation_id` from previous step to filter down logs in gcp logs explorer, example filter: `jsonPayload.correlation_id="e7171f28-706d-4a47-be25-29d9b3751c0e"`

In addition one can use a workflow's `workflow_id` that is being recorded either in sentry or in log explorer to filter down LangSmith logs using `thread_id` filter in _metadata_ and comparing it against `workflow_id`.

## Past in depth investigations

1. Faulty network proxy via Cloudflare [investigation issue](https://gitlab.com/gitlab-org/gitlab/-/issues/501170)

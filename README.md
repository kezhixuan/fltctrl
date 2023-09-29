# SQ Dahsboard

SQ Dashboard is meant to present projects statuses from the QA perspective: list crucial bugs,
present information to about number of bugs among other statistics and defined KPIs.

This incarnation of the SQ Dashboard is a project meant as a replacement for the older dashboard.
The previous dashboard didn't store any information and was always pulling data from JIRA,
TestRail and others. This incarnation of the SQ Dashboard is meant to remedy that shortcoming.

## Technical insight

On the technical level the dashboard name might be misleading. There is no 'view' layer in
the project. There are only specific components responsible for collecting and storing specific
data. Details of these components are described below:
- data-sources: responsible for connecting to the defined external data source and pulling
required data from there:
    - TestRail data source
    - JIRA data source
- data-sink: responsible for pushing the data to the defined storing location:
    - file
    - mongodb

## Add new project

TODO: Add section describing how to add a new project to the SQ Dashboard

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://git.signintra.com/qa-dashboard/qa-dashboard/flightctrl.git
git branch -M main
git push -uf origin main
```

## Integrate with your tools

- [ ] [Set up project integrations](https://git.signintra.com/qa-dashboard/qa-dashboard/flightctrl/-/settings/integrations)

## Collaborate with your team

- [ ] [Invite team members and collaborators](https://docs.gitlab.com/ee/user/project/members/)
- [ ] [Create a new merge request](https://docs.gitlab.com/ee/user/project/merge_requests/creating_merge_requests.html)
- [ ] [Automatically close issues from merge requests](https://docs.gitlab.com/ee/user/project/issues/managing_issues.html#closing-issues-automatically)
- [ ] [Enable merge request approvals](https://docs.gitlab.com/ee/user/project/merge_requests/approvals/)
- [ ] [Set auto-merge](https://docs.gitlab.com/ee/user/project/merge_requests/merge_when_pipeline_succeeds.html)

## Test and Deploy

Use the built-in continuous integration in GitLab.

- [ ] [Get started with GitLab CI/CD](https://docs.gitlab.com/ee/ci/quick_start/index.html)
- [ ] [Analyze your code for known vulnerabilities with Static Application Security Testing(SAST)](https://docs.gitlab.com/ee/user/application_security/sast/)
- [ ] [Deploy to Kubernetes, Amazon EC2, or Amazon ECS using Auto Deploy](https://docs.gitlab.com/ee/topics/autodevops/requirements.html)
- [ ] [Use pull-based deployments for improved Kubernetes management](https://docs.gitlab.com/ee/user/clusters/agent/)
- [ ] [Set up protected environments](https://docs.gitlab.com/ee/ci/environments/protected_environments.html)


# -*- coding: utf-8 -*-

#
# Unless explicitly stated otherwise all files in this repository are licensed
# under the Apache 2 License.
#
# This product includes software developed at Datadog
# (https://www.datadoghq.com/).
#
# Copyright 2018 Datadog, Inc.
#

"""create_issue_issue.py

Creates a JIRA issue based on GitHub issue data.
"""

import textwrap
from . import CreateJIRAIssue
from ..services import IssueService


class CreateIssueIssue(CreateJIRAIssue):
    """A class that creates a trello card on a board."""

    def __init__(self):
        """Initializes a task to create an issue trello card."""
        super().__init__()
        self._issue_service = IssueService()

    def _issue_body(self):
        """Concrete helper method.

        Internal helper to format the jira issue description, based on the data
        passed in.

        Returns:
            str: the markdown template for the JIRA Issue created.
        """
        return textwrap.dedent(
            f"""
            h1. GitHub Issue Opened By Community Member
            ----

            * Issue link: [{self._title}|{self._url}]
            * Opened by: [{self._user}|{self._user_url}]
            ----

            h3. Issue Body
            ----

            """
        ) + self._body

    def _persist_issue_to_database(self, issue):
        """Concrete helper method.

        Internal helper to save the record created to the database.

        Args:
            issue (trello.Issue): An object representing the JIRA created.

        Returns:
            None
        """
        self._issue_service.create(
            name=self._title,
            url=self._url,
            github_issue_id=self._id,
            repo_id=self._repo_id,
            jira_project_key=issue.fields.project.key,
            jira_issue_key=issue.key,
            jira_parent_issue_key=issue.fields.parent.key
            if hasattr(issue.fields, 'parent') else None
        )

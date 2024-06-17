import typing as t
from shared.composio_tools.lib import Action, Tool

from .actions import (
    AddDomainAction,
    CreateEnvVarAction,
    CreateProjectAction,
    DeleteProjectAction,
    EditEnvVarAction,
    FindProjectAction,
    GetEnvVarsAction,
    PauseProjectAction,
    UnpauseProjectAction,
    UpdateProjectAction,
)


class Vercel(Tool):
    """
    Tool for managing Vercel projects.
    """

    def actions(self) -> list:
        return [
            GetEnvVarsAction,
            FindProjectAction,
            AddDomainAction,
            CreateProjectAction,
            CreateEnvVarAction,
            DeleteProjectAction,
            EditEnvVarAction,
            PauseProjectAction,
            UnpauseProjectAction,
            UpdateProjectAction,
        ]

    def triggers(self) -> list:
        return []

__all__ = ["Vercel"]
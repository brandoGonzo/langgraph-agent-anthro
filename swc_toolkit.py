import os
from typing import Optional, Type, List

from pydantic import BaseModel, Field

from langchain_core.callbacks import CallbackManagerForToolRun
from langchain_core.tools import BaseTool, BaseToolkit

try:
    from swcpy import SWCClient
    from swcpy import SWCConfig
    from swcpy.swc_client import League, Team
except ImportError:
    raise ImportError(
        "swcpy package not found. Please install it with 'pip install swcpy'"
    )

config = SWCConfig(backoff=False)
local_swc_client = SWCClient(config)


class HealthCheckInput(BaseModel):
    pass


class HealthCheckTool(BaseTool):
    name: str = "health_check"
    description: str = ("Check if the API is running and healthy.")
    args_schema: Type[HealthCheckInput] = HealthCheckInput
    return_direct: bool = False

    def _run(
        self, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Check if the API is running and healthy."""
        health_check_response = local_swc_client.get_health_check()
        return health_check_response.text


class LeaguesInput(BaseModel):
    league_name: Optional[str] = Field(
        default=None,
        description="league name. Leave blank or None to get all leagues."
    )


class ListLeaguesTool(BaseTool):
    name: str = "ListLeagues"
    description: str = (
        "get a list of leagues from the SWC API."
        "Leagues contain teams if they are present."
    )
    args_schema: Type[LeaguesInput] = LeaguesInput
    return_direct: bool = False

    def _run(
        self, league_name: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[League]:
        """Use the tool to get a list of leagues from the SWC API."""
        # Call the API with league_name, which should be None to get all leagues.
        list_leagues_response = local_swc_client.list_leagues(league_name)
        return list_leagues_response


class TeamsInput(BaseModel):
    team_name: Optional[str] = Field(
        default=None,
        description="team name. Leave blank or None to get all teams."
    )
    league_id: Optional[int] = Field(
        default=None,
        description=(
            "League ID from a league. You must provide a numberical League ID."
            "Leave blank or None to get all teams."
        ))


class ListTeamsTool(BaseTool):
    name: str = "ListTeams"
    description: str = (
        "Get a list of teams from the SWC API. Teams contain player data."
        "Optionally, provide a numerical League ID to filter teams from a specific league."
    )
    args_schema: Type[TeamsInput] = TeamsInput
    return_direct: bool = False

    def _run(
        self, team_name: Optional[str] = None,
        league_id: Optional[int] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> List[Team]:
        """Use the tool to get a list of teams from the SWC API."""
        list_teams_response = local_swc_client.list_teams(
            team_name=team_name, league_id=league_id)
        return list_teams_response

class SportsWorldCentralToolkit(BaseToolkit):
    def get_tools(self) -> List[BaseTool]:
        """Return the list of tools in the toolkit."""
        return [
            HealthCheckTool(),
            ListLeaguesTool(),
            ListTeamsTool(),
        ]
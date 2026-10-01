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

# TODO: Implement this tool
class ListLeaguesTool(BaseTool):
    pass
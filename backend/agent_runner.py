import sys
import os

sys.path.append(os.path.abspath("sragent_crewai/src"))
sys.path.append(os.path.abspath("fedlead_agent_crewai/src"))

def run_tool(tool: str, goal: str = None):
    if tool == "sragent_run":
        from sragent_crewai.main import run
        return run()

    elif tool == "fedlead_run":
        from fedlead_agent_crewai.main import run
        return run()

    else:
        return f"Unknown tool: {tool}"

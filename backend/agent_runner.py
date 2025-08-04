#This uses the local agents, not task definitions
#import sys
#import os

#sys.path.append(os.path.abspath("sragent_crewai/src"))
#sys.path.append(os.path.abspath("fedlead_agent_crewai/src"))

#def run_tool(tool: str, goal: str = None):
#    if tool == "sragent_run":
#        from sragent_crewai.main import run
#        return run()

#    elif tool == "fedlead_run":
#        from fedlead_agent_crewai.main import run
#        return run()

#    else:
#        return f"Unknown tool: {tool}"


#task definition version
import boto3
import json
import uuid
import os

CLUSTER_ARN = os.getenv("CLUSTER_ARN")
SUBNET_ID = os.getenv("SUBNET_ID")
SECURITY_GROUP = os.getenv("SECURITY_GROUP")
STEP_FUNCTION_ARN = os.getenv("STEP_FUNCTION_ARN")

ecs_client = boto3.client("ecs", region_name="us-east-2")
sf_client = boto3.client("stepfunctions", region_name="us-east-2")


def run_tool(tool: str, goal: str = None):
    if tool == "sragent_run":
        return run_ecs_task(task_def="sragent-task", container="sragent", goal=goal)
    elif tool == "fedlead_run":
        return run_ecs_task(task_def="fedagent-task", container="fedlead", goal=goal)
    elif tool == "step_function":
        return run_step_function(goal)
    else:
        return f"Unknown tool: {tool}"
    
def run_ecs_task(task_def: str, container: str, goal: str = None):
    overrides = {
        "containerOverrides": [{
            "name": container,
            "environment": [{"name": "GOAL", "value": goal or ""}]
        }]
    }

    response = ecs_client.run_task(
        cluster=CLUSTER_ARN,
        launchType="FARGATE",
        taskDefinition=task_def,
        count=1,
        platformVersion="LATEST",
        networkConfiguration={
            "awsvpcConfiguration": {
                "subnets": [SUBNET_ID],
                "assignPublicIp": "ENABLED",
                "securityGroups": [SECURITY_GROUP]
            }
        },
        overrides=overrides
    )

    return {
        "taskArn": response["tasks"][0]["taskArn"],
        "status": "started"
    }
    
    
def run_step_function(goal: str = None):
    execution_input = {
        "goal": goal or "default-goal",
        "run_id": str(uuid.uuid4())
    }

    response = sf_client.start_execution(
        stateMachineArn=STEP_FUNCTION_ARN,
        name=f"exec-{uuid.uuid4()}",
        input=json.dumps(execution_input)
    )
    return {
        "executionArn": response["executionArn"],
        "startDate": str(response["startDate"])
    }
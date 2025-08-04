# **CRDC Datahub Agent Farm**

This project delivers a fully cloud-native, self-improving multi-agent AI system to automate the end-to-end CRDC Datahub submission process. Built using the CrewAI framework, the system leverages modular, Dockerized agents deployed on AWS ECS Fargate and orchestrated via AWS Step Functions to perform intelligent, scalable automation of submission creation, metadata population, and review approval.

Each agent operates as a self-contained service capable of actions such as logging in, navigating dynamic forms, generating metadata via AWS Bedrock, and simulating user interaction through Playwright. Execution logs — including tool inputs, outputs, system feedback — are written to DynamoDB, enabling full observability and traceability. A Bedrock-based evaluator periodically analyzes these logs to extract generalized prompt templates, enabling agents to evolve from hardcoded logic to adaptive, prompt-driven behavior over time.

Interaction with the system is currently supported via a FastAPI backend, deployed in the cloud. Users can trigger agent runs either through AWS Step Functions or by directly invoking ECS tasks using FastAPI endpoints. The architecture is designed from the ground up to be modular, extensible, and production-ready — with each component deployable independently across isolated containers and fully integrated with AWS infrastructure.


## Setup (Development use only)
1. **Activate the Python virtual environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Add Login Info to .env files**
```
   MODEL=YOUR_LLM_MODEL
   TOTP_SECRET=YOUR_TOTP_SECRET
   LOGIN_USERNAME=YOUR_LOGIN_USERNAME
   LOGIN_PASSWORD=YOUR_LOGIN_PASSWORD
```

3. **Install requirements**
   ```bash
   pip install requirements
   ```

4. **Start the FastAPI backend**
```bash
python -m uvicorn backend.main:app --reload 
```
5. **Acces the API docs**

Open your browser and navigate to:
http://localhost:8000/docs#/default/handle_run_run_post

6. **Running Agents through API**

To trigger a run via the API, use the /run endpoint with a JSON payload like one of the following:
- to run the submission request agent:
```json
{
  "tool": "sragent_run"

}
```
- to run the submission approval agent:
```json
{
  "tool": "fedlead_run"

}
```


## Using the Cloud API

You can explore and test the API using the Swagger docs available at:
http://<your-ec2-ip>:8000/docs

### POST /run
To run agents, send a POST request to:
http://<your-ec2-ip>:8000/run

- Run the **end-to-end workflow**:
```json
{
  "tool": "step_function",
  "goal": "go through the crdc workflow"
}
```

- Run the **Submission Request Agent**:
```json
{
  "tool": "sragent_run",
  "goal": "create a submission request"
}
```

- Run the **Submission Approval Agent**:
```json
{
  "tool": "fedlead_run",
  "goal": "approve the latest submission request"
}
```

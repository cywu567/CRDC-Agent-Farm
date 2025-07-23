### **CRDC Datahub Agent Farm**

This project delivers a fully cloud-native, self-improving multi-agent AI system to automate the end-to-end CRDC Datahub submission process. Built using the CrewAI framework, the system leverages modular, Dockerized agents deployed on AWS ECS Fargate and orchestrated via AWS Step Functions to perform intelligent, scalable automation of submission creation, metadata population, and review approval.

Each agent operates as a self-contained service capable of actions such as logging in, navigating dynamic forms, generating metadata via AWS Bedrock, and simulating user interaction through Playwright. Execution logs — including tool inputs, outputs, system feedback — are written to DynamoDB, enabling full observability and traceability. A Bedrock-based evaluator periodically analyzes these logs to extract generalized prompt templates, enabling agents to evolve from hardcoded logic to adaptive, prompt-driven behavior over time.

Interaction with the system is supported via a React frontend and FastAPI backend, allowing users to chat with agents, monitor task progress, view history, and provide real-time feedback. The architecture is designed from the ground up to be modular, extensible, and production-ready — with each component deployable independently across isolated containers and fully integrated with AWS infrastructure.


## Setup
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
.venv/bin/python -m uvicorn backend.main:app --reload 
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

7. **Running Agents Using Dockerfiles**

- Navigate to the service directory, e.g., for the backend:
```bash
cd backend
```
- Build the Docker image:
```bash
docker build -t crdc-backend .
```
- Run the container:
```bash
docker run -p 8000:8000 crdc-backend
```
- Access the FastAPI Swagger UI in your browser:
   - http://localhost:8000/docs (backend)
   - http://localhost:8001/docs (FedLead agent)
   - http://localhost:8002/docs (Submission request agent)

# monty
A FastAPI-based service designed for high-concurrency image processing, utilizing **AWS S3** for storage and **DynamoDB** for metadata persistence. This project is engineered with a "build once, deploy anywhere" philosophy, featuring the **AWS Lambda Web Adapter** for serverless readiness.

---

## 🛠 Tech Stack
- **FastAPI**: Modern Python web framework.
- **LocalStack**: AWS cloud emulation (S3, DynamoDB).
- **Docker & Docker Compose**: Environment orchestration.
- **Pytest**: Integration testing suite.
- **Poetry**: Dependency management.

---

## 🚀 Local Setup & Execution

Follow these steps to pull, build, and run the service on your local machine.

### 1. Prerequisites
Ensure you have **Docker Desktop** installed and running.

### 2. Launch the Stack
This command builds the FastAPI container and starts LocalStack. It also triggers `init-aws.sh` to automatically provision the necessary S3 buckets and DynamoDB tables.
```bash
docker compose up --build -d
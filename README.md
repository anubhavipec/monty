# Monty: Cloud-Native Image Management Service

This project is a FastAPI-based service designed to handle image uploads to **AWS S3** and metadata persistence in **AWS DynamoDB**. It is engineered to be "Cloud-Native," utilizing the **AWS Lambda Web Adapter** to allow the same Docker container to run seamlessly on either a standard server or as a Serverless AWS Lambda function.

## 🛠 Tech Stack

*   **FastAPI**: High-performance Python web framework.
    
*   **LocalStack**: Cloud service emulation for S3 and DynamoDB.
    
*   **Docker & Docker Compose**: Consistent environment orchestration.
    
*   **Pytest**: Integration testing suite.
    
*   **Poetry**: Dependency management.
    

* * *

## 🚀 Getting Started (Local Setup)

Follow these steps to run the entire stack on your local machine.

### 1\. Clone the repository

Bash

    git clone <your-repo-url>
    cd monty

### 2\. Start the Containers

This command builds the API and starts LocalStack. An initialization script (`init-aws.sh`) runs automatically to provision the S3 bucket and DynamoDB table.

Bash

    docker compose up --build -d

### 3\. Verify the Services

Once the containers are running, you can access the following:

*   **Interactive API Docs (Swagger):** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)
    


* * *

## 🧪 Running Integration Tests

The project includes a suite of tests that verify the integration between the FastAPI app and the AWS services.

**Ensure the containers are running**, then execute:

Bash

    chmod +x run_tests.sh
    ./run_tests.sh

_This script executes `pytest` inside the running container to ensure the environment matches the production configuration._

* * *

## 📂 Project Architecture

*   **`app/`**: Contains the FastAPI application, AWS service logic, and configuration.
    
*   **`tests/`**: Integration tests located at the root for standard discovery.
    
*   **`init-aws.sh`**: A shell script that runs on LocalStack startup to ensure the `user-images` bucket and `ImageMetadata` table exist.
    
*   **`Dockerfile`**: Uses a multi-stage build and includes the **AWS Lambda Web Adapter** binary (`/lambda-adapter`), enabling the app to listen on `$PORT` in a Lambda environment.
    

* * *

## 📝 API Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| POST | /upload | Upload image to S3 and save metadata to DynamoDB. |
| GET | /images | List all uploaded images with optional filtering. |
| GET | /images/{id}/download | Generate a temporary presigned URL for secure download. |
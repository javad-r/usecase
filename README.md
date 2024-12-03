# Instagram Post Classification Use Case

## Overview

This project focuses on extracting topics from Instagram posts, performing multilabel classification on the extracted topics, and exposing the classification functionality through a REST API. The project leverages Infrastructure as Code (IaC) using Terraform for managing Azure resources.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Usage](#usage)
  - [Topic Extraction](#topic-extraction)
  - [Classification](#classification)
  - [Running the API Locally](#running-the-api-locally)
  - [Build and Push Docker Image to ACR](#build-and-push-docker-image-to-acr)
- [API Endpoints](#api-endpoints)
  - [POST /predict](#post-predict)

## Features

- **Topic Extraction**: Extracts key topics from Instagram posts using Natural Language Processing (NLP) techniques.
- **Multilabel Classification**: Classifies posts into multiple categories based on the extracted topics.
- **REST API**: Provides classification functionality through a FastAPI-based REST API.
- **Infrastructure as Code (IaC)**: Manages Azure resources using Terraform for streamlined deployment.

## Technologies Used

- **Programming Language**: Python
- **Libraries/Frameworks**: Pandas, Scikit-learn, FastAPI, NLTK, Joblib, PySpark
- **Infrastructure**: Azure Machine Learning, Terraform, Docker
- **Tools**: PyCharm, Azure Container Registry, Azure App Service
- **Other**: NumPy

## Project Structure

```plaintext
│
├── src/                            # Source code for the project
│   ├── topic_extraction/           # Code for topic extraction
│   ├── classification/             # Code for classification
│   ├── api/                        # FastAPI application code
│
├── infra/                          # Terraform scripts for IaC
│
├── .gitignore                      # Git ignore file
├── README.md                       # Project documentation
└── script.sh                       # Script to build/push Docker image to ACR
```

## Getting Started

Follow these steps to set up the environment and run the application:

### 1. Clone the Repository

```bash
git clone <repository-url>
cd instagram_classification_project
   ```

### 2. Configure Azure Resources

Set up the necessary Azure resources using Terraform:

1. Navigate to the `infra` directory:

    ```bash
    cd infra
    ```

2. Initialize Terraform:

    ```bash
    terraform init
    ```

3. Review the Terraform plan:

    ```bash
    terraform plan
    ```

4. Apply the Terraform configuration to create the Azure resources:

    ```bash
    terraform apply
    ```

    Confirm the prompt with `yes` to provision the resources.

After completing these steps, the following resources will be created:

1. **Azure Resource Group**  
   - A resource group to organize all the resources.

2. **Azure Storage Account**  
   - Used for general-purpose storage (Standard LRS replication).

3. **Azure Key Vault**  
   - Secures sensitive information, such as secrets, keys, and certificates.

4. **Azure Application Insights**  
   - Monitors the application and provides telemetry data.

5. **Azure Container Registry (ACR)**  
   - Stores container images for the FastAPI application.

6. **Azure Machine Learning Workspace**  
   - A workspace for machine learning models and operations, integrated with Key Vault, Storage Account, Application Insights, and ACR.

7. **Azure App Service Plan**  
   - A Linux-based App Service Plan used to host the FastAPI application.

8. **Azure App Service (Linux Web App)**  
   - Hosts the FastAPI application with support for containerized deployments.  
   - Includes the following configurations:
     - System-assigned identity for secure integration with other Azure services.
     - Environment variables for the application.
     - Configured to pull the container image from the Azure Container Registry (ACR).

9. **Azure Role Assignment for ACR Pull**  
   - Assigns the `AcrPull` role to the App Service to allow pulling container images from the Azure Container Registry.

## Usage

### Topic Extraction

* Use the `./topic_extraction/LDA.ipynb` notebook located in the src/topic_extraction/ directory to extract topics.
- Update the notebook with the path to your dataset and adjust parameters for optimal performance.
- The notebook preprocesses text, tokenizes data, removes stopwords, and performs lemmatization. Finally, it applies LDA for topic modeling.

### Classification

* Prerequisite steps for Azure Machine Learning (AML):
  - Deploy Azure resources using Terraform.
  - Manually create a workspace in Azure Machine Learning.
  - Register the dataset obtained from the topic extraction step in the datastore.
  - Provision a compute instance for training.
- Use the `./classficiation/usecasetest.ipynb` notebook to preprocess the data, train a multilabel classification model, and store the model for inference.
- Deploy the model using `./classficiation/deployment.ipynb`, which sets up an Azure Managed Online Endpoint.
The classification task is done by using Azure Machine learning space.

### Running the API Locally

To run the FastAPI application locally:

1. Navigate to the src/api directory.
2. Start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Build && Push the image of API app to ACR

- Use the script.sh script to build and push the Docker image to Azure Container Registry (ACR)

### API Endpoints

#### 1. POST /predict

- **Description**: Classifies the input text into multiple categories based on extracted topics. You can send requests to the API using tools like Postman or cURL.
- **Request Body**:

    ```json
    {
        "text": [
            "Sample Instagram post 1!",
            "Sample Instagram post 2!"
        ]
    }
    ```

- **Request Header**:

    ```
        x-api-key : <Your API Key for App service>
    ```

- **Response**:
  - **Success**: Returns the predicted labels for the input text.

    ```json
    {
        [
            {
                "input_text": "Sample Instagram post 1!",
                "predicted_topics": ["topic 15", "topic 19"],
                "decoded_topics": [
                    ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
                    ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
                ]
            },
            {
                "input_text": "Sample Instagram post 2!",
                "predicted_topics": ["topic 7", "topic 11", "topic 15"],
                "decoded_topics": [
                    ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],,
                    ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],,
                    ["keyword 1", "keyword 2", "keyword 3", "keyword 4", "keyword 5"],
                ]
            }
        ]
    }
    ```

  - **Error**: Returns an error message if the input is invalid or an exception occurs.

    ```json
    {
        "error": "Error message"
    }
    ```

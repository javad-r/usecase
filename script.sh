# sett the model key and endpint 
export TF_VAR_AZURE_ML_ENDPOINT="https://your-ml-endpoint.azurewebsites.net"
export TF_VAR_AZURE_ML_API_KEY="your api key for ml model rest api"
export TF_VAR_APP_SERVICE_API_KEY="your api key for app service "

# Build the Docker image
docker build -t myapp .

# Login to Azure Container Registry (if using)
# get/change the acr name from variables.tf 
az acr login --name usecasetest

# Tag the image
docker tag myapp:latest usecasetest.azurecr.io/myapp:latest

# Push the image to Azure Container Registry
docker push usecasetest.azurecr.io/myapp:latest

# Initialize Terraform
terraform init

# Plan the deployment
terraform plan

# Apply the changes (deploy)
terraform apply


# flask-deploy-pipeline

A sample Flask project for CI/CD deployment on AWS.

## Project Structure
```
flask-deploy-pipeline/
├── config/
│   └── config.json
├── deploy.py
├── requirements.txt
└── README.md
```

## How to Run Locally
```bash
pip install -r requirements.txt
python deploy.py
```

## Deployment (AWS Elastic Beanstalk)
- Dockerize the app (see Dockerfile below)
- Use the provided GitHub Actions workflow for CI/CD

## Dockerfile
```
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "deploy.py"]
```

## GitHub Actions Workflow
Add this to `.github/workflows/aws-deploy.yml`:
```
name: Deploy to AWS Elastic Beanstalk

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v3

    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'

    - name: Install AWS CLI
      run: pip install awscli

    - name: Zip application
      run: zip -r app.zip . -x '*.git*'

    - name: Deploy to Elastic Beanstalk
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        AWS_DEFAULT_REGION: 'us-east-1'
      run: |
        aws elasticbeanstalk create-application-version --application-name <your-app-name> --version-label $GITHUB_SHA --source-bundle S3Bucket=<your-bucket>,S3Key=app.zip
        aws elasticbeanstalk update-environment --environment-name <your-env-name> --version-label $GITHUB_SHA
```
Replace `<your-app-name>`, `<your-env-name>`, and `<your-bucket>` with your AWS details.

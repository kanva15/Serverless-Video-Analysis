# Serverless-Video-Analysis
=====================================

This project implements a serverless video analysis pipeline using AWS Lambda, Amazon S3, Docker, and PyTorch. It extracts frames from a video, classifies each frame using a pre-trained deep learning model, and uploads the results back to S3.

Features
--------
- Serverless architecture using AWS Lambda and ECR
- Frame extraction using FFmpeg
- Image classification using PyTorch (ResNet-50)
- S3 integration for video input and results output
- Docker-based Lambda deployment for custom dependencies

Project Structure
-----------------
serverless-video-analysis/
├── Dockerfile             # Lambda-compatible Docker container
├── main.py                # Lambda handler and processing logic
├── requirements.txt       # Python dependencies
└── README.txt             # Project documentation

Technologies
------------
- AWS Lambda
- AWS S3
- AWS ECR
- Docker
- Python 3.8
- PyTorch
- FFmpeg

Setup Instructions
------------------

1. Clone the Repository

   git clone https://github.com/kanva15/serverless-video-analysis.git
   cd serverless-video-analysis

2. Configure AWS Credentials

   Ensure your AWS credentials have the following permissions:
   - ecr:*
   - s3:*
   - lambda:*

   Configure AWS CLI:
   aws configure

Docker Build & Push
-------------------

3. Build Docker Image

   docker buildx build --platform linux/amd64 -t video-analysis . --load

4. Tag and Push to AWS ECR

   aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<region>.amazonaws.com

   docker tag video-analysis:latest <your-account-id>.dkr.ecr.<region>.amazonaws.com/video-analysis:latest

   docker push <your-account-id>.dkr.ecr.<region>.amazonaws.com/video-analysis:latest

Test Locally (Optional)
-----------------------
   docker run -v $(pwd):/var/task video-analysis

Deploy Lambda Function
----------------------
1. Go to AWS Lambda > Create Function > Container Image
2. Use the ECR image URI you pushed.
3. Set an execution role with S3 access permissions.
4. Optionally add environment variables:
   - S3_BUCKET_NAME = your bucket name

Input / Output
--------------
- Upload a video (e.g., sample.mp4) to your S3 bucket.
- Lambda will:
  1. Extract frames using FFmpeg
  2. Classify frames using ResNet-50
  3. Upload results to s3://<bucket>/results/

Dependencies
------------
torch
torchvision
boto3

Sample Output
-------------
frame_001.jpg: Class Index 970
frame_002.jpg: Class Index 107
frame_003.jpg: Class Index 815
...

License
-------
MIT License. See LICENSE file for details.

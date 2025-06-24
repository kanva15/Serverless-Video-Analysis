import os
import subprocess
from PIL import Image
import torch
from torchvision import models, transforms
import boto3

# 🪣 Set your S3 bucket name here
S3_BUCKET_NAME = 'video-analysis-kanva'  # ← REPLACE this

# Step 1: Extract frames
def extract_frames(video_path, output_dir="frames"):
    os.makedirs(output_dir, exist_ok=True)
    cmd = f"ffmpeg -i {video_path} -vf fps=1 {output_dir}/frame_%03d.jpg"
    subprocess.run(cmd, shell=True)
    print(f"Frames extracted to '{output_dir}'")

# Step 2: Load pre-trained model
def load_model():
    model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)
    model.eval()
    return model

# Step 3: Analyze one image
def analyze_image(image_path, model, transform):
    image = Image.open(image_path).convert("RGB")
    input_tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        prediction = torch.argmax(output, dim=1).item()
    return prediction

# Step 4: Upload file to S3
def upload_to_s3(file_path, s3_path):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, S3_BUCKET_NAME, s3_path)
    print(f"Uploaded to s3://{S3_BUCKET_NAME}/{s3_path}")

# Main
if __name__ == "__main__":
    video_file = "sample.mp4"
    frame_dir = "frames"

    extract_frames(video_file, frame_dir)

    model = load_model()
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor()
    ])

    for frame in sorted(os.listdir(frame_dir)):
        if frame.endswith(".jpg"):
            path = os.path.join(frame_dir, frame)
            result = analyze_image(path, model, transform)
            print(f"{frame}: Class Index {result}")
            # Upload frame to S3 under a results folder
            s3_key = f"results/{frame}"
            upload_to_s3(path, s3_key)

import torch
import torchvision.models as models
import torchvision.transforms as transforms
from PIL import Image
import numpy as np
import os

class FeatureExtractor:
    def __init__(self):
        print("Loading ResNet50 model...")
        # Load pretrained ResNet50
        self.model = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        # Remove last classification layer — we want features not labels
        self.model = torch.nn.Sequential(*list(self.model.children())[:-1])
        self.model.eval()
        
        # Image preprocessing pipeline
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        print("✅ ResNet50 loaded successfully")

    def extract(self, image_path):
        try:
            # Load and preprocess image
            img = Image.open(image_path).convert('RGB')
            img_tensor = self.transform(img).unsqueeze(0)
            
            # Extract features
            with torch.no_grad():
                features = self.model(img_tensor)
            
            # Flatten to 2048-dimensional vector
            features = features.squeeze().numpy()
            # Normalize vector
            features = features / np.linalg.norm(features)
            return features
            
        except Exception as e:
            print(f"Error processing {image_path}: {e}")
            return None

# Test it
if __name__ == "__main__":
    extractor = FeatureExtractor()
    
    # Test on first image in dataset
    test_image = "data/images/15970.jpg"
    if os.path.exists(test_image):
        features = extractor.extract(test_image)
        print(f"✅ Feature vector shape: {features.shape}")
        print(f"✅ First 5 values: {features[:5]}")
    else:
        print("Test image not found — check path")
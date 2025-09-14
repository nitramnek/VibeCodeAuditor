"""
PyTorch sample with ML security vulnerabilities for testing framework-specific rules.
"""

import torch
import torch.nn as nn
import pickle
import requests
import os

# Unsafe model loading - major security risk
def load_model_unsafe():
    """Loading model without map_location - can execute arbitrary code."""
    model = torch.load('model.pth')  # Vulnerable: no map_location
    return model

def load_model_from_url():
    """Loading model from HTTP URL - man-in-the-middle risk."""
    model_url = "http://untrusted-site.com/model.pth"
    model = torch.load(model_url)  # Vulnerable: HTTP + no map_location
    return model

def load_with_pickle():
    """Using pickle directly with .pth files."""
    with open('model.pth', 'rb') as f:
        model = pickle.load(f)  # Vulnerable: pickle can execute code
    return model

def unsafe_jit_loading():
    """Loading JIT model from untrusted source."""
    jit_model = torch.jit.load("http://malicious-site.com/model.pt")  # Vulnerable
    return jit_model

def trust_repo_without_verification():
    """Trusting repository without proper verification."""
    model = torch.hub.load('untrusted/repo', 'model', trust_repo=True)  # Risky
    return model

class VulnerableModel(nn.Module):
    """Model with potential security issues."""
    
    def __init__(self):
        super().__init__()
        self.fc = nn.Linear(10, 1)
        
        # Hardcoded model parameters - not a security issue but bad practice
        self.secret_weight = torch.tensor([1.234, 5.678])
    
    def forward(self, x):
        # Potential gradient leak if not handled properly
        torch.autograd.set_grad_enabled(False)
        result = self.fc(x)
        # Missing proper context management
        return result

def unsafe_data_loading():
    """Loading data without validation."""
    # Loading data from untrusted source
    data_url = "http://untrusted-data.com/dataset.pt"
    response = requests.get(data_url)
    
    # Saving and loading without validation
    with open('temp_data.pt', 'wb') as f:
        f.write(response.content)
    
    # Loading without validation
    data = torch.load('temp_data.pt')  # Vulnerable: no validation
    return data

def model_inference_without_validation(model, user_input):
    """Model inference without input validation."""
    # No input validation - could lead to adversarial attacks
    with torch.no_grad():
        prediction = model(user_input)  # Should validate input shape, range, etc.
    return prediction

def save_model_insecurely(model):
    """Saving model without proper security considerations."""
    # Saving to world-readable location
    torch.save(model.state_dict(), '/tmp/model.pth')  # Insecure location
    
    # Saving with pickle protocol (default) - less secure
    torch.save(model, 'model_full.pth')  # Contains code, not just weights

def load_user_provided_model(model_path):
    """Loading model from user-provided path without validation."""
    # No path validation - could lead to directory traversal
    if os.path.exists(model_path):
        model = torch.load(model_path)  # Vulnerable: user-controlled path
        return model
    return None

# Configuration issues
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Hardcoded paths and credentials
MODEL_STORAGE_PATH = "/home/user/models/"  # Hardcoded path
API_KEY = "sk-1234567890abcdef"  # Hardcoded API key for model serving

def main():
    """Main function with security issues."""
    
    # Create model
    model = VulnerableModel()
    
    # Unsafe operations
    unsafe_model = load_model_unsafe()
    url_model = load_model_from_url()
    pickle_model = load_with_pickle()
    
    # Unsafe inference
    user_data = torch.randn(1, 10)  # In real app, this comes from user
    prediction = model_inference_without_validation(model, user_data)
    
    # Unsafe saving
    save_model_insecurely(model)
    
    print(f"Prediction: {prediction}")
    print(f"API Key: {API_KEY}")  # Logging sensitive information

if __name__ == "__main__":
    main()
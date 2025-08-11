import os
import torch
import torchvision.transforms as transforms
from PIL import Image
from tqdm import tqdm

def load_png_to_tensor(img_path, img_size=128):
    """
    Load a .png file and transform it into a tensor.
    
    Args:
        img_path (str): Path to the .png image file
        img_size (int): Target size for resizing (default: 128)
    
    Returns:
        torch.Tensor: Image tensor with shape (3, img_size, img_size)
    """
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor()
    ])
    
    try:
        img = Image.open(img_path).convert('RGB') 
        img_tensor = transform(img)
        return img_tensor
    except Exception as e:
        print(f"Error loading image {img_path}: {e}")
        return torch.zeros((3, img_size, img_size), dtype=torch.float)

def load_img(dir_path, img_size=128):
    """
    Load all .png images from a directory.
    """
    image_dict = {}
    transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor()
    ])
    
    png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
    
    for filename in tqdm(png_files, desc="Loading Images"):
        
        drug_id = filename[:-4]  
        img_path = os.path.join(dir_path, filename)
        
        try:
            img = Image.open(img_path).convert('RGB')  
            img_tensor = transform(img)
            image_dict[drug_id] = img_tensor
        except Exception as e:
            print(f"Error loading image {filename}: {e}")
            image_dict[drug_id] = torch.zeros((3, img_size, img_size), dtype=torch.float)
    
    return image_dict

if __name__ == "__main__":
    # Example usage
    image_dict = load_img('molecules/images', img_size=128)
    print(f"Loaded {len(image_dict)} images.")
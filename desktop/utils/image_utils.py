"""
Image utilities for the StegnoX desktop application.
"""

from PIL import Image, ImageTk
import os
import io
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ImageUtils:
    """Utility class for image processing and visualization"""
    
    def __init__(self):
        """Initialize the image utilities"""
        pass
    
    def resize_image(self, image, max_size):
        """
        Resize an image to fit within max_size while preserving aspect ratio
        
        Args:
            image (PIL.Image): The image to resize
            max_size (tuple): Maximum (width, height)
            
        Returns:
            PIL.Image: Resized image
        """
        width, height = image.size
        
        # Calculate aspect ratio
        aspect_ratio = width / height
        
        # Calculate new dimensions
        if width > height:
            new_width = min(width, max_size[0])
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(height, max_size[1])
            new_width = int(new_height * aspect_ratio)
        
        # Ensure new dimensions don't exceed max_size
        if new_width > max_size[0]:
            new_width = max_size[0]
            new_height = int(new_width / aspect_ratio)
        
        if new_height > max_size[1]:
            new_height = max_size[1]
            new_width = int(new_height * aspect_ratio)
        
        # Resize the image
        return image.resize((new_width, new_height), Image.LANCZOS)
    
    def create_thumbnail(self, image_path, max_size=(100, 100)):
        """
        Create a thumbnail from an image file
        
        Args:
            image_path (str): Path to the image file
            max_size (tuple): Maximum (width, height) for the thumbnail
            
        Returns:
            PIL.ImageTk.PhotoImage: Thumbnail image for Tkinter
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Resize to thumbnail size
            thumbnail = self.resize_image(image, max_size)
            
            # Convert to PhotoImage
            return ImageTk.PhotoImage(thumbnail)
        except Exception as e:
            print(f"Error creating thumbnail: {str(e)}")
            return None
    
    def get_image_info(self, image_path):
        """
        Get information about an image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Image information
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Get basic information
            width, height = image.size
            format_name = image.format
            mode = image.mode
            file_size = os.path.getsize(image_path)
            
            # Get additional information
            info = {
                "width": width,
                "height": height,
                "format": format_name,
                "mode": mode,
                "file_size": file_size,
                "file_size_kb": file_size / 1024,
                "file_size_mb": file_size / (1024 * 1024),
                "aspect_ratio": width / height,
                "path": image_path,
                "filename": os.path.basename(image_path)
            }
            
            return info
        except Exception as e:
            print(f"Error getting image info: {str(e)}")
            return None
    
    def create_histogram_plot(self, image_path, parent_widget):
        """
        Create a histogram plot for an image
        
        Args:
            image_path (str): Path to the image file
            parent_widget (tk.Widget): Parent widget to place the plot
            
        Returns:
            matplotlib.backends.backend_tkagg.FigureCanvasTkAgg: Canvas with the plot
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Convert to RGB if needed
            if image.mode != "RGB":
                image = image.convert("RGB")
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Create figure and subplots
            fig, axs = plt.subplots(1, 3, figsize=(10, 4), tight_layout=True)
            
            # Plot histograms for each channel
            channels = ['Red', 'Green', 'Blue']
            colors = ['red', 'green', 'blue']
            
            for i, color in enumerate(colors):
                axs[i].hist(img_array[:, :, i].ravel(), bins=256, color=color, alpha=0.7)
                axs[i].set_title(channels[i])
                axs[i].set_xlim([0, 255])
                axs[i].set_yticks([])
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=parent_widget)
            canvas.draw()
            
            return canvas
        except Exception as e:
            print(f"Error creating histogram plot: {str(e)}")
            return None
    
    def create_bit_plane_visualization(self, image_path, parent_widget, bit_plane=0):
        """
        Create a visualization of a specific bit plane
        
        Args:
            image_path (str): Path to the image file
            parent_widget (tk.Widget): Parent widget to place the visualization
            bit_plane (int): Bit plane to visualize (0-7, where 0 is LSB)
            
        Returns:
            matplotlib.backends.backend_tkagg.FigureCanvasTkAgg: Canvas with the visualization
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Convert to grayscale
            if image.mode != "L":
                image = image.convert("L")
            
            # Convert to numpy array
            img_array = np.array(image)
            
            # Extract the bit plane
            bit_plane_img = (img_array >> bit_plane) & 1
            
            # Create figure
            fig, ax = plt.subplots(figsize=(6, 6), tight_layout=True)
            
            # Display the bit plane
            ax.imshow(bit_plane_img, cmap='gray')
            ax.set_title(f"Bit Plane {bit_plane}")
            ax.axis('off')
            
            # Create canvas
            canvas = FigureCanvasTkAgg(fig, master=parent_widget)
            canvas.draw()
            
            return canvas
        except Exception as e:
            print(f"Error creating bit plane visualization: {str(e)}")
            return None
    
    def extract_metadata(self, image_path):
        """
        Extract metadata from an image
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            dict: Image metadata
        """
        try:
            # Open the image
            image = Image.open(image_path)
            
            # Get metadata
            metadata = {
                "format": image.format,
                "mode": image.mode,
                "size": image.size,
                "info": image.info
            }
            
            return metadata
        except Exception as e:
            print(f"Error extracting metadata: {str(e)}")
            return None
    
    def save_image_with_metadata(self, image, output_path, metadata):
        """
        Save an image with custom metadata
        
        Args:
            image (PIL.Image): The image to save
            output_path (str): Path to save the image
            metadata (dict): Metadata to include
            
        Returns:
            bool: Success status
        """
        try:
            # Determine format from output path
            format_name = os.path.splitext(output_path)[1][1:].upper()
            if not format_name:
                format_name = image.format
            
            # Save with metadata
            image.save(output_path, format=format_name, **metadata)
            return True
        except Exception as e:
            print(f"Error saving image with metadata: {str(e)}")
            return False

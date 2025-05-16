"""
StegnoX Engine - Core steganography functionality
"""

import os
import numpy as np
from PIL import Image

class StegnoxEngine:
    """StegnoX Engine class for steganography operations."""

    def __init__(self):
        """Initialize the engine."""
        pass

    def analyze_image(self, image_path):
        """Analyze an image using all available methods."""
        results = {
            'lsb_extraction': self.lsb_extraction(image_path),
            'parity_bit_extraction': self.parity_bit_extraction(image_path),
            'metadata_extraction': self.metadata_extraction(image_path)
        }
        return results

    def lsb_extraction(self, image_path):
        """Extract message using LSB method."""
        try:
            img = Image.open(image_path)
            pixels = np.array(img)
            lsb = pixels & 1
            return {
                'success': True,
                'data': lsb.tobytes().hex()[:100]  # Return first 100 chars for preview
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def parity_bit_extraction(self, image_path):
        """Extract message using parity bit method."""
        try:
            img = Image.open(image_path)
            pixels = np.array(img)
            parity = np.sum(pixels & 1, axis=2) % 2
            return {
                'success': True,
                'data': parity.tobytes().hex()[:100]  # Return first 100 chars for preview
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def metadata_extraction(self, image_path):
        """Extract metadata from image."""
        try:
            img = Image.open(image_path)
            return {
                'success': True,
                'data': {
                    'format': img.format,
                    'mode': img.mode,
                    'size': img.size,
                    'info': img.info
                }
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

    def encode_message(self, input_path, output_path, message, method='lsb_encoding'):
        """Encode a message in an image."""
        try:
            if method == 'lsb_encoding':
                return self.lsb_encoding(input_path, output_path, message)
            elif method == 'parity_encoding':
                return self.parity_encoding(input_path, output_path, message)
            elif method == 'metadata_encoding':
                return self.metadata_encoding(input_path, output_path, message)
            else:
                return False
        except Exception:
            return False

    def lsb_encoding(self, input_path, output_path, message):
        """Encode message using LSB method."""
        try:
            img = Image.open(input_path)
            pixels = np.array(img)
            
            # Convert message to binary
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            binary_message += '00000000'  # Add null terminator
            
            # Ensure image has enough capacity
            if len(binary_message) > pixels.size:
                return False
            
            # Modify LSBs
            for i, bit in enumerate(binary_message):
                if i >= pixels.size:
                    break
                x = (i // 3) // pixels.shape[1]
                y = (i // 3) % pixels.shape[1]
                c = i % 3
                pixels[x, y, c] = (pixels[x, y, c] & ~1) | int(bit)
            
            # Save image
            Image.fromarray(pixels).save(output_path)
            return True
        except Exception:
            return False

    def parity_encoding(self, input_path, output_path, message):
        """Encode message using parity bit method."""
        try:
            img = Image.open(input_path)
            pixels = np.array(img)
            
            # Convert message to binary
            binary_message = ''.join(format(ord(c), '08b') for c in message)
            binary_message += '00000000'  # Add null terminator
            
            # Ensure image has enough capacity
            if len(binary_message) > pixels.shape[0] * pixels.shape[1]:
                return False
            
            # Modify pixels to match desired parity
            for i, bit in enumerate(binary_message):
                if i >= pixels.shape[0] * pixels.shape[1]:
                    break
                x = i // pixels.shape[1]
                y = i % pixels.shape[1]
                current_parity = np.sum(pixels[x, y]) % 2
                if current_parity != int(bit):
                    pixels[x, y, 0] ^= 1
            
            # Save image
            Image.fromarray(pixels).save(output_path)
            return True
        except Exception:
            return False

    def metadata_encoding(self, input_path, output_path, message):
        """Encode message in image metadata."""
        try:
            img = Image.open(input_path)
            img.info['steganography'] = message
            img.save(output_path, pnginfo=img.info.get('pnginfo'))
            return True
        except Exception:
            return False 
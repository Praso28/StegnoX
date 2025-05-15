from PIL import Image
import numpy as np
import base64
import io
import cv2
from scipy.fftpack import dct, idct
import matplotlib.pyplot as plt
from io import BytesIO

class StegnoxEngine:
    def __init__(self):
        self.methods = [
            self.lsb_extraction,
            self.parity_bit_extraction,
            self.metadata_extraction,
            self.dct_analysis,
            self.bit_plane_analysis,
            self.histogram_analysis
        ]

    def extract_all_methods(self, image_path):
        """Run all extraction methods on the image"""
        results = {}

        for method in self.methods:
            try:
                method_name = method.__name__
                result = method(image_path)
                results[method_name] = result
            except Exception as e:
                results[method_name] = {"error": str(e)}

        return results

    def lsb_extraction(self, image_path):
        """Extract data using LSB method (from original code)"""
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size

        binary_message = ""
        pixels = img.load()
        terminator = ''.join(format(ord('#'), '08b') * 4)

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                binary_message += str(r & 1)
                binary_message += str(g & 1)
                binary_message += str(b & 1)

                if terminator in binary_message:
                    binary_message = binary_message[:binary_message.index(terminator)]
                    break
            else:
                continue
            break

        if len(binary_message) % 8 != 0:
            return {"message": "No valid data found"}

        try:
            message_bytes = bytes(int(binary_message[i:i+8], 2) for i in range(0, len(binary_message), 8))
            return {"message": message_bytes.decode('utf-8', errors='replace')}
        except:
            return {"message": "Binary data found but not decodable as text"}

    def parity_bit_extraction(self, image_path):
        """Extract data using parity bit method"""
        img = Image.open(image_path)
        img = img.convert("RGB")
        width, height = img.size

        binary_data = ""
        pixels = img.load()

        for y in range(height):
            for x in range(width):
                r, g, b = pixels[x, y]
                # Check parity of each color channel
                binary_data += str((r + g + b) % 2)

        # Try to interpret as ASCII
        try:
            chunks = [binary_data[i:i+8] for i in range(0, min(len(binary_data), 1000), 8)]
            ascii_text = ''.join(chr(int(chunk, 2)) for chunk in chunks if len(chunk) == 8)
            return {"message": ascii_text}
        except:
            return {"message": "No readable text found with parity method"}

    def metadata_extraction(self, image_path):
        """Extract metadata from the image"""
        img = Image.open(image_path)
        metadata = {}

        # Extract basic metadata
        metadata["format"] = img.format
        metadata["mode"] = img.mode
        metadata["size"] = img.size

        # Extract EXIF data if available
        if hasattr(img, '_getexif') and img._getexif():
            exif = {
                str(k): str(v) for k, v in img._getexif().items()
                if isinstance(v, (str, int, float, bytes))
            }
            metadata["exif"] = exif

        return metadata

    def dct_analysis(self, image_path):
        """
        Analyze DCT coefficients for signs of steganography

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Analysis results with confidence score and assessment
        """
        try:
            # Read image using OpenCV
            img = cv2.imread(image_path)
            if img is None:
                return {
                    "error": "Could not read image with OpenCV",
                    "confidence": 0,
                    "assessment": "Failed",
                    "statistics": {
                        "zero_count": 0,
                        "nonzero_count": 0,
                        "suspicious_blocks": 0,
                        "total_blocks": 0
                    }
                }

            # Convert to grayscale for simplicity
            try:
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            except Exception as e:
                return {
                    "error": f"Failed to convert image to grayscale: {str(e)}",
                    "confidence": 0,
                    "assessment": "Failed",
                    "statistics": {
                        "zero_count": 0,
                        "nonzero_count": 0,
                        "suspicious_blocks": 0,
                        "total_blocks": 0
                    }
                }

            # Divide the image into 8x8 blocks (standard for DCT)
            h, w = gray.shape
            block_size = 8

            # Store coefficient statistics
            dct_stats = {
                "zero_count": 0,
                "nonzero_count": 0,
                "suspicious_blocks": 0,
                "total_blocks": 0
            }

            # Process each 8x8 block
            for y in range(0, h-block_size+1, block_size):
                for x in range(0, w-block_size+1, block_size):
                    try:
                        # Extract block
                        block = gray[y:y+block_size, x:x+block_size].astype(float)

                        # Apply DCT
                        block_dct = dct(dct(block.T, norm='ortho').T, norm='ortho')

                        # Count zero and non-zero coefficients
                        zero_coeffs = np.count_nonzero(block_dct == 0)
                        nonzero_coeffs = block_size * block_size - zero_coeffs

                        dct_stats["zero_count"] += zero_coeffs
                        dct_stats["nonzero_count"] += nonzero_coeffs
                        dct_stats["total_blocks"] += 1

                        # Check for suspicious patterns
                        odd_coeffs = np.count_nonzero(np.abs(block_dct) % 2 > 0.5)
                        if odd_coeffs > (block_size * block_size * 0.7):
                            dct_stats["suspicious_blocks"] += 1
                    except Exception as e:
                        # Skip problematic blocks but continue processing
                        continue

            # Calculate confidence score
            if dct_stats["total_blocks"] > 0:
                confidence = (dct_stats["suspicious_blocks"] / dct_stats["total_blocks"]) * 100
            else:
                confidence = 0

            return {
                "statistics": dct_stats,
                "confidence": confidence,
                "assessment": "Suspicious" if confidence > 30 else "Likely clean",
                "message": f"DCT analysis complete. Confidence that steganography is present: {confidence:.2f}%"
            }

        except Exception as e:
            return {
                "error": f"DCT analysis failed: {str(e)}",
                "confidence": 0,
                "assessment": "Failed",
                "statistics": {
                    "zero_count": 0,
                    "nonzero_count": 0,
                    "suspicious_blocks": 0,
                    "total_blocks": 0
                }
            }

    def bit_plane_analysis(self, image_path):
        """
        Analyze bit planes for signs of steganography

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Analysis results with bit plane data
        """
        try:
            # Open image with PIL
            img = Image.open(image_path)
            img = img.convert("RGB")

            # Convert to numpy array
            img_array = np.array(img)

            # Extract channels
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]

            # Analyze each bit plane
            results = {}
            suspicious_planes = 0

            # Function to analyze a single bit plane
            def analyze_bit_plane(channel, bit_position):
                # Extract the bit plane
                bit_plane = (channel >> bit_position) & 1

                # Calculate statistics
                ones = np.count_nonzero(bit_plane)
                zeros = bit_plane.size - ones

                # Calculate entropy (randomness)
                # More random bit planes might indicate hidden data
                p_ones = ones / bit_plane.size
                p_zeros = zeros / bit_plane.size

                entropy = 0
                if p_ones > 0:
                    entropy -= p_ones * np.log2(p_ones)
                if p_zeros > 0:
                    entropy -= p_zeros * np.log2(p_zeros)

                # Check for suspicious patterns
                # High entropy in lower bit planes can indicate steganography
                is_suspicious = False
                if bit_position == 0 and entropy > 0.95:  # LSB with high entropy
                    is_suspicious = True

                return {
                    "ones": ones,
                    "zeros": zeros,
                    "entropy": entropy,
                    "suspicious": is_suspicious
                }

            # Analyze each bit plane for each channel
            for bit in range(8):  # 8 bits per channel
                r_analysis = analyze_bit_plane(r_channel, bit)
                g_analysis = analyze_bit_plane(g_channel, bit)
                b_analysis = analyze_bit_plane(b_channel, bit)

                results[f"bit_{bit}"] = {
                    "red": r_analysis,
                    "green": g_analysis,
                    "blue": b_analysis
                }

                if r_analysis["suspicious"] or g_analysis["suspicious"] or b_analysis["suspicious"]:
                    suspicious_planes += 1

            # Calculate overall confidence
            confidence = (suspicious_planes / 24) * 100  # 24 bit planes total (8 per channel)

            return {
                "bit_planes": results,
                "suspicious_planes": suspicious_planes,
                "confidence": confidence,
                "assessment": "Suspicious" if confidence > 20 else "Likely clean",
                "message": f"Bit plane analysis complete. Confidence that steganography is present: {confidence:.2f}%"
            }

        except Exception as e:
            return {"error": f"Bit plane analysis failed: {str(e)}"}

    def histogram_analysis(self, image_path):
        """
        Analyze image histograms for signs of steganography

        Args:
            image_path (str): Path to the image file

        Returns:
            dict: Analysis results with histogram data
        """
        try:
            # Open image with PIL
            img = Image.open(image_path)
            img = img.convert("RGB")

            # Convert to numpy array
            img_array = np.array(img)

            # Extract channels
            r_channel = img_array[:, :, 0]
            g_channel = img_array[:, :, 1]
            b_channel = img_array[:, :, 2]

            # Calculate histograms
            r_hist, _ = np.histogram(r_channel, bins=256, range=(0, 256))
            g_hist, _ = np.histogram(g_channel, bins=256, range=(0, 256))
            b_hist, _ = np.histogram(b_channel, bins=256, range=(0, 256))

            # Analyze histograms for signs of steganography
            # One approach: check for "pair-wise" patterns in LSB steganography
            # In LSB steganography, pairs of values (2n, 2n+1) tend to be equalized

            def analyze_histogram(hist):
                pairs_count = 0
                suspicious_pairs = 0

                for i in range(0, 256, 2):
                    even_val = hist[i]
                    odd_val = hist[i+1]

                    pairs_count += 1

                    # If the values are very close, it might indicate LSB manipulation
                    if abs(even_val - odd_val) < (even_val + odd_val) * 0.05:  # Within 5%
                        suspicious_pairs += 1

                return {
                    "total_pairs": pairs_count,
                    "suspicious_pairs": suspicious_pairs,
                    "suspicion_ratio": suspicious_pairs / pairs_count if pairs_count > 0 else 0
                }

            r_analysis = analyze_histogram(r_hist)
            g_analysis = analyze_histogram(g_hist)
            b_analysis = analyze_histogram(b_hist)

            # Calculate overall confidence
            avg_suspicion = (r_analysis["suspicion_ratio"] +
                            g_analysis["suspicion_ratio"] +
                            b_analysis["suspicion_ratio"]) / 3

            confidence = avg_suspicion * 100

            # Generate histogram visualization
            # This would normally save the visualization, but we'll just return the data

            return {
                "red_channel": r_analysis,
                "green_channel": g_analysis,
                "blue_channel": b_analysis,
                "confidence": confidence,
                "assessment": "Suspicious" if confidence > 40 else "Likely clean",
                "message": f"Histogram analysis complete. Confidence that steganography is present: {confidence:.2f}%"
            }

        except Exception as e:
            return {"error": f"Histogram analysis failed: {str(e)}"}

    def detect_format(self, image_path):
        """
        Detect the format of an image file

        Args:
            image_path (str): Path to the image file

        Returns:
            str: Detected format
        """
        try:
            with Image.open(image_path) as img:
                return img.format.lower()
        except Exception as e:
            return f"Unknown format: {str(e)}"

    def lsb_encoding(self, image_path, message, output_path):
        """
        Encode a message using LSB steganography

        Args:
            image_path (str): Path to the cover image
            message (str): Message to hide
            output_path (str): Path to save the resulting image

        Returns:
            bool: Success status
        """
        try:
            # Open the image
            img = Image.open(image_path)
            img = img.convert("RGB")
            width, height = img.size

            # Add terminator to the message
            message_bytes = message.encode() + b"####"
            binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
            message_len = len(binary_message)

            # Check if the image is large enough to hold the message
            if message_len > width * height * 3:
                return {
                    "success": False,
                    "error": "Message is too long to hide in this image."
                }

            # Get pixel data
            pixels = img.load()
            index = 0

            # Embed the message
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]

                    # Modify the least significant bit of each color channel
                    if index < message_len:
                        r = (r & 0xFE) | int(binary_message[index])
                        index += 1
                    if index < message_len:
                        g = (g & 0xFE) | int(binary_message[index])
                        index += 1
                    if index < message_len:
                        b = (b & 0xFE) | int(binary_message[index])
                        index += 1

                    pixels[x, y] = (r, g, b)

                    if index >= message_len:
                        break

                if index >= message_len:
                    break

            # Save the image
            img.save(output_path, "PNG")

            return {
                "success": True,
                "message": f"Message successfully hidden in {output_path}",
                "bits_used": message_len,
                "capacity": width * height * 3
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"LSB encoding failed: {str(e)}"
            }

    def parity_bit_encoding(self, image_path, message, output_path):
        """
        Encode a message using parity bit steganography

        Args:
            image_path (str): Path to the cover image
            message (str): Message to hide
            output_path (str): Path to save the resulting image

        Returns:
            bool: Success status
        """
        try:
            # Open the image
            img = Image.open(image_path)
            img = img.convert("RGB")
            width, height = img.size

            # Convert message to binary
            message_bytes = message.encode() + b"####"
            binary_message = ''.join(format(byte, '08b') for byte in message_bytes)
            message_len = len(binary_message)

            # Check if the image is large enough to hold the message
            if message_len > width * height:
                return {
                    "success": False,
                    "error": "Message is too long to hide in this image."
                }

            # Get pixel data
            pixels = img.load()
            index = 0

            # Embed the message using parity
            for y in range(height):
                for x in range(width):
                    if index < message_len:
                        r, g, b = pixels[x, y]

                        # Calculate current parity
                        current_parity = (r + g + b) % 2

                        # Desired parity based on message bit
                        desired_parity = int(binary_message[index])

                        # If parity doesn't match, adjust one of the channels
                        if current_parity != desired_parity:
                            # Modify the blue channel (least visually noticeable)
                            if b > 0:
                                b -= 1
                            else:
                                b += 1

                        pixels[x, y] = (r, g, b)
                        index += 1

                    if index >= message_len:
                        break

                if index >= message_len:
                    break

            # Save the image
            img.save(output_path, "PNG")

            return {
                "success": True,
                "message": f"Message successfully hidden in {output_path} using parity encoding",
                "bits_used": message_len,
                "capacity": width * height
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Parity bit encoding failed: {str(e)}"
            }

    def metadata_encoding(self, image_path, message, output_path):
        """
        Hide a message in image metadata

        Args:
            image_path (str): Path to the cover image
            message (str): Message to hide
            output_path (str): Path to save the resulting image

        Returns:
            dict: Result information
        """
        try:
            # Open the image
            img = Image.open(image_path)

            # Create a new image with the same content
            metadata = img.info.copy()

            # Add our message to the metadata
            metadata["comment"] = message

            # Save the image with the new metadata
            img.save(output_path, format=img.format, **metadata)

            return {
                "success": True,
                "message": f"Message successfully hidden in metadata of {output_path}",
                "metadata_key": "comment"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"Metadata encoding failed: {str(e)}"
            }

"""
Export utilities for the StegnoX desktop application.
"""

import os
import json
import csv
import xml.dom.minidom
import yaml
import zipfile
import io
from PIL import Image

class ExportUtils:
    """Utility class for exporting data in various formats"""
    
    @staticmethod
    def export_to_json(data, file_path):
        """
        Export data to JSON format
        
        Args:
            data: The data to export
            file_path: The output file path
            
        Returns:
            bool: Success status
        """
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting to JSON: {str(e)}")
            return False
    
    @staticmethod
    def export_to_csv(data, file_path, headers=None):
        """
        Export data to CSV format
        
        Args:
            data: The data to export (list of dictionaries or list of lists)
            file_path: The output file path
            headers: Optional list of column headers
            
        Returns:
            bool: Success status
        """
        try:
            with open(file_path, 'w', newline='') as f:
                if isinstance(data[0], dict):
                    # Data is a list of dictionaries
                    if headers is None:
                        headers = data[0].keys()
                    
                    writer = csv.DictWriter(f, fieldnames=headers)
                    writer.writeheader()
                    writer.writerows(data)
                else:
                    # Data is a list of lists
                    writer = csv.writer(f)
                    if headers:
                        writer.writerow(headers)
                    writer.writerows(data)
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {str(e)}")
            return False
    
    @staticmethod
    def export_to_xml(data, file_path, root_element='data', item_element='item'):
        """
        Export data to XML format
        
        Args:
            data: The data to export
            file_path: The output file path
            root_element: The name of the root XML element
            item_element: The name of the item XML element
            
        Returns:
            bool: Success status
        """
        try:
            # Create XML document
            doc = xml.dom.minidom.getDOMImplementation().createDocument(None, root_element, None)
            root = doc.documentElement
            
            # Helper function to create elements from data
            def create_element(parent, name, value):
                if isinstance(value, dict):
                    # Create a new element for the dictionary
                    elem = doc.createElement(name)
                    parent.appendChild(elem)
                    
                    # Add dictionary items as child elements
                    for k, v in value.items():
                        create_element(elem, k, v)
                elif isinstance(value, list):
                    # Create a new element for the list
                    elem = doc.createElement(name)
                    parent.appendChild(elem)
                    
                    # Add list items as child elements
                    for i, item in enumerate(value):
                        create_element(elem, item_element, item)
                else:
                    # Create a simple element with text content
                    elem = doc.createElement(name)
                    parent.appendChild(elem)
                    
                    # Add text content
                    if value is not None:
                        text = doc.createTextNode(str(value))
                        elem.appendChild(text)
            
            # Process the data
            if isinstance(data, dict):
                # Add dictionary items as child elements of root
                for key, value in data.items():
                    create_element(root, key, value)
            elif isinstance(data, list):
                # Add list items as child elements of root
                for item in data:
                    create_element(root, item_element, item)
            
            # Write to file
            with open(file_path, 'w') as f:
                f.write(doc.toprettyxml(indent='  '))
            
            return True
        except Exception as e:
            print(f"Error exporting to XML: {str(e)}")
            return False
    
    @staticmethod
    def export_to_yaml(data, file_path):
        """
        Export data to YAML format
        
        Args:
            data: The data to export
            file_path: The output file path
            
        Returns:
            bool: Success status
        """
        try:
            with open(file_path, 'w') as f:
                yaml.dump(data, f, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Error exporting to YAML: {str(e)}")
            return False
    
    @staticmethod
    def export_to_text(data, file_path):
        """
        Export data to plain text format
        
        Args:
            data: The data to export
            file_path: The output file path
            
        Returns:
            bool: Success status
        """
        try:
            with open(file_path, 'w') as f:
                if isinstance(data, str):
                    f.write(data)
                elif isinstance(data, dict):
                    for key, value in data.items():
                        f.write(f"{key}: {value}\n")
                elif isinstance(data, list):
                    for item in data:
                        f.write(f"{item}\n")
                else:
                    f.write(str(data))
            return True
        except Exception as e:
            print(f"Error exporting to text: {str(e)}")
            return False
    
    @staticmethod
    def export_to_zip(files, file_path):
        """
        Export multiple files to a ZIP archive
        
        Args:
            files: Dictionary of {filename: content} or list of file paths
            file_path: The output ZIP file path
            
        Returns:
            bool: Success status
        """
        try:
            with zipfile.ZipFile(file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if isinstance(files, dict):
                    # Dictionary of {filename: content}
                    for filename, content in files.items():
                        if isinstance(content, str):
                            # Text content
                            zipf.writestr(filename, content)
                        elif isinstance(content, bytes):
                            # Binary content
                            zipf.writestr(filename, content)
                        elif isinstance(content, Image.Image):
                            # PIL Image
                            img_bytes = io.BytesIO()
                            content.save(img_bytes, format=content.format or 'PNG')
                            zipf.writestr(filename, img_bytes.getvalue())
                        else:
                            # Other content, convert to string
                            zipf.writestr(filename, str(content))
                else:
                    # List of file paths
                    for file_path in files:
                        if os.path.exists(file_path):
                            zipf.write(file_path, os.path.basename(file_path))
            return True
        except Exception as e:
            print(f"Error exporting to ZIP: {str(e)}")
            return False
    
    @staticmethod
    def export_image(image, file_path, format=None):
        """
        Export an image to a file
        
        Args:
            image: PIL Image object
            file_path: The output file path
            format: Optional image format (PNG, JPEG, etc.)
            
        Returns:
            bool: Success status
        """
        try:
            # Determine format from file extension if not specified
            if format is None:
                format = os.path.splitext(file_path)[1][1:].upper()
                if not format:
                    format = 'PNG'
            
            # Save the image
            image.save(file_path, format=format)
            return True
        except Exception as e:
            print(f"Error exporting image: {str(e)}")
            return False
    
    @staticmethod
    def export_results(results, file_path, format='json'):
        """
        Export analysis results to a file
        
        Args:
            results: The analysis results
            file_path: The output file path
            format: The output format ('json', 'csv', 'xml', 'yaml', 'text')
            
        Returns:
            bool: Success status
        """
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
            
            # Export based on format
            if format.lower() == 'json':
                return ExportUtils.export_to_json(results, file_path)
            elif format.lower() == 'csv':
                return ExportUtils.export_to_csv(results, file_path)
            elif format.lower() == 'xml':
                return ExportUtils.export_to_xml(results, file_path)
            elif format.lower() == 'yaml':
                return ExportUtils.export_to_yaml(results, file_path)
            elif format.lower() == 'text':
                return ExportUtils.export_to_text(results, file_path)
            else:
                raise ValueError(f"Unsupported export format: {format}")
        except Exception as e:
            print(f"Error exporting results: {str(e)}")
            return False

"""
StegnoX Engine Demo

This script demonstrates the usage of the enhanced StegnoX engine.
"""

import os
import sys
import argparse
from PIL import Image

# Add parent directory to path to allow imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine.stegnox_engine import StegnoxEngine

def main():
    parser = argparse.ArgumentParser(description="StegnoX Engine Demo")
    parser.add_argument("--action", choices=["analyze", "encode", "decode"], required=True,
                        help="Action to perform: analyze, encode, or decode")
    parser.add_argument("--image", required=True, help="Path to the image file")
    parser.add_argument("--method", choices=["lsb", "parity", "metadata"], 
                        help="Method for encoding/decoding (required for encode/decode)")
    parser.add_argument("--message", help="Message to encode (required for encode)")
    parser.add_argument("--output", help="Output file path (required for encode)")
    
    args = parser.parse_args()
    
    engine = StegnoxEngine()
    
    if args.action == "analyze":
        print(f"Analyzing image: {args.image}")
        results = engine.extract_all_methods(args.image)
        
        # Print results in a readable format
        for method_name, result in results.items():
            print(f"\n=== {method_name} ===")
            if isinstance(result, dict):
                for key, value in result.items():
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for subkey, subvalue in value.items():
                            print(f"    {subkey}: {subvalue}")
                    else:
                        print(f"  {key}: {value}")
            else:
                print(f"  {result}")
    
    elif args.action == "encode":
        if not args.method:
            print("Error: --method is required for encode action")
            return
        if not args.message:
            print("Error: --message is required for encode action")
            return
        if not args.output:
            print("Error: --output is required for encode action")
            return
        
        print(f"Encoding message using {args.method} method")
        
        if args.method == "lsb":
            result = engine.lsb_encoding(args.image, args.message, args.output)
        elif args.method == "parity":
            result = engine.parity_bit_encoding(args.image, args.message, args.output)
        elif args.method == "metadata":
            result = engine.metadata_encoding(args.image, args.message, args.output)
        
        if result["success"]:
            print(f"Success: {result['message']}")
        else:
            print(f"Error: {result['error']}")
    
    elif args.action == "decode":
        if not args.method:
            print("Error: --method is required for decode action")
            return
        
        print(f"Decoding message using {args.method} method")
        
        if args.method == "lsb":
            result = engine.lsb_extraction(args.image)
        elif args.method == "parity":
            result = engine.parity_bit_extraction(args.image)
        elif args.method == "metadata":
            result = engine.metadata_extraction(args.image)
        
        if "message" in result:
            print(f"Decoded message: {result['message']}")
        else:
            print("No message found or error occurred")
            print(result)

if __name__ == "__main__":
    main()

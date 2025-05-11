#!/usr/bin/env python
"""
Build script for StegnoX desktop application

This script builds the StegnoX desktop application for Windows, macOS, and Linux.
"""

import os
import sys
import shutil
import subprocess
import platform
import argparse
from datetime import datetime

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Build StegnoX desktop application')
    parser.add_argument('--platform', choices=['all', 'windows', 'macos', 'linux'], default='all',
                        help='Platform to build for')
    parser.add_argument('--version', default=None, help='Version number (default: YYYY.MM.DD)')
    parser.add_argument('--clean', action='store_true', help='Clean build directory before building')
    return parser.parse_args()

def clean_build_dir():
    """Clean the build directory"""
    print("Cleaning build directory...")
    if os.path.exists('build'):
        shutil.rmtree('build')
    if os.path.exists('dist'):
        shutil.rmtree('dist')

def get_version(args_version):
    """Get the version number"""
    if args_version:
        return args_version
    
    # Use date-based version if not specified
    now = datetime.now()
    return f"{now.year}.{now.month}.{now.day}"

def build_windows(version):
    """Build Windows installer"""
    print(f"Building Windows installer (version {version})...")
    
    # Create setup.py for py2exe
    with open('setup_win.py', 'w') as f:
        f.write(f"""
from setuptools import setup
import py2exe

setup(
    name="StegnoX",
    version="{version}",
    description="Advanced Steganography Analysis Tool",
    author="StegnoX Team",
    options={{
        'py2exe': {{
            'bundle_files': 1,
            'compressed': True,
            'includes': ['tkinter', 'PIL', 'numpy', 'scipy', 'cv2'],
        }}
    }},
    windows=[{{'script': 'main.py', 'icon_resources': [(1, 'assets/icon.ico')], 'dest_base': 'StegnoX'}}],
    zipfile=None,
)
""")
    
    # Run py2exe
    subprocess.run([sys.executable, 'setup_win.py', 'py2exe'], check=True)
    
    # Create installer with NSIS
    # This requires NSIS to be installed
    nsis_script = f"""
!define PRODUCT_NAME "StegnoX"
!define PRODUCT_VERSION "{version}"
!define PRODUCT_PUBLISHER "StegnoX Team"
!define PRODUCT_WEB_SITE "https://stegnox.com"
!define PRODUCT_DIR_REGKEY "Software\\Microsoft\\Windows\\CurrentVersion\\App Paths\\StegnoX.exe"
!define PRODUCT_UNINST_KEY "Software\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\${{PRODUCT_NAME}}"

SetCompressor lzma
Name "${{PRODUCT_NAME}} ${{PRODUCT_VERSION}}"
OutFile "dist\\StegnoX-${{PRODUCT_VERSION}}-setup.exe"
InstallDir "$PROGRAMFILES\\StegnoX"
InstallDirRegKey HKLM "${{PRODUCT_DIR_REGKEY}}" ""

Section "MainSection" SEC01
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
  File /r "dist\\*.*"
  CreateDirectory "$SMPROGRAMS\\StegnoX"
  CreateShortCut "$SMPROGRAMS\\StegnoX\\StegnoX.lnk" "$INSTDIR\\StegnoX.exe"
  CreateShortCut "$DESKTOP\\StegnoX.lnk" "$INSTDIR\\StegnoX.exe"
SectionEnd

Section -Post
  WriteUninstaller "$INSTDIR\\uninstall.exe"
  WriteRegStr HKLM "${{PRODUCT_DIR_REGKEY}}" "" "$INSTDIR\\StegnoX.exe"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "DisplayName" "$(^Name)"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "UninstallString" "$INSTDIR\\uninstall.exe"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "DisplayIcon" "$INSTDIR\\StegnoX.exe"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "DisplayVersion" "${{PRODUCT_VERSION}}"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "URLInfoAbout" "${{PRODUCT_WEB_SITE}}"
  WriteRegStr HKLM "${{PRODUCT_UNINST_KEY}}" "Publisher" "${{PRODUCT_PUBLISHER}}"
SectionEnd
"""
    
    with open('installer.nsi', 'w') as f:
        f.write(nsis_script)
    
    # Run NSIS
    try:
        subprocess.run(['makensis', 'installer.nsi'], check=True)
        print(f"Windows installer created: dist/StegnoX-{version}-setup.exe")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("NSIS not found. Please install NSIS to create the Windows installer.")
        print("Windows build files are available in the 'dist' directory.")

def build_macos(version):
    """Build macOS application"""
    print(f"Building macOS application (version {version})...")
    
    # Create setup.py for py2app
    with open('setup_mac.py', 'w') as f:
        f.write(f"""
from setuptools import setup

APP = ['main.py']
DATA_FILES = ['assets']
OPTIONS = {{
    'argv_emulation': True,
    'iconfile': 'assets/icon.icns',
    'plist': {{
        'CFBundleName': 'StegnoX',
        'CFBundleDisplayName': 'StegnoX',
        'CFBundleVersion': '{version}',
        'CFBundleShortVersionString': '{version}',
        'CFBundleIdentifier': 'com.stegnox.app',
        'NSHumanReadableCopyright': '© StegnoX Team',
        'NSHighResolutionCapable': True,
    }},
    'packages': ['tkinter', 'PIL', 'numpy', 'scipy', 'cv2', 'engine', 'storage', 'queue'],
}}

setup(
    name='StegnoX',
    app=APP,
    data_files=DATA_FILES,
    options={{'py2app': OPTIONS}},
    setup_requires=['py2app'],
)
""")
    
    # Run py2app
    subprocess.run([sys.executable, 'setup_mac.py', 'py2app'], check=True)
    
    # Create DMG
    try:
        subprocess.run([
            'hdiutil', 'create', 
            f'dist/StegnoX-{version}.dmg',
            '-srcfolder', 'dist/StegnoX.app',
            '-ov', '-volname', f'StegnoX {version}'
        ], check=True)
        print(f"macOS DMG created: dist/StegnoX-{version}.dmg")
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Could not create DMG. macOS application is available at dist/StegnoX.app")

def build_linux(version):
    """Build Linux package"""
    print(f"Building Linux package (version {version})...")
    
    # Create setup.py for bdist_rpm
    with open('setup_linux.py', 'w') as f:
        f.write(f"""
from setuptools import setup

setup(
    name='stegnox',
    version='{version}',
    description='Advanced Steganography Analysis Tool',
    author='StegnoX Team',
    author_email='info@stegnox.com',
    url='https://stegnox.com',
    packages=['engine', 'storage', 'queue', 'desktop'],
    scripts=['main.py'],
    data_files=[
        ('share/applications', ['stegnox.desktop']),
        ('share/pixmaps', ['assets/icon.png']),
    ],
)
""")
    
    # Create desktop file
    with open('stegnox.desktop', 'w') as f:
        f.write(f"""
[Desktop Entry]
Name=StegnoX
Comment=Advanced Steganography Analysis Tool
Exec=stegnox
Icon=stegnox
Terminal=false
Type=Application
Categories=Graphics;Security;
""")
    
    # Run bdist_rpm
    try:
        subprocess.run([sys.executable, 'setup_linux.py', 'bdist_rpm'], check=True)
        print(f"Linux RPM package created in dist/ directory")
    except subprocess.SubprocessError:
        print("Could not create RPM package. Try installing rpm-build package.")
    
    # Create DEB package
    try:
        subprocess.run([sys.executable, 'setup_linux.py', 'bdist_deb'], check=True)
        print(f"Linux DEB package created in dist/ directory")
    except subprocess.SubprocessError:
        print("Could not create DEB package. Try installing python3-stdeb package.")

def main():
    """Main function"""
    args = parse_args()
    version = get_version(args.version)
    
    print(f"Building StegnoX desktop application version {version}")
    
    if args.clean:
        clean_build_dir()
    
    # Create build directory
    os.makedirs('dist', exist_ok=True)
    
    # Build for selected platform(s)
    if args.platform in ['all', 'windows']:
        if platform.system() == 'Windows' or args.platform == 'windows':
            build_windows(version)
        else:
            print("Skipping Windows build (not on Windows)")
    
    if args.platform in ['all', 'macos']:
        if platform.system() == 'Darwin' or args.platform == 'macos':
            build_macos(version)
        else:
            print("Skipping macOS build (not on macOS)")
    
    if args.platform in ['all', 'linux']:
        if platform.system() == 'Linux' or args.platform == 'linux':
            build_linux(version)
        else:
            print("Skipping Linux build (not on Linux)")
    
    print("Build completed!")

if __name__ == '__main__':
    main()

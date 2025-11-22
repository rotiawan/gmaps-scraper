"""
Setup script untuk Google Maps Lead Scraper Package
====================================================

Untuk install package:
    pip install .

Untuk install dalam development mode:
    pip install -e .

Untuk build distribution:
    python setup.py sdist bdist_wheel

Author: rotiawan
Date: 2025-11-22
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README untuk long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements dari requirements.txt
requirements_file = Path(__file__).parent / "gmaps_scraper" / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, 'r', encoding='utf-8') as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith('#')
        ]

setup(
    # === PACKAGE METADATA ===
    name="gmaps-lead-scraper",
    version="18.0.0",
    author="rotiawan",
    author_email="your.email@example.com",  # Update dengan email asli
    description="Professional lead generation tool from Google Maps with email extraction",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rotiawan/gmaps-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/rotiawan/gmaps-scraper/issues",
        "Documentation": "https://github.com/rotiawan/gmaps-scraper#readme",
        "Source Code": "https://github.com/rotiawan/gmaps-scraper",
    },
    
    # === PACKAGE CONFIGURATION ===
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.7",
    install_requires=requirements,
    
    # === CLASSIFIERS ===
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Developers",
        "Intended Audience :: Business",
        
        # Topic
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Python Versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        
        # Operating System
        "Operating System :: OS Independent",
    ],
    
    # === ENTRY POINTS ===
    entry_points={
        "console_scripts": [
            "gmaps-scraper=gmaps_scraper.gmaps_scraper:main",
        ],
    },
    
    # === KEYWORDS ===
    keywords=[
        "google maps",
        "web scraping",
        "lead generation",
        "selenium",
        "email extraction",
        "business data",
        "data mining"
    ],
    
    # === PACKAGE DATA ===
    include_package_data=True,
    package_data={
        "gmaps_scraper": [
            "requirements.txt",
            "*.md"
        ],
    },
    
    # === ZIP SAFE ===
    zip_safe=False,
)


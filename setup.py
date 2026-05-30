#!/usr/bin/env python3
"""
0xRecon Setup Script
Advanced OSINT Framework by 0xCosmix
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="0xrecon",
    version="3.0.0",
    author="0xCosmix",
    author_email="contact@0xcosmix.dev",
    description="Advanced OSINT Framework with Professional GUI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/0xCosmix/0xRecon",
    project_urls={
        "Bug Tracker": "https://github.com/0xCosmix/0xRecon/issues",
        "Documentation": "https://github.com/0xCosmix/0xRecon/tree/main/docs",
        "Source Code": "https://github.com/0xCosmix/0xRecon",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: Security",
    ],
    python_requires=">=3.10",
    install_requires=[
        "PyQt6>=6.4.0",
        "requests>=2.28.0",
        "dnspython>=2.3.0",
        "python-whois>=0.8.0",
        "reportlab>=4.0.0",
        "networkx>=3.0",
        "pillow>=9.0.0",
        "python-docx>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0",
            "pytest-cov>=4.0",
            "black>=23.0",
            "flake8>=6.0",
            "mypy>=1.0",
            "isort>=5.12",
            "pylint>=2.17",
        ],
    },
    entry_points={
        "console_scripts": [
            "0xrecon=0xrecon.gui.main_window:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

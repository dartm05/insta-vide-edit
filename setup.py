"""
Setup script for AI-Powered Instagram Video Editing Platform
"""
from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    requirements = [
        line.strip()
        for line in requirements_file.read_text().splitlines()
        if line.strip() and not line.startswith('#')
    ]

setup(
    name="instagram-video-agent",
    version="0.1.0",
    author="Your Name",
    description="AI-powered video editing platform for Instagram formats with style transfer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/instagram-video-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Multimedia :: Video",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "video-agent=examples.basic_edit:main",
            "copy-style=examples.copy_editing_style:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", ".env.example"],
    },
)

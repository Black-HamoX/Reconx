from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = [l.strip() for l in f if l.strip() and not l.startswith("#")]

setup(
    name="reconx",
    version="4.0.0",
    author="C5_72",
    description="OSINT Reconnaissance Toolkit for Termux",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "reconx=reconx.cli:main",
        ],
    },
    python_requires=">=3.8",
)
from setuptools import setup, find_packages

setup(
    name="ai_defender",
    version="1.0.0",
    author="Farida Haitham Mohamed Amin",
    description="In-Line White-Box Neuro-Probing Library for AI Agent Security",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "ai_defender": ["weights/*.pt"],
    },
    install_requires=[
        "torch",
        "transformers"
    ],
    entry_points={
        "console_scripts": [
            "ai-defender=ai_defender.cli:main",
        ],
    },
)

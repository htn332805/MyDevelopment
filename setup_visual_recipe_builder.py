# setup.py for visual_recipe_builder

from setuptools import setup, find_packages

setup(
    name="visual_recipe_builder",
    version="1.0.0",
    packages=find_packages(include=["visual_recipe_builder", "visual_recipe_builder.*"]),
    install_requires=[
        "dash>=3.0.0",
        "plotly>=6.0.0",
        "pyyaml>=6.0",
        "pandas>=1.3.0",
        "numpy>=1.21.0"
    ],
    python_requires=">=3.8",
)
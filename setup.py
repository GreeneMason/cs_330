from setuptools import setup, find_packages

setup(
    name="ufc_analysis",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "numpy>=1.24.0",
        "pandas>=2.0.0",
        "xgboost>=2.0.0",
        "scikit-learn>=1.3.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "shap>=0.42.0",
        "scipy>=1.11.0",
    ],
    author="GreeneMason",
    description="UFC Fight Analysis using Machine Learning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.8",
)
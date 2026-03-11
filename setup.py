from setuptools import setup, find_packages

setup(
    name="labconstrictor_demo",
    version="0.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.11.13",
    install_requires=[
    ],
)

from setuptools import setup, find_packages

setup(
    name="labconstrictor_demo",
    version="0.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=PYTHON_VERSION",
    install_requires=[
    ],
)

from setuptools import setup


setup(
    name="expense_manager",
    version="1.0.0",
    packages=["expense_manager"],
    author="bkandhasamy",
    author_email="bhuvanesh.kandhasamy@gmail.com",
    url="https://github.com/bkandhasamy/expense_manager.git",
    description="This package can be used for monthly expense and generate reports",
    python_requires=">=3.11",
    install_requires=[
        "pytest==8.3.3",
        "pandas==2.2.3",
        "flake8==7.1.1",
        "pytest==8.3.3",
        "black==24.10.0",
        "reportlab==4.2.5",
        "requests==2.32.3",
        "matplotlib==3.9.2",
    ],
)

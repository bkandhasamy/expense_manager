# Expense Manager

[![Python Version](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://img.shields.io/badge/Build-Passing-green.svg)](https://github.com/bkandhasamy/expense_manager.git/actions)


## Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Installation](#installation)
* [Requirements](#requirements)
* [Usage](#usage)
* [Best Practice](#Best Practice)
* [Authors](#authors)



## Overview

A simple and intuitive expense tracking application to help you manage your finances.


## Features

* Track daily expenses
* Categorize expenses (food, transportation, entertainment, etc.)
* Set Savings goal and receive insights & recommendations
* Visualize spending patterns using charts and graph
* Generate monthly/annual expense reports


## Installation
```bash
git clone https://github.com/bkandhasamy/expense_manager.git
cd expense_manager
```
### Create virtual environment
```bash
python3.11 -m venv venv
source ./venv/bin/activate
```
## Requirements
### Install dependencies
```bash
python -m pip install -r requirements.txt
```
### Install Package in Root Library Using pip
### Note: Please use absolute path for local installation
```bash
pip install <absolute_path>/expense_manager
```
## Usage
### pass parameter -h to get usage
```bash
python ~/expense_manager/scripts/run_expense_manager.py -h
```
```markdown
usage: run_expense_manager.py [-h] [-d] DATA_PATH DATE_MMYYYY SORT_COLUMN

positional arguments:
  DATA_PATH    Monthly Expense data path
  DATE_MMYYYY  Transaction month to process
  SORT_COLUMN  Column used to sort the expense file

options:
  -h, --help   show this help message and exit
  -d, --debug  Run the program in debug mode.
```
### pass parameter -d or --debug  to run program in debug mode
```bash
python ~/expense_manager/scripts/run_expense_manager.py -h
```
### Example
### Note: create required directory structure
```bash
~/expense_manager/scripts/run_expense_manager.py -d ~/expense_manager/data 112024 expense_category 
```
### Note sample data, reports and logs in data folder kept for reference

## Best Practice

### Run pre-commit hooks
```bash
pre-commit install
pre-commit run --al-files
```
```markdown
# Output
black....................................................................Passed
flake8...................................................................Passed
pytest...................................................................Passed
```

### Update CHANGELOG.md
### Versions follow Semantic versioning <MAJOR.MINOR.PATCH> https://semver.org/ 
```markdown
MAJOR version when you make incompatible API changes
MINOR version when you add functionality in a backward compatible manner
PATCH version when you make backward compatible bug fixes
```

## Authors
### Maintainers
- [bkandhasamy](https://github.com/bkandhasamy)



# spending_AI_manager

## Description

An intelligent spending manager application that uses AI to help track, analyze, and optimize personal or business expenses.

## Features

- Gets spendings saved in Google Sheet via Google Cloud API - requires private access to your own sheets.
- Attaches one category from category config file to transaction using fastText

## Installation

```bash
git clone https://github.com/yourusername/spending_AI_manager.git
cd spending_AI_manager
pip install -r requirements.txt
```

It is recommended to create a virtual environment.

## How does it work

Application is connecting to a private Google Sheet file via Google Cloud API. There you can copy credentials and paste them to the credentials.json file.
After connection, there are downloaded two types of information - amount of spending or income and description.
Application gets description and predicts the closest category from category_config.json file. For example "Train to Berlin" should be connected with "Transport" category.

## Technologies

- Python
- Google Cloud API
- fastText model

For more information feel free to contact with me!

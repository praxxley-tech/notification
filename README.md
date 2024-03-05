# Python Data Management and Notification System

This project comprises a set of Python scripts designed to work together to fetch data via a REST API, store it in a local PostgreSQL database, serialize the data for formatting, and finally, notify users of the process completion. It uses .txt files to track the creation of reports and prevent duplicate processing. The system is designed to be run automatically via cron jobs.

## Components

1. **RestAPI.py**: Fetches data using a REST API with basic authentication.
2. **db.py**: Inserts the fetched data into a local PostgreSQL database.
3. **serialization_1.py** and **serialization_2.py**: Two scripts for reading from the database and serializing the data into a well-formatted structure.
4. **ntfy.py**: Sends out a notification indicating the process completion.
5. **.txt files**: Used to track the reports that have been created to avoid duplication.

## Prerequisites

- Python 3.8 or higher
- PostgreSQL installed and running on the local machine
- Access credentials for the REST API
- A system that supports cron jobs for scheduling (typically a UNIX-like system)

## Installation

1. Clone this repository to your local machine.
2. Install the required Python dependencies:

```bash
pip install -r requirements.txt
```

1. Configure your PostgreSQL connection details. Add your credentials to bashrc
2. Set up your API credentails too in bashrc

## Configuration

### Database Setup
Ensure your PostgreSQL database is configured correctly and that db.py has the correct connection string.
You will find information how to set up under	[[title](https://www.postgresql.org/docs/current/tutorial-install.html)](https://www.postgresql.org/docs/current/tutorial-install.html)

### Notification Setup

Configure ntfy.py with your preferred method of notification (email, Slack, etc.), including any necessary API keys or SMTP settings.

## Usage

The scripts are designed to be run in a specific order:

1. RestAPI.py to fetch and store data.
2. db.py to insert data into the database.
3. serialization_1.py and serialization_2.py to format the data.
4. ntfy.py to send a notification.

You can set up cron jobs to automate the execution of these scripts. For example, to run RestAPI.py every day at 6 AM:
```bash
0 6 * * * /path/to/python3 /path/to/RestAPI.py
```

## Preventing Duplicate Reports

The system uses .txt files to track whether a report has already been created for a particular dataset. Ensure that these files are stored in a designated directory and are correctly referenced in the scripts to prevent duplicate processing.


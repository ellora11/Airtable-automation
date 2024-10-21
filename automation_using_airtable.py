# -*- coding: utf-8 -*-
"""Automation using Airtable

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/19BJ-wKFqv_f5nolC3FJc3KcBX9HWCkJO
"""

!pip install pyairtable

from pyairtable import Api
from datetime import datetime, timedelta

# Airtable credentials
PERSONAL_ACCESS_TOKEN = "pat8Y0x8V4U6Qa3ey.f03a71d75892933a980f0532220208244b4a0e39db54f39ff9f7d7018d7a02f3"  # Replace this with your actual token
BASE_ID = "appgXA6jifYpUvfqY"  # Replace this with your Airtable base ID
 # Replace this with your Airtable base ID
SCHEDULE_TABLE_NAME = "Time Blocks"  # Schedule table name
ARCHIVE_TABLE_NAME = "Archive"  # Archive table name
LINKED_TABLE_NAME = "Activities"  # Replace with the name of the linked table

# Initialize Airtable API and tables
api = Api(PERSONAL_ACCESS_TOKEN)
schedule_table = api.table(BASE_ID, SCHEDULE_TABLE_NAME)
archive_table = api.table(BASE_ID, ARCHIVE_TABLE_NAME)
tasks_table = api.table(BASE_ID, LINKED_TABLE_NAME)  # Table that holds the linked tasks

# Function to get task record IDs (modify query as needed)
def get_task_record_ids():
    task_records = tasks_table.all()
    task_record_ids = [record['id'] for record in task_records]
    return task_record_ids

# Function to move yesterday's records
def move_yesterdays_records():
    # Calculate yesterday's date
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    # Get all records from the Time Blocks table
    schedule_records = schedule_table.all()

    for record in schedule_records:
        # Replace 'Day/Date' and 'Scheduled Tasks' with the correct field names
        record_date = record['fields'].get('Day/Date', '')  # Ensure this matches your field name
        scheduled_tasks = record['fields'].get('Scheduled Tasks', '')  # Ensure this matches your field name
        status = record['fields'].get('Status', '')  # Ensure this matches your field name

        # Check if the record date matches yesterday's date
        if record_date == yesterday:
            # Move only the relevant fields to the Archive table
            archive_table.create({
                "Date": record_date,
                "Tasks": scheduled_tasks,
                "Status": status
            })

            # Delete the record from the Time Blocks table
            schedule_table.delete(record['id'])

# Function to create new slots for today
def create_today_slots():
    # Get today's date
    today = datetime.now().strftime("%Y-%m-%d")

    # Define the 5 time slots you want to create
    time_slots = ["09:00 AM", "11:00 AM", "01:00 PM", "03:00 PM", "05:00 PM"]

    # Fetch task record IDs from the linked Tasks table
    task_record_ids = get_task_record_ids()

    # Create a new record for each slot
    for slot in time_slots:
        # Insert the array of record IDs in the 'Scheduled Tasks' linked field
        schedule_table.create({
            "Date": today,  # Replace with the correct field name for the date
            "Tasks": task_record_ids[:1],  # Use the first task record ID for the time slot
            "Status": "Available"  # Ensure this matches your field name
        })

# Main function to run the automation
def run_daily_automation():
    # Step 1: Move yesterday's records
    move_yesterdays_records()

    # Step 2: Create today's 5 new slots
    create_today_slots()

# Run the automation
run_daily_automation()


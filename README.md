# parallel_text_handling_processor

Student Text Processor – Milestone 1
📌 Project Overview

The Student Text Processor is a Python-based parallel processing system designed to analyze student feedback data.

In Milestone-1, the system:

> Reads student feedback from a CSV file
> Processes the data using multiprocessing
> Applies rule-based sentiment scoring
> Stores results in an SQLite database
> Allows searching and exporting results

student_text_processor/
│
├── main.py                # Main execution file
├── generate_students.py   # Generates sample student data
├── config.py              # Configuration settings
├── database.py            # Database creation and operations
├── scorer.py              # Sentiment scoring logic
├── text_loader.py         # CSV loading functionality
├── search_module.py       # Search and export functionality
│
└── data/
      └── students.csv     # Student feedback dataset

**🚀 Features Implemented (Milestone-1)**

> CSV file handling (1000 student records)
> processing using multiprocessing
> Rule-based sentiment analysis using regex
> SQLite database integration
> Secure parameterized search queries
> Export search results to CSV
> Execution time tracking

** 🛠 Technologies Used **

> Python 3
> multiprocessing module
> csv module
> re (Regular Expressions)
> sqlite3
> time module

** ⚙ How the System Works **

> Loads student feedback from data/students.csv
> Splits data into chunks
> Processes feedback in parallel
> Calculates sentiment score using rule-based patterns
> Stores processed data in SQLite database
> Allows searching by student name
> Exports filtered results to CSV
> Displays total execution time

** ▶ How to Run **

1. Make sure Python 3 is installed.
2. Navigate to the project folder.
3. Run:
     python main.py
4. Enter student name when prompted (or press Enter to skip search).

**📊 Output**

> Database file created (e.g., student_data.db)
> Processed 1000 student records
> Search results exported to CSV
> Displays total processing time

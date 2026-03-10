# 🚀 Parallel Text Handling Processor

Parallel Text Handling Processor using Python multiprocessing to efficiently analyze large student feedback datasets with regex-based sentiment scoring and SQLite storage.
A Python-based parallel text processing system designed to efficiently analyze large volumes of student feedback using multiprocessing, regex-based sentiment scoring, and database storage.

The system reads feedback data from a dataset, splits it into chunks, processes the data in parallel using multiple CPU cores, and stores the analyzed results in a database for further search and export.

**Key Features**

* Parallel text processing using Python multiprocessing
* Chunk-based dataset handling for large datasets
* Regex-based sentiment scoring
* SQLite database integration
* CSV export functionality
* Modular and scalable architecture
* Logging system for monitoring execution

**Project Architecture**

 Dataset (students.csv)
        │
        ▼
Text Loader
(load dataset)
        │
        ▼
Chunk Generator
(split dataset into chunks)
        │
        ▼
Multiprocessing Pool
(using CPU cores)
        │
        ▼
Parallel Workers
(process chunks)
        │
        ▼
Regex Sentiment Scoring
        │
        ▼
Database Storage (SQLite)
        │
        ▼
Search & CSV Export

**Project Architecture**

parallel_text_handling_processor/
│
├── main.py
├── text_loader.py
├── scorer.py
├── database.py
├── search_module.py
├── students.csv
├── feedback.db
├── requirements.txt
└── README.md

**Dataset**

The dataset contains student feedback records used to test the system's ability to process large amounts of text data.

Example dataset format:

Student ID	Feedback
1	      The class was very helpful
2	      The lecture was boring
3	      The teacher explained clearly

For scalability testing, the dataset was expanded to 5000 feedback records.

Parallel Processing Strategy

The dataset is divided into smaller chunks before processing.

Example:

Total Records: 5000
Chunk Size: 250
Total Chunks: 20
CPU Cores Used: 2

Each CPU core processes different chunks simultaneously, which significantly improves processing speed compared to sequential execution.

**Sentiment Scoring**

Sentiment scoring is performed using regular expressions to detect positive and negative keywords in feedback text.

Example keywords:

Positive words:

good
excellent
great
amazing
helpful

Negative words:

bad
poor
slow
boring
confusing

Each feedback entry receives a sentiment classification based on keyword matches.

**Database Integration**

Processed results are stored in a SQLite database.

Database fields include:

Student ID

Feedback text

Sentiment score

Processing timestamp

Database file:

feedback.db

**Logging System**

The system uses Python logging to track program execution.

Example log output:

2026-03-08 23:27:06 - INFO - Total records loaded: 5000
2026-03-08 23:27:06 - INFO - Total chunks created: 20
2026-03-08 23:27:06 - INFO - Processing feedback in parallel
2026-03-08 23:27:06 - INFO - Using 2 CPU cores

Logging helps with debugging, monitoring performance, and tracking system behavior.

**Installation**

Clone the repository:

git clone https://github.com/yourusername/parallel_text_handling_processor.git

Navigate to the project directory:

cd parallel_text_handling_processor

Install required dependencies:

pip install -r requirements.txt

**Running the Project**

Run the main program:
python main.py

Expected output:
===== Student Feedback Processing System Started =====

Total records loaded: 5000
Total chunks created: 20
Processing feedback in parallel...
Using 2 CPU cores

Processing completed successfully
Results stored in database

**Performance and Scalability**

Parallel processing improves system efficiency when handling large datasets.

Example comparison:

Dataset Size	Sequential Processing	Parallel Processing
1000 records	slower	            faster
5000 records	slower	            significantly faster

The chunk-based multiprocessing approach allows the system to scale effectively as dataset size increases.

**Future Improvements**

Possible enhancements for the system include:
Machine learning-based sentiment analysis
Web dashboard for visualization
Support for larger distributed datasets
Use of advanced databases like PostgreSQL
Dynamic CPU core allocation

**Conclusion**

The Parallel Text Handling Processor demonstrates how parallel computing techniques can be applied to large-scale text analysis problems. By combining multiprocessing, chunk-based processing, sentiment analysis, and database storage, the system provides an efficient and scalable solution for analyzing large datasets.

Database Integration

Processed results are stored in a SQLite database.

Database fields include:

Student ID

Feedback text

Sentiment score

Processing timestamp

Database file:

feedback.db
Logging System

The system uses Python logging to track program execution.

Example log output:

2026-03-08 23:27:06 - INFO - Total records loaded: 5000
2026-03-08 23:27:06 - INFO - Total chunks created: 20
2026-03-08 23:27:06 - INFO - Processing feedback in parallel
2026-03-08 23:27:06 - INFO - Using 2 CPU cores

Logging helps with debugging, monitoring performance, and tracking system behavior.

Installation

Clone the repository:

git clone https://github.com/yourusername/parallel_text_handling_processor.git

Navigate to the project directory:

cd parallel_text_handling_processor

Install required dependencies:

pip install -r requirements.txt
Running the Project

Run the main program:

python main.py

Expected output:

===== Student Feedback Processing System Started =====

Total records loaded: 5000
Total chunks created: 20
Processing feedback in parallel...
Using 2 CPU cores

Processing completed successfully
Results stored in database
Performance and Scalability

Parallel processing improves system efficiency when handling large datasets.

Example comparison:

Dataset Size	Sequential Processing	Parallel Processing
1000 records	slower	faster
5000 records	slower	significantly faster

The chunk-based multiprocessing approach allows the system to scale effectively as dataset size increases.

Future Improvements

Possible enhancements for the system include:

Machine learning-based sentiment analysis

Web dashboard for visualization

Support for larger distributed datasets

Use of advanced databases like PostgreSQL

Dynamic CPU core allocation

**Conclusion**

The Parallel Text Handling Processor demonstrates how parallel computing techniques can be applied to large-scale text analysis problems. By combining multiprocessing, chunk-based processing, sentiment analysis, and database storage, the system provides an efficient and scalable solution for analyzing large datasets.

**Milestone Implementation**

This project was developed following a milestone-based approach to ensure structured development and gradual improvement of the system.

**Milestone 1: System Setup and Basic Processing (Weeks 1–2)**

Goal: Build the basic text processing system.

Tasks completed:

Created the project structure
Implemented dataset loading from CSV
Developed regex-based sentiment scoring
Built database module for storing feedback
Added logging for tracking system execution
Successfully processed small datasets

**Milestone 2: Text Breaker and Loader (Weeks 3–4)**

Goal: Improve system performance using parallel processing.
Tasks completed:
Implemented data chunking to divide the dataset into smaller groups
Built a text loader module for handling large datasets
Implemented multiprocessing using CPU cores
Tested system with large datasets (5000 records)
Measured performance improvements
Example processing configuration:

Total records: 5000
Chunk size: 250
Total chunks: 20
CPU cores used: 2

This milestone improved the speed, efficiency, and scalability of the system.

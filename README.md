## 🚀 Parallel Text Handling Processor

A Python-based parallel text processing system designed to efficiently analyze large volumes of student feedback using multiprocessing, regex sentiment scoring, and SQLite database storage.

The system reads a dataset, divides it into chunks, processes the chunks in parallel using CPU cores, and stores the results for search and export.

## 📌 Project Overview

| Feature | Description |
|--------|-------------|
| Language | Python |
| Processing | Parallel processing using multiprocessing |
| Text Analysis | Regex-based sentiment scoring |
| Database | SQLite |
| Dataset | Student feedback records |
| Output | Database storage + CSV export |

🏗 System Architecture

                +----------------------+
                |   students.csv       |
                | (Feedback Dataset)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    text_loader.py    |
                | Load & Chunk Data    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Multiprocessing    |
                |   Pool (CPU cores)   |
                +----+-----------+-----+
                     |           |
                     v           v
              +-----------+ +-----------+
              | Worker 1  | | Worker 2  |
              |Chunk Proc.| |Chunk Proc.|
              +-----+-----+ +-----+-----+
                    |             |
                    +------v------+
                           |
                           v
                +----------------------+
                |      scorer.py       |
                | Sentiment Analysis   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |     database.py      |
                | SQLite Storage       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    search_module     |
                | Search & CSV Export  |
                +----------------------+

                +----------------------+
                |   students.csv       |
                | (Feedback Dataset)   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    text_loader.py    |
                | Load & Chunk Data    |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Multiprocessing    |
                |   Pool (CPU cores)   |
                +----+-----------+-----+
                     |           |
                     v           v
              +-----------+ +-----------+
              | Worker 1  | | Worker 2  |
              |Chunk Proc.| |Chunk Proc.|
              +-----+-----+ +-----+-----+
                    |             |
                    +------v------+
                           |
                           v
                +----------------------+
                |      scorer.py       |
                | Sentiment Analysis   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |     database.py      |
                | SQLite Storage       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |    search_module     |
                | Search & CSV Export  |
                +----------------------+

## 📂 Project Structure

| File / Folder | Description |
|---------------|-------------|
| `main.py` | Main program that runs the entire workflow including loading data, parallel processing, database storage, and search/export |
| `generate_students.py` | Script used to generate student feedback dataset |
| `config.py` | Contains configuration settings such as chunk size and other constants |
| `database.py` | Handles SQLite database operations like creating tables, inserting data, and searching records |
| `scorer.py` | Performs sentiment scoring using regex-based rules |
| `text_loader.py` | Loads CSV data and divides it into chunks for parallel processing |
| `search_module.py` | Handles searching records and exporting results to CSV |
| `data/` | Folder that stores dataset files |
| `data/students.csv` | CSV file containing student feedback dataset |

## ⚙️ System Workflow

| Step | Process | Description |
|-----|--------|-------------|
| 1 | Load Data | Read student feedback data from CSV file |
| 2 | Chunk Data | Split the dataset into smaller chunks |
| 3 | Parallel Processing | Process chunks simultaneously using multiprocessing |
| 4 | Sentiment Scoring | Apply regex rules to analyze feedback sentiment |
| 5 | Store Results | Save processed results into SQLite database |
| 6 | Search Records | Allow user to search feedback by student name |
| 7 | Export Results | Export results to CSV file |

## ⚡ Parallel Processing

The system uses Python's multiprocessing module to process chunks in parallel.

Example configuration:

| Parameter | Value |
|----------|-------------|
| Dataset Size| 5000 records |
| Chunk Size | 250 |
| Total Chunks | 20 |
| CPU Cores Used | 2|

Each CPU core processes different chunks simultaneously, improving performamce.

## 🧠 Sentiment Scoring (Regex)

Sentiment scoring is performed using keyword-based regex matching.

| Sentiment Type | Example Words |
|---------------|---------------|
| Positive | good, excellent, amazing, helpful |
| Negative | bad, poor, terrible, boring |
| Neutral | feedback without positive or negative keywords |

| Score Condition | Sentiment Result |
|----------------|------------------|
| Score > 0 | Positive |
| Score = 0 | Neutral |
| Score < 0 | Negative |

## 💾 Database Integration

| Column  | Description |
|----------|-------------|
| student_id|Unique student ID |
|student_name|Name of student |
| feedback | Feedback text |
| score | sentiment score |
| sentiment | sentiment label |

## 📊 Example Output
```
===== Student Feedback Processing System =====

Total records loaded: 5000
Total chunks created: 20
Processing feedback in parallel...
Using 2 CPU cores

Data stored in database successfully.
Total records processed: 5000
Processing completed in 2.1 seconds
```

##  🛠 Installation

Clone the repository:
```
git clone https://github.com/SriveniBingi/parallel_text_handling_processor
```
Navigate to project folder:
```
cd parallel_text_handling_processor
```
Run the program:
```
python main.py
```

## 📈 Performance and Scalability

| Feature | Explanation |
|-------|-------------|
| Parallel Processing | Multiple CPU cores process data simultaneously |
| Chunking Strategy | Large datasets divided into smaller chunks |
| Dataset Tested | 5000 student feedback records |
| Performance Benefit | Reduced processing time |
| Scalability | System can handle larger datasets efficiently |

## 🗺 Milestone Implementation
#Milestone 1

* Built modular project structure

* Implemented dataset loading

* Developed regex sentiment scoring

* Added SQLite database integration

#Milestone 2

* Implemented chunk-based processing

* Added multiprocessing support

* Tested with 5000 feedback records

* Improved processing performance

## 👩‍💻 Author

Sriveni Bingi

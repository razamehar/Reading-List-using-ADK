# Reading List using ADK

This project manages your reading list using Google's Agent Development Kit (ADK.  

## Features

- Add books to your reading list  
- Update book status: `to read`, `currently reading`, `read`  
- Annotate notes for each book  
- List all books with their status  
- Remove books from the list  
- Save and maintain user-specific state  


## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```


2. Install required packages:
```bash
pip install -r requirements.txt
```

## Usage
1. Run the main applications:
```bash
python main.py
```

2. Commands
- `add "Book Title" [status]` – Add a book with optional status (`to read` by default)  
- `update <index> [title] [status] [notes]` – Update a book at a given index  
- `annotate <index> <notes>` – Add notes to a book  
- `list [status]` – List all books, optionally filtered by status  
- `remove <index>` – Remove a book from the list  
- `exit` – Quit the application

## Status Values
- `to read` – Book is planned to read  
- `currently reading` – Book is being read  
- `read` – Book has been finished


## License
This project is licensed under the Raza Mehar License. See the LICENSE.md file for details.

## Contact
For any questions or clarifications, please contact Raza Mehar at [raza.mehar@gmail.com].
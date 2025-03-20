# Simple CLI Application

A simple interactive command-line application that responds to basic commands.

## Setup

### Virtual Environment
1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
# On macOS/Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. To deactivate when done:
```bash
deactivate
```

## Commands
- `hello`: Outputs "hello"
- `help`: Shows available commands and their descriptions
- `exit`: Quits the program

## Running the Application
Make sure your virtual environment is activated, then run:
```bash
python main.py
```

## Running Tests
With virtual environment activated:
```bash
python -m unittest discover tests
```
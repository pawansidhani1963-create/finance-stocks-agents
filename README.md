# Finance Stocks Agents

This project is designed to build agents that retrieve and process stock fundamental data using the SEC (Securities and Exchange Commission) data.

## Project Structure

```
finance-stocks-agents
├── src
│   ├── __init__.py
│   ├── sec_client.py
│   ├── data_layer.py
│   └── models
│       └── __init__.py
├── tests
│   ├── __init__.py
│   └── test_data_layer.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd finance-stocks-agents
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

- The `sec_client.py` file contains the implementation for fetching stock fundamental data from the SEC.
- The `data_layer.py` file handles the logic for data retrieval and processing.
- Unit tests can be found in the `tests/test_data_layer.py` file.

## Environment Variables

Make sure to set up your environment variables in the `.env` file as needed for your application.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
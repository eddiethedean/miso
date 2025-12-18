# MISO Management System

A Streamlit-based application for managing and analyzing Military Information Support Operations (MISO) and Cyber operations data.

## Setup

1. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Initialize database:**
```bash
python init_database.py
```

4. **Generate fake data:**
```bash
python generate_fake_data.py
```

5. **Run the application:**
```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`

## Features

- **Analytics Dashboard**: View tables, charts, and metrics for MISO operations
- **Data Export**: Export PSYOP, Cyber, and Civil Affairs data to Excel
- **Filtering**: Filter by fiscal year, quarter, TSOC, threats, programs, and more
- **Visualizations**: Interactive charts showing operations by various dimensions

## Database

The application uses SQLite (`miso.db`) for data storage. The database includes:

- `miso_series`: PSYOP series data
- `miso_execution`: Execution details
- `miso_assessment`: Assessment metrics
- `miso_location`: Geographic data for series
- `cyber_series`: Cyber operations data
- `cyber_assessment`: Cyber assessments
- `cyber_location`: Geographic data for cyber operations

## Testing

The project includes a comprehensive test suite using pytest and Streamlit's built-in testing framework.

### Run Tests
```bash
# Run all tests
pytest tests/

# Run with coverage
pytest tests/ --cov=modules --cov-report=html

# Run specific test file
pytest tests/test_data_operations.py
```

See [tests/README.md](tests/README.md) for detailed testing documentation.

## Project Structure

```
miso/
├── app.py                      # Main Streamlit application
├── init_database.py            # Database initialization script
├── generate_fake_data.py       # Fake data generator
├── requirements.txt             # Python dependencies
├── miso.db                     # SQLite database (created after setup)
├── pytest.ini                  # Pytest configuration
├── tests/                       # Test suite
│   ├── conftest.py             # Test fixtures
│   ├── test_constants.py       # Constants tests
│   ├── test_data_operations.py # Data operations tests
│   ├── test_analytics_data_operations.py  # Analytics tests
│   └── test_streamlit_app.py   # Streamlit UI tests
└── modules/
    ├── analytics.py            # Analytics page
    ├── export.py               # Export functionality
    ├── data_operations.py      # Data operations
    ├── analytics_charts.py    # Chart generation
    ├── analytics_data_operations.py  # Analytics helpers
    └── constants.py           # Constants and schemas
```


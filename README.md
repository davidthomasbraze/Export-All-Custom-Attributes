# Braze Custom Attribute Exporter

This script fetches all custom attributes from your Braze account and outputs them as a JSON array.

## Requirements

- Python 3
- `requests` library
- `dotenv` library

## Setup

1.  **Install Dependencies:**
    Open your terminal and run the following command to install the required Python library. Using `python3 -m pip` ensures that the package is installed for the correct interpreter.

    ```bash
    python3 -m pip install -r requirements.txt
    ```

2.  **Create a `.env` file:**
    This file stores your Braze API credentials. A `.env` file has been created for you.

3.  **Add your credentials to `.env`:**
    Open the `.env` file and replace the placeholder values with your actual Braze API key and REST API host.

    ```bash
    # Your REST API key with users.track permission
    BRAZE_API_KEY="YOUR_API_KEY_HERE"

    # Host portion of your REST endpoint (e.g., rest.iad-01.braze.com)
    BRAZE_REST_API_HOST="YOUR_BRAZE_HOST_HERE"

    # Optional: Path to write the full JSON payload (defaults to None)
    # OUT_FILE="braze_attributes.json"
    #
    # Optional: Path to write a CSV of attributes (defaults to None)
    # CSV_FILE="braze_attributes.csv"
    ```

## Usage

To run the script, you need to source the environment variables from the `.env` file first.

```bash
# Make the script executable
chmod +x fetch_attributes.py

# Run the script
./fetch_attributes.py
```

The script will print the JSON output to the console. If you set the `OUT_FILE` variable in your `.env` file, it will also save the output to that file. Similarly, if you set `CSV_FILE`, a CSV version will be written to the specified path.
# Export-All-Custom-Attributes

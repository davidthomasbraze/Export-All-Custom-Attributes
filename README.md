# Braze Custom Attribute Exporter

This script fetches all custom attributes from your Braze account and outputs them as a JSON array. This can optionally be saved as JSON file and CSV.

This script utilizes Braze's `/custom_attributes` endpoint. For more details on the API, please refer to the official [Braze documentation](https://www.braze.com/docs/api/endpoints/export/custom_attributes/get_custom_attributes).

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
    This file stores your Braze API credentials. A `.env.example` file has been created for you.

3.  **Add your credentials to `.env`:**
    Open the `.env` file and replace the placeholder values with your actual Braze API key and REST API host.

    ```bash
    # Your REST API key with users.track permission
    BRAZE_API_KEY="YOUR_API_KEY_HERE"

    # Host portion of your REST endpoint (e.g., https://rest.iad-01.braze.com)
    BRAZE_REST_ENDPOINT="YOUR_BRAZE_REST_ENDPOINT"

    # Optional: Path to write the full JSON payload (defaults to None)
    # OUT_FILE="braze_attributes.json"
    #
    # Optional: Path to write a CSV of attributes (defaults to None)
    # CSV_FILE="braze_attributes.csv"
    ```

## Usage

To run the script, execute it with `python3`. The script will automatically load the environment variables from your `.env` file.

```bash
python3 fetch_attributes.py
```

The script will print the JSON output to the console. If you set the `OUT_FILE` variable in your `.env` file, it will also save the output to that file. Similarly, if you set `CSV_FILE`, a CSV version will be written to the specified path.

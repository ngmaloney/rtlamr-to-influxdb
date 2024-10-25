import sys
import json
import os
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from dateutil import parser
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch InfluxDB connection details from environment variables
INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")

def parse_input(json_input):
    try:
        # Parse the JSON string
        data = json.loads(json_input)

        # Extract the relevant fields
        time = data.get("Time")
        timestamp = parser.isoparse(time)  # Use dateutil's parser to handle the timestamp
        message = data.get("Message", {})
        consumption = message.get("Consumption", 0)
        tamper_phy = message.get("TamperPhy", 0)
        tamper_enc = message.get("TamperEnc", 0)
        msg_id = message.get("ID", "N/A")
        msg_type = message.get("Type", "N/A")  # Extract "Type" from Message

        # Construct line protocol with Type as a tag
        point = (
            Point("sensor_data")  # Measurement name
            .tag("ID", str(msg_id))  # Add ID as a tag
            .tag("Type", str(msg_type))  # Add Type as a tag
            .field("Consumption", consumption)  # Add fields
            .field("TamperPhy", tamper_phy)
            .field("TamperEnc", tamper_enc)
            .time(timestamp)  # Add time
        )

        return point

    except json.JSONDecodeError:
        print(f"Invalid JSON input: {json_input}")
        return None

def write_to_influxdb(point):
    # Create a client
    client = InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG)

    # Get the write API
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Write the data
    write_api.write(INFLUXDB_BUCKET, INFLUXDB_ORG, point)

    # Close the client
    client.close()

if __name__ == "__main__":
    # Read the input stream line by line (each line should be a valid JSON object)
    for line in sys.stdin:
        line = line.strip()  # Remove any extra spaces or newline characters
        if line:
            point = parse_input(line)  # Parse and process each JSON object
            if point:
                write_to_influxdb(point)
                print("Data sent to InfluxDB successfully!")
            else:
                print("Failed to send data to InfluxDB.")

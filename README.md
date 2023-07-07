# AT Command Fuzzing Script

## Description

This script performs fuzzing on AT commands sent to an IoT device via a serial connection. It reads a log file containing AT inputs, sends the commands to the device, and checks the response from the Command Line Interface (CLI). Any errors encountered during the process are logged to an error file.

## Prerequisites

- Python 3.x
- pySerial library

## Usage

1. Ensure that the serial ports (`usb1_serial_AT` and `acm1_serial_CLI`) are correctly configured for your system.
2. Set the `error_file` and `inputs_file` variables to appropriate file paths.
3. Run the script.
4. The script will read AT inputs from the log file and send them to the IoT device.
5. The CLI response will be checked for errors, and any encountered errors will be logged to the error file.

## Files

- **error_inputs.txt**: The file where encountered errors are logged.
- **putty_AT_fuzzingsession1.log**: The log file containing AT inputs for fuzzing.

## Notes

- This script assumes the use of two serial ports: `usb1_serial_AT` for sending AT commands and `acm1_serial_CLI` for receiving CLI responses.
- Ensure that the correct baud rate is set for both serial connections (default: 115200).
- Customize the script as needed for your specific setup and requirements.

## License

This project is licensed under the [MIT License](LICENSE).

##Athour
Alon Gritsovsky

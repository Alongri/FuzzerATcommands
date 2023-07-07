import serial
import time




def read_at_inputs_from_log(inputs_file):
    """read from log file and put it in arr"""
    with open(inputs_file, "rb") as f:
        lines = f.readlines()
        AT_input = []
        for line in lines:
            AT_input.append(line.strip())
    return AT_input


def send_inputs_to_AT_and_check_CLI(usb1_serial_AT,acm1_serial_CLI, AT_input):
    """
        1) gets both ports AT and CLI and arr of AT_input
        2) check if AT% or AT+ are in AT_input
        3) send command to AT
        4) Read ERROR or OK from USB1=AT and check response in CLI
        5) Return none if  ERROR or OK is returned and cli is empty
        6) else put un array all the errors
    """
    iteration = 0
    errors_array = []
    for line in AT_input:
        if line.startswith(b"AT%") or line.startswith(b"AT+"):
            print("iteration: " + str(iteration))
            iteration+=1
            usb1_serial_AT.write(line+b"\n\r")
            print(b"Sent: " + line)
            time.sleep(200 / 1000)
            last_output_AT = read_from_usb1(usb1_serial_AT)
            print("recived output usb1: " + last_output_AT)
            last_output_CLI = acm1_serial_CLI.readline()
            print("recived output acm1: " + last_output_CLI.decode())
            if b"RTOS Exception" in last_output_CLI or b"MAC Assert" in last_output_CLI \
                or b"error parse string" in last_output_CLI or b"RTOS Assert" in last_output_CLI \
                or b"System Error" in last_output_CLI or b"RTOS Stack Overflow" in last_output_CLI\
                    or b"Watchdog Timeout" in last_output_CLI:
                error_from_cli_and_at = "The CLI output is: "+last_output_CLI.decode() +\
                                        "The AT output is: " + last_output_AT.decode()
                print("found error: " + error_from_cli_and_at)
                errors_array.append(error_from_cli_and_at)
    return errors_array

def read_from_usb1(usb1_serial_AT):
    """read from usb1 and put it in arr"""
    while True:
        output = usb1_serial_AT.readline().rstrip(b'\n\r')
        #print(output)
        if output == b"ERROR" or output == b"OK":
            return output.decode()

def write_to_file(errors_array):
    """write all error array to error file"""
    with open(error_file, "ab") as f:
        for line in errors_array:
            f.write(line + "\n")





error_file = "/home/iotuser/fuzzer/error_inputs.txt"
inputs_file = "/home/iotuser/fuzzer/putty_AT_fuzzingsession1.log"
usb1_serial_AT = serial.Serial("/dev/ttyUSB0", baudrate=115200)
acm1_serial_CLI = serial.Serial("/dev/ttyACM1",baudrate=115200 , timeout=1)

AT_input = read_at_inputs_from_log(inputs_file)
print("number of AT inputs: " + str(len(AT_input)))
print("starting fuzzing")
errors_array = send_inputs_to_AT_and_check_CLI(usb1_serial_AT,acm1_serial_CLI, AT_input)
print("exection finished,number of errors: " + str(len(errors_array)))
write_to_file(errors_array)

usb1_serial_AT.close()
acm1_serial_CLI.close()



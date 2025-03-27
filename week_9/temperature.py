# Import necessary libraries
import os  # Provides functions to interact with the operating system
import glob  # Used to find pathnames matching a specified pattern
import time  # Provides time-related functions like sleep

def setup():
    # Load the necessary kernel modules for 1-Wire communication
    os.system('modprobe w1-gpio')  # Load the w1-gpio module for GPIO support
    os.system('modprobe w1-therm')  # Load the w1-therm module for temperature sensor support
    
    # Define the base directory where 1-Wire devices are registered
    base_dir = '/sys/bus/w1/devices/'
    # Find the folder corresponding to the DS18B20 sensor (starts with '28')
    device_folder = glob.glob(base_dir + '28*')[0]
    # Define the path to the sensor's data file
    device_file = device_folder + '/w1_slave'
    
    # Return the path to the sensor's data file
    return device_file

def read_file(device_file):
    # Open the sensor's data file in read mode
    with open(device_file, 'r') as f:
        # Read all lines from the file and store them in a list
        lines = f.readlines()  # Each line is a string ending with a newline character
    # Return the list of lines
    return lines

def read_temperature(device_file):
    # Continuously attempt to read valid temperature data
    while True:
        # Read the lines from the sensor's data file
        lines = read_file(device_file)
        
        # Check if the data is valid (the first line should end with 'YES')
        while lines[0].strip()[-3:] != 'YES':
            # If not valid, wait 0.2 seconds and try again
            time.sleep(0.2)
            lines = read_file(device_file)
        
        # Find the position of the temperature value in the second line
        temp_pos = lines[1].find('t=')
        if temp_pos != -1:  # If the temperature value is found
            # Extract the temperature string (starting after 't=')
            temp_string = lines[1][temp_pos+2:]
            # Convert the temperature string to a float and divide by 1000 to get Celsius
            temp_c = float(temp_string) / 1000.0
            # Convert Celsius to Fahrenheit
            temp_f = temp_c * 9.0 / 5.0 + 32.0
            # Return the temperature in both Celsius and Fahrenheit
            return temp_c, temp_f

def loop(device_file):
    
        # Continuously read and display the temperature
        while True:
            # Read the temperature in Celsius and Fahrenheit
            celsius, fahrenheit = read_temperature(device_file)
            # Print the temperature with 2 decimal places
            print(f"Temperature: {celsius:.2f} °C, {fahrenheit:.2f} °F")
            # Wait for 1 second before reading the temperature again
            time.sleep(1)
    

# Program entry point
if __name__ == '__main__':
    # Print a message indicating how to stop the program
    print("Press Ctrl+C to end the program...")
    # Set up the sensor and get the path to its data file
    device_file = setup()
    try:
        # Start the loop to read and display temperature
        loop(device_file)
    except KeyboardInterrupt:
        # Print a goodbye message if the program is interrupted
        print("Bye")
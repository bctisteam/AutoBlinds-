import RPi.GPIO as GPIO
import time

# Pin Definitions
LDR_PIN = 3
MOT_A_PIN = 16
MOT_B_PIN = 18
MOT_E_PIN = 22

# Timing Constants
INITIAL_DELAY = 5  # Delay between actions in seconds
THRESHOLD = 5      # Threshold for LDR value change
MIN_CHANGE = 3     # Minimum change in LDR value to trigger motor movement
INTERVAL = 5       # Interval for movement scaling
BASE_DURATION = 3  # Base duration for a single interval movement

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(MOT_A_PIN, GPIO.OUT)
GPIO.setup(MOT_B_PIN, GPIO.OUT)
GPIO.setup(MOT_E_PIN, GPIO.OUT)
GPIO.setup(LDR_PIN, GPIO.IN)

def set_motor_state(motA, motB, motE):
    GPIO.output(MOT_A_PIN, motA)
    GPIO.output(MOT_B_PIN, motB)
    GPIO.output(MOT_E_PIN, motE)

def read_ldr():
    GPIO.setup(LDR_PIN, GPIO.OUT)
    GPIO.output(LDR_PIN, GPIO.LOW)
    time.sleep(0.1)
    GPIO.setup(LDR_PIN, GPIO.IN)
    start_time = time.time()
    while GPIO.input(LDR_PIN) == GPIO.LOW:
        pass
    ldr_value = (time.time() - start_time) * 1000  # Convert to milliseconds
    return ldr_value

def move_motor(duration, direction):
    set_motor_state(direction[0], direction[1], GPIO.HIGH)
    print(f"Moving motor {'up' if direction == (GPIO.LOW, GPIO.HIGH) else 'down'} for {duration} seconds")
    time.sleep(duration)
    # Stop motor after movement
    set_motor_state(GPIO.LOW, GPIO.LOW, GPIO.LOW)

def initialize_motor(ldr_value):
    if ldr_value <= 20:
        print("Initial LDR value: Full position")
        move_motor(32, (GPIO.HIGH, GPIO.LOW))  # Example duration for Semi position
    elif 21 <= ldr_value <= 61.5:
        print("Initial LDR value: Half position")
        move_motor(24, (GPIO.HIGH, GPIO.LOW))  # Example duration for ThreeQ position
    elif 61.6 <= ldr_value <= 80:
        print("Initial LDR value: ThreeQ position")
        move_motor(16, (GPIO.HIGH, GPIO.LOW))  # Example duration for Half position
    else:
        print("Initial LDR value: Semi position")
        move_motor(8, (GPIO.HIGH, GPIO.LOW))  # Example duration for Full position

def main():
    # Initial LDR Reading
    initial_ldr_value = read_ldr()
    print(f'Initial LDR Value: {initial_ldr_value}')
    
    # Initialize motor based on initial LDR reading
    initialize_motor(initial_ldr_value)
    
    # Stop the motor after initial positioning
    set_motor_state(GPIO.LOW, GPIO.LOW, GPIO.LOW)
    print("Motor stopped after initialization.")

    previous_ldr_value = initial_ldr_value
    
    try:
        while True:
            # Read the current LDR value with a delay
            time.sleep(3)  # 3-second delay before reading the LDR value
            current_ldr_value = read_ldr()
            print(f'Current LDR Value: {current_ldr_value}')
            
            # Calculate the difference
            difference = current_ldr_value - previous_ldr_value
            
            # Check if the change is significant enough
            if abs(difference) >= MIN_CHANGE:
                intervals = int(abs(difference) / INTERVAL)
                duration = intervals * BASE_DURATION
                direction = (GPIO.LOW, GPIO.HIGH) if difference > 0 else (GPIO.HIGH, GPIO.LOW)
                
                move_motor(duration, direction)
                
                # Update previous LDR value
                previous_ldr_value = current_ldr_value
            else:
                print("LDR value change too small, no motor movement")
            
            time.sleep(INITIAL_DELAY)
    
    except KeyboardInterrupt:
        print("Program Stopped")
    
    finally:
        GPIO.output(MOT_A_PIN, GPIO.LOW)
        GPIO.output(MOT_B_PIN, GPIO.LOW)
        GPIO.output(MOT_E_PIN, GPIO.LOW)
        GPIO.cleanup()

if __name__ == "__main__":
    main()
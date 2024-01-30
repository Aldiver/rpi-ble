import random

def generate_random_readings():
    heart_rate = random.randint(60, 100)
    steps = random.randint(1000, 5000)
    calories_burned = random.randint(100, 500)
    distance = random.uniform(1.0, 5.0)
    
    readings = f"Heart Rate: {heart_rate} bpm, Steps: {steps}, Calories Burned: {calories_burned}, Distance: {distance} km"
    return readings

random_readings = generate_random_readings()
print(random_readings)

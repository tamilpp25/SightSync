import smbus
import math
import time

# MPU6050 Registers
POWER_MGMT_1 = 0x6B
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H = 0x43
GYRO_YOUT_H = 0x45
GYRO_ZOUT_H = 0x47

# MPU6050 Configuration
DEVICE_ADDRESS = 0x68  # MPU6050 device address
bus = smbus.SMBus(1)  # Rev 2 Pi uses 1

def read_word(reg):
    high = bus.read_byte_data(DEVICE_ADDRESS, reg)
    low = bus.read_byte_data(DEVICE_ADDRESS, reg + 1)
    val = (high << 8) + low
    return val

def read_word_2c(reg):
    val = read_word(reg)
    if val >= 0x8000:
        return -((65535 - val) + 1)
    else:
        return val

def dist(a, b):
    return math.sqrt((a * a) + (b * b))

def get_y_rotation(x, y, z):
    radians = math.atan2(x, dist(y, z))
    return -math.degrees(radians)

def get_x_rotation(x, y, z):
    radians = math.atan2(y, dist(x, z))
    return math.degrees(radians)

bus.write_byte_data(DEVICE_ADDRESS, POWER_MGMT_1, 0)

while True:
    accel_x = read_word_2c(ACCEL_XOUT_H) / 16384.0
    accel_y = read_word_2c(ACCEL_YOUT_H) / 16384.0
    accel_z = read_word_2c(ACCEL_ZOUT_H) / 16384.0

    gyro_x = read_word_2c(GYRO_XOUT_H) / 131.0
    gyro_y = read_word_2c(GYRO_YOUT_H) / 131.0
    gyro_z = read_word_2c(GYRO_ZOUT_H) / 131.0

    print("Accelerometer: x={:.2f}g y={:.2f}g z={:.2f}g".format(accel_x, accel_y, accel_z))
    print("Gyroscope:     x={:.2f}°/s y={:.2f}°/s z={:.2f}°/s".format(gyro_x, gyro_y, gyro_z))
    
    time.sleep(0.1)  # Adjust sleep time as needed

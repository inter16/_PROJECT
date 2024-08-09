from flask import Flask, request
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# GPIO 설정
SPEAKER_PIN = 18  # 스피커가 연결된 GPIO 핀 번호
FREQUENCY = 440  # 기본 주파수 (Hz)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SPEAKER_PIN, GPIO.OUT)
pwm = GPIO.PWM(SPEAKER_PIN, FREQUENCY)
pwm.start(0)  # 초기에는 스피커를 끕니다.

@app.route('/speaker/on', methods=['POST'])
def turn_on_speaker():
    frequency = request.json.get('frequency', FREQUENCY)
    pwm.ChangeFrequency(frequency)
    pwm.ChangeDutyCycle(50)  # 50% duty cycle로 스피커를 켭니다.
    return f"Speaker turned on with frequency {frequency} Hz", 200

@app.route('/speaker/off', methods=['POST'])
def turn_off_speaker():
    pwm.ChangeDutyCycle(0)  # Duty cycle을 0으로 설정하여 스피커를 끕니다.
    return "Speaker turned off", 200

@app.route('/speaker/set_frequency', methods=['POST'])
def set_frequency():
    frequency = request.json.get('frequency', FREQUENCY)
    pwm.ChangeFrequency(frequency)
    return f"Frequency set to {frequency} Hz", 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        pwm.stop()
        GPIO.cleanup()
from flask import Flask, render_template, jsonify
import requests
from geopy.geocoders import Nominatim

app = Flask(__name__)

class SafetyDevice:
    def __init__(self):
        self.emergency_contacts = {
            'primary': '1234567890',  
            'police': '112'  
        }

    def send_telegram_message(self, chat_id='7439759200', message="I am in danger"):
        bot_token = '7251028903:AAGJLqT8f6oWt7IQePHIO3UmRz8Wwu9tS-U'
        send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'
        response = requests.get(send_text)
        return response.json()
    
    def get_location(self):
        response = requests.get("http://ipinfo.io")
        data = response.json()
        location = data['loc'].split(',')
        latitude, longitude = location[0], location[1]

        geolocator = Nominatim(user_agent="geoapi")
        location_address = geolocator.reverse(f"{latitude}, {longitude}")

        return {
            'latitude': latitude,
            'longitude': longitude,
            'address': location_address.address if location_address else "Address not found"
        }
    
    def send_sms(self, number, location):
        location_message = f"Latitude: {location['latitude']}, Longitude: {location['longitude']}, Address: {location['address']}"
        print(f"Sending SMS to {number} with location {location_message}")
    
    def send_alert(self):
        location_data = self.get_location()  
        self.send_sms(self.emergency_contacts['primary'], location_data)
        self.send_sms(self.emergency_contacts['police'], location_data)
        self.send_telegram_message(message=f"I am in danger. My location is: Latitude: {location_data['latitude']}, Longitude: {location_data['longitude']}, Address: {location_data['address']}")
        return location_data

safety_device = SafetyDevice()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/alert', methods=['GET'])
def trigger_alert():
    location_data = safety_device.send_alert()
    return jsonify(location_data)

if __name__ == '__main__':
    app.run(debug=True)

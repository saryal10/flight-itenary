from flask import Flask, request, send_file, jsonify
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from io import BytesIO

app = Flask(__name__)

@app.route('/generate-itinerary', methods=['POST'])
def generate_itinerary():
    try:
        data = request.get_json()
        departure_city = data.get('departureCity', 'N/A')
        arrival_city = data.get('arrivalCity', 'N/A')
        departure_date = data.get('departureDate', 'N/A')
        return_date = data.get('returnDate', 'N/A')
        num_passengers = data.get('numPassengers', 'N/A')
        airline = data.get('airline', 'N/A')
        flight_number = data.get('flightNumber', 'N/A')
        booking_reference = data.get('bookingReference', 'N/A')

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        p.drawString(100, 750, "Flight Itinerary")
        p.drawString(100, 730, f"Departure City: {departure_city}")
        p.drawString(100, 710, f"Arrival City: {arrival_city}")
        p.drawString(100, 690, f"Departure Date: {departure_date}")
        if return_date != 'N/A':
            p.drawString(100, 670, f"Return Date: {return_date}")
        p.drawString(100, 650, f"Number of Passengers: {num_passengers}")
        if airline != 'N/A':
            p.drawString(100, 630, f"Airline: {airline}")
        if flight_number != 'N/A':
            p.drawString(100, 610, f"Flight Number: {flight_number}")
        if booking_reference != 'N/A':
            p.drawString(100, 590, f"Booking Reference: {booking_reference}")

        p.showPage()
        p.save()
        buffer.seek(0)

        return send_file(buffer, as_attachment=True, download_name='flight_itinerary.pdf', mimetype='application/pdf')

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return jsonify({'error': 'Failed to generate itinerary on the server'}), 500

if __name__ == '__main__':
    app.run(debug=True)

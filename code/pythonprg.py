import os
import time
import random
import string
import qrcode
from PIL import Image

# Constants
QR_CODE_PATH = "ticket_payment_qr.png"
UPI_ID = "6363759716-2@ibl"
TICKET_PRICES = {
    "The government museum bengaluru": 100,
    "Gandhi bavan bengaluru": 150,
    "Kempegowda museum bengaluru": 200,
    "Venkatappa art gallery bengaluru": 180,
    "NIMHANS brain museum bengaluru": 250,
    "National gallery of modern art bengaluru": 270,
    "HAL heritage centre and aerospce museum bengaluru": 300,
}

TRANSLATIONS = {
    'kn': {
        "The government museum bengaluru": "ಸರ್ಕಾರಿ ಮ್ಯೂಸಿಯಮ್ ಬೆಂಗಳೂರು",
        "Gandhi bavan bengaluru": "ಗಾಂಧಿ ಭವನ ಬೆಂಗಳೂರು",
        "Kempegowda museum bengaluru": "ಕೆಂಪೇಗೌಡ ಮ್ಯೂಸಿಯಮ್ ಬೆಂಗಳೂರು",
        "Venkatappa art gallery bengaluru": "ವೆಂಕಟಪ್ಪ ಆರ್ಟ್ ಗ್ಯಾಲರಿ ಬೆಂಗಳೂರು",
        "NIMHANS brain museum bengaluru": "ನಿಮ್ಹಾನ್ಸ್ ಮೆದುಳು ಮ್ಯೂಸಿಯಮ್ ಬೆಂಗಳೂರು",
        "National gallery of modern art bengaluru": "ನೇಷನಲ್ ಗ್ಯಾಲರಿ ಆಫ್ ಮೋಡರ್ನ್ ಆರ್ಟ್ ಬೆಂಗಳೂರು",
        "HAL heritage centre and aerospce museum bengaluru": "ಎಚ್ಎಎಲ್ ಹೆರಿಟೇಜ್ ಸೆಂಟರ್ ಮತ್ತು ಏರೋಸ್ಪೇಸ್ ಮ್ಯೂಸಿಯಮ್ ಬೆಂಗಳೂರು",
    },
    'hi': {
        "The government museum bengaluru": "सरकारी संग्रहालय बेंगलुरु",
        "Gandhi bavan bengaluru": "गांधी भवन बेंगलुरु",
        "Kempegowda museum bengaluru": "केम्पेगौड़ा संग्रहालय बेंगलुरु",
        "Venkatappa art gallery bengaluru": "वेंकटप्पा आर्ट गैलरी बेंगलुरु",
        "NIMHANS brain museum bengaluru": "निमहांस ब्रेन संग्रहालय बेंगलुरु",
        "National gallery of modern art bengaluru": "नेशनल गैलरी ऑफ मॉडर्न आर्ट बेंगलुरु",
        "HAL heritage centre and aerospce museum bengaluru": "एचएएल हेरिटेज सेंटर और एयरोस्पेस संग्रहालय बेंगलुरु",
    }
}

# Dictionary to keep track of payment status and ticket booking
payment_status = {}
ticket_bookings = {}

class PaymentError(Exception):
    pass

def generate_random_string(length=10):
    """Generate a random string of fixed length"""
    letters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(letters) for _ in range(length))

def generate_qr_code(data):
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(QR_CODE_PATH)
        return True
    except Exception as e:
        print(f"Error generating QR code: {e}")
        return False

def display_qr_code():
    if os.path.exists(QR_CODE_PATH):
        try:
            if os.name == 'nt':  # For Windows
                os.startfile(QR_CODE_PATH)
            elif os.name == 'posix':  # For macOS and Linux
                os.system(f"xdg-open {QR_CODE_PATH}")
        except Exception as e:
            print(f"Unable to automatically open the QR code: {e}")
            print("Please manually open the file to view the QR code.")
    else:
        print("QR code file not found. Please ensure it was generated correctly.")

def make_payment(price, name, payment_method, language='en'):
    transaction_id = generate_random_string()
    payment_link = f"https://paymentgateway.com/confirm_payment?tid={transaction_id}"
    
    if payment_method.lower() == "qr":
        qr_data = payment_link
        if generate_qr_code(qr_data):
            display_qr_code()
            if language == 'en':
                print(f"Transaction ID: {transaction_id}")
            elif language == 'kn':
                print(f"ವಹಿವಾಟು ID: {transaction_id}")
            else:
                print(f"लेन-देन ID: {transaction_id}")
        else:
            raise PaymentError("Failed to generate QR code.")
    
    elif payment_method.lower() == "upi":
        upi_link = f"upi://pay?pa={UPI_ID}&pn={name}&am={price}&cu=INR&tn={transaction_id}"
        if generate_qr_code(upi_link):
            display_qr_code()
            if language == 'en':
                print(f"Please use the following UPI ID to make the payment of Rs{price}: {UPI_ID}")
                print(f"Or use this UPI link on your mobile device: {upi_link}")
                print(f"After completing the payment, confirm it using this link: {payment_link}")
            elif language == 'kn':
                print(f"ದಯವಿಟ್ಟು ಈ UPI ID ಅನ್ನು ಬಳಸಿಕೊಂಡು {price} ರುಪಾಯಿಗಳನ್ನು ಪಾವತಿಸಿ: {UPI_ID}")
                print(f"ಅಥವಾ ನಿಮ್ಮ ಮೊಬೈಲ್ ಸಾಧನದಲ್ಲಿ ಈ UPI ಲಿಂಕ್ ಅನ್ನು ಬಳಸಿ: {upi_link}")
                print(f"ಪಾವತಿಯನ್ನು ಪೂರ್ಣಗೊಳಿಸಿದ ನಂತರ, ಈ ಲಿಂಕ್ ಬಳಸಿಕೊಂಡು ದೃಢೀಕರಿಸಿ: {payment_link}")
            else:
                print(f"कृपया इस UPI ID का उपयोग करके {price} रुपये का भुगतान करें: {UPI_ID}")
                print(f"या अपने मोबाइल डिवाइस पर इस UPI लिंक का उपयोग करें: {upi_link}")
                print(f"भुगतान पूरा करने के बाद, इस लिंक का उपयोग करके इसे पुष्टि करें: {payment_link}")
        else:
            raise PaymentError("Failed to generate QR code.")
    
    # Simulate waiting for payment confirmation
    if language == 'en':
        payment_confirmed = input("Has the payment been completed? (1 for Yes, 2 for No): ").strip() == '1'
    elif language == 'kn':
        payment_confirmed = input("ಪಾವತಿ ಪೂರ್ಣಗೊಂಡಿತೇ? (1 ಹೌದು, 2 ಇಲ್ಲ): ").strip() == '1'
    else:
        payment_confirmed = input("क्या भुगतान पूरा हो गया है? (1 हां के लिए, 2 नहीं के लिए): ").strip() == '1'
    
    if payment_confirmed:
        if language == 'en':
            print("Payment confirmed. Thank you!")
        elif language == 'kn':
            print("ಪಾವತಿ ದೃಢೀಕರಿಸಲಾಗಿದೆ. ಧನ್ಯವಾದಗಳು!")
        else:
            print("भुगतान की पुष्टि हो गई है। धन्यवाद!")
        payment_status[transaction_id] = 'Confirmed'
    else:
        if language == 'en':
            print("Payment not confirmed. Please try again.")
        elif language == 'kn':
            print("ಪಾವತಿ ದೃಢೀಕರಿಸಲಿಲ್ಲ. ದಯವಿಟ್ಟು ಪುನರಾಯಿಸಲು ಪ್ರಯತ್ನಿಸಿ.")
        else:
            print("भुगतान की पुष्टि नहीं हुई है। कृपया पुनः प्रयास करें।")
        payment_status[transaction_id] = 'Pending'
    
    return payment_confirmed, transaction_id

def calculate_ticket_price(destination):
    return TICKET_PRICES.get(destination, 0)

def book_ticket(name, destination, language='en'):
    ticket_id = random.randint(1000, 9999)
    ticket_bookings[ticket_id] = destination  # Track the booking by ticket ID
    if language == 'en':
        print(f"Ticket booked for {name} to {destination}.")
    elif language == 'kn':
        print(f"{name} ರಿಗೆ {TRANSLATIONS['kn'].get(destination, destination)} ಗೆ ಟಿಕೆಟ್ ಬುಕ್ ಮಾಡಲಾಗಿದೆ.")
    else:
        print(f"{name} के लिए {TRANSLATIONS['hi'].get(destination, destination)} का टिकट बुक किया गया है।")
    return ticket_id

def check_ticket_status(ticket_id, language='en'):
    destination = ticket_bookings.get(ticket_id)
    if destination:
        transaction_id = next((tid for tid, dest in ticket_bookings.items() if dest == destination), None)
        status = payment_status.get(transaction_id, 'Pending')
        if language == 'kn':
            status = {"Confirmed": "ದೃಢೀಕರಿಸಲಾಗಿದೆ", "Pending": "ಬಾಕಿ", "Cancelled": "ರದ್ದು"}.get(status, status)
        elif language == 'hi':
            status = {"Confirmed": "पुष्टि", "Pending": "लंबित", "Cancelled": "रद्द"}.get(status, status)
        return status
    else:
        return "Ticket not found." if language == 'en' else "ಟಿಕೆಟ್ ಕಂಡುಬಂದಿಲ್ಲ." if language == 'kn' else "टिकट नहीं मिला।"

def cancel_ticket(ticket_id, language='en'):
    if ticket_id in ticket_bookings:
        transaction_id = next((tid for tid, dest in ticket_bookings.items() if dest == ticket_bookings[ticket_id]), None)
        payment_status[transaction_id] = 'Cancelled'
        del ticket_bookings[ticket_id]
        if language == 'en':
            print(f"Ticket ID {ticket_id} has been cancelled.")
        elif language == 'kn':
            print(f"ಟಿಕೆಟ್ ID {ticket_id} ರದ್ದುಮಾಡಲಾಗಿದೆ.")
        else:
            print(f"टिकट ID {ticket_id} रद्द कर दिया गया है।")
    else:
        if language == 'en':
            print(f"No ticket found for ID {ticket_id}.")
        elif language == 'kn':
            print(f"ID {ticket_id} ರಿಗಾಗಿ ಯಾವುದೇ ಟಿಕೆಟ್ ಪತ್ತೆಯಾಗಲಿಲ್ಲ.")
        else:
            print(f"ID {ticket_id} के लिए कोई टिकट नहीं मिला।")

def select_language():
    print("Select language / ಭಾಷೆ ಆಯ್ಕೆ ಮಾಡಿ / भाषा चुनें:")
    print("1: English")
    print("2: ಕನ್ನಡ")
    print("3: हिन्दी")
    choice = input("Enter your choice / ನಿಮ್ಮ ಆಯ್ಕೆಯನ್ನು ನಮೂದಿಸಿ / अपनी पसंद दर्ज करें: ").strip()
    if choice == '2':
        return 'kn'
    elif choice == '3':
        return 'hi'
    else:
        return 'en'

def display_terms_and_conditions(language):
    if language == 'en':
        print("\nTerms and Conditions:")
        print("1. Visitors must maintain silence.")
        print("2. Visitors should not create any nuisance in the museum.")
        input("Click OK to accept the terms and conditions: ").strip()
    elif language == 'kn':
        print("\nನಿಯಮಗಳು ಮತ್ತು ಷರತ್ತುಗಳು:")
        print("1. ಭೇಟಿ ನೀಡುವವರು ಮೌನವನ್ನು ಕಾಪಾಡಬೇಕು.")
        print("2. ಭೇಟಿದಾರರು ಮ್ಯೂಸಿಯಮ್‌ನಲ್ಲಿ ಯಾವುದೇ ಗಲಾಟೆ ಸೃಷ್ಟಿಸಬಾರದು.")
        input("ನಿಯಮಗಳು ಮತ್ತು ಷರತ್ತುಗಳನ್ನು ಒಪ್ಪಲು OK ಕ್ಲಿಕ್ ಮಾಡಿ: ").strip()
    else:
        print("\nनियम और शर्तें:")
        print("1. आगंतुकों को मौन बनाए रखना चाहिए।")
        print("2. आगंतुकों को संग्रहालय में कोई उपद्रव नहीं करना चाहिए।")
        input("नियम और शर्तों को स्वीकार करने के लिए OK दबाएं: ").strip()

def main():
    language = select_language()
    
    display_terms_and_conditions(language)

    if language == 'en':
        print("Welcome to the Bengaluru Museum Ticket Booking System.")
    elif language == 'kn':
        print("ಬೆಂಗಳೂರು ಮ್ಯೂಸಿಯಮ್ ಟಿಕೆಟ್ ಬುಕ್ಕಿಂಗ್ ವ್ಯವಸ್ಥೆಗೆ ಸ್ವಾಗತ.")
    else:
        print("बेंगलुरु संग्रहालय टिकट बुकिंग प्रणाली में आपका स्वागत है।")

    while True:
        if language == 'en':
            print("\nOptions:")
            print("1: Book a ticket")
            print("2: Check ticket status")
            print("3: Cancel a ticket")
            print("4: Exit")
            choice = input("Enter your choice: ").strip()
        elif language == 'kn':
            print("\nಆಯ್ಕೆಗಳು:")
            print("1: ಟಿಕೆಟ್ ಬುಕ್ ಮಾಡಿ")
            print("2: ಟಿಕೆಟ್ ಸ್ಥಿತಿ ಪರಿಶೀಲಿಸಿ")
            print("3: ಟಿಕೆಟ್ ರದ್ದುಮಾಡಿ")
            print("4: ನಿರ್ಗಮಿಸಿ")
            choice = input("ನಿಮ್ಮ ಆಯ್ಕೆಯನ್ನು ನಮೂದಿಸಿ: ").strip()
        else:
            print("\nविकल्प:")
            print("1: टिकट बुक करें")
            print("2: टिकट की स्थिति जांचें")
            print("3: टिकट रद्द करें")
            print("4: बाहर निकलें")
            choice = input("अपनी पसंद दर्ज करें: ").strip()

        if choice == '1':
            if language == 'en':
                name = input("Enter your name: ").strip()
                print("Available destinations:")
                for idx, destination in enumerate(TICKET_PRICES.keys(), 1):
                    print(f"{idx}: {destination}")
                destination_idx = int(input("Select your destination by number: ").strip()) - 1
            elif language == 'kn':
                name = input("ನಿಮ್ಮ ಹೆಸರು ನಮೂದಿಸಿ: ").strip()
                print("ಲಭ್ಯವಿರುವ ಸ್ಥಳಗಳು:")
                for idx, destination in enumerate(TRANSLATIONS['kn'].values(), 1):
                    print(f"{idx}: {destination}")
                destination_idx = int(input("ನಿಮ್ಮ ಗಮ್ಯಸ್ಥಾನವನ್ನು ಸಂಖ್ಯೆಯಿಂದ ಆಯ್ಕೆ ಮಾಡಿ: ").strip()) - 1
            else:
                name = input("अपना नाम दर्ज करें: ").strip()
                print("उपलब्ध स्थान:")
                for idx, destination in enumerate(TRANSLATIONS['hi'].values(), 1):
                    print(f"{idx}: {destination}")
                destination_idx = int(input("संख्या द्वारा अपना गंतव्य चुनें: ").strip()) - 1

            destination_list = list(TICKET_PRICES.keys())
            destination = destination_list[destination_idx]
            price = calculate_ticket_price(destination)

            if language == 'en':
                print(f"The price for {destination} is Rs{price}.")
            elif language == 'kn':
                print(f"{TRANSLATIONS['kn'][destination]} ಯ ಬೆಲೆ Rs{price} ಆಗಿದೆ.")
            else:
                print(f"{TRANSLATIONS['hi'][destination]} के लिए कीमत Rs{price} है।")

            payment_method = input("Select payment method (QR/UPI): ").strip().lower()
            payment_confirmed, transaction_id = make_payment(price, name, payment_method, language)

            if payment_confirmed:
                ticket_id = book_ticket(name, destination, language)
                if language == 'en':
                    print(f"Your ticket ID is {ticket_id}. Please keep it safe.")
                elif language == 'kn':
                    print(f"ನಿಮ್ಮ ಟಿಕೆಟ್ ID {ticket_id}. ದಯವಿಟ್ಟು ಅದನ್ನು ಸುರಕ್ಷಿತವಾಗಿ ಇಟ್ಟುಕೊಳ್ಳಿ.")
                else:
                    print(f"आपका टिकट ID {ticket_id} है। कृपया इसे सुरक्षित रखें।")

        elif choice == '2':
            ticket_id = int(input("Enter your ticket ID: ").strip())
            status = check_ticket_status(ticket_id, language)
            if language == 'en':
                print(f"Ticket ID {ticket_id} status: {status}.")
            elif language == 'kn':
                print(f"ಟಿಕೆಟ್ ID {ticket_id} ಸ್ಥಿತಿ: {status}.")
            else:
                print(f"टिकट ID {ticket_id} स्थिति: {status}.")
                
        elif choice == '3':
            ticket_id = int(input("Enter your ticket ID: ").strip())
            cancel_ticket(ticket_id, language)

        elif choice == '4':
            if language == 'en':
                print("Thank you for using the Bengaluru Museum Ticket Booking System.")
            elif language == 'kn':
                print("ಬೆಂಗಳೂರು ಮ್ಯೂಸಿಯಮ್ ಟಿಕೆಟ್ ಬುಕ್ಕಿಂಗ್ ವ್ಯವಸ್ಥೆಯನ್ನು ಬಳಸಿದಕ್ಕಾಗಿ ಧನ್ಯವಾದಗಳು.")
            else:
                print("बेंगलुरु संग्रहालय टिकट बुकिंग प्रणाली का उपयोग करने के लिए धन्यवाद।")
            break

        else:
            if language == 'en':
                print("Invalid choice. Please try again.")
            elif language == 'kn':
                print("ಅಮಾನ್ಯ ಆಯ್ಕೆ. ದಯವಿಟ್ಟು ಪುನಃ ಪ್ರಯತ್ನಿಸಿ.")
            else:
                print("अमान्य विकल्प। कृपया पुनः प्रयास करें।")

if _name_ == "_main_":
    main()
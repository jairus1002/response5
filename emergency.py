import sqlite3
import africastalking

# Initialize Africa's Talking
username = "sandbox"  # Use 'sandbox' if using the sandbox environment
api_key = "atsk_7ab5eb7344b16d5b8bb583e8eb49d0d2a18e7b91ff86389f0887366b4dea08ac587b9eae"  # Your Africa's Talking API key

africastalking.initialize(username, api_key)
sms = africastalking.SMS  # Initialize the SMS service

CRITICAL_ISSUES = [
    "fire", 
    "flood", 
    "medical emergency", 
    "serious injury", 
    "severe security threat", 
    "gas leak", 
    "collapsed building", 
    "rape"
]

def send_sms(contact_number, message):
    """Send an SMS message."""
    try:
        sms.send(message, [contact_number])
        print(f"SMS sent to {contact_number}: {message}")
    except Exception as e:
        print(f"Error sending SMS: {str(e)}")

def check_user_response(user_response):
    """Check if the user's response indicates a critical issue."""
    if user_response.lower() in CRITICAL_ISSUES:
        return True
    return False

def get_user_emergency_contact(user_id):
    """Retrieve the emergency contact information for the user from the database."""
    connection = sqlite3.connect('your_database.db')  # Replace with your database file
    cursor = connection.cursor()

    cursor.execute("SELECT emergency_contact, emergency_contact_phone FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()

    connection.close()
    
    if result:
        return result  # Returns a tuple (emergency_contact, emergency_contact_phone)
    else:
        return None

def handle_user_response(user_id, user_response):
    """Handle the user's response and send SMS if it's a critical issue."""
    if check_user_response(user_response):
        emergency_contact_info = get_user_emergency_contact(user_id)
        
        if emergency_contact_info:
            emergency_contact, emergency_contact_phone = emergency_contact_info
            message = f"ALERT: {user_response} reported by {emergency_contact}. Please respond immediately."
            send_sms(emergency_contact_phone, message)
        else:
            print("No emergency contact found for this user.")
    else:
        print("User response is not a critical issue.")

# Example usage
user_id = 1  # Replace with the actual user ID
user_response = "fire"  # Replace with the actual response

handle_user_response(user_id, user_response)

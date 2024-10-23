from flask import Flask, request, render_template, redirect, url_for
import google.generativeai as genai

app = Flask(__name__)

# Configure the Gemini API key
api_key = "AIzaSyB0exgFLLDaljxqXN2qPtQ2AVdDDRLoQaw"
genai.configure(api_key=api_key)

# List of critical issues that require special handling
CRITICAL_ISSUES = ["fire", "flood", "medical emergency", "serious injury", "severe security threat", "gas leak", "collapsed building", "rape"]
MENTAL_HEALTH_ISSUES = ["depression", "anxiety", "mental health", "suicide"]

# List of university contacts for specific departments
UNIVERSITY_CONTACTS = {
    "security": "Campus Security Office: +1234567890",
    "medical": "University Health Services: +1234567891",
    "maintenance": "Facilities and Maintenance: +1234567892",
    "administration": "University Admin Office: +1234567893",
    "mental_health": "University Counseling Services: +1234567894"
}

@app.route('/')
def index():
    return render_template('ai.html', generated_text=None)  # Pass None initially

@app.route('/get_disease_info', methods=['GET', 'POST'])
def get_disease_info():
    if request.method == 'POST':
        issue_type = request.form.get('issue_type')
        details = request.form.get('details').lower()  # Convert details to lowercase for easier matching
        
        # Check if the issue is critical
        if any(critical_issue in details for critical_issue in CRITICAL_ISSUES):
            # Redirect to the report issues dashboard for critical issues
            return redirect(url_for('report_issue_dashboard'))
        
        # Check if it's a mental health issue and provide contacts instead of AI response
        if any(mental_issue in details for mental_issue in MENTAL_HEALTH_ISSUES):
            generated_text = f"Mental health is important. For support, please reach out to {UNIVERSITY_CONTACTS['mental_health']}."
            return render_template("ai.html", generated_text=generated_text)
        
        # Provide specific contacts or procedures for common issues
        if "security" in details:
            generated_text = f"For security concerns, please contact {UNIVERSITY_CONTACTS['security']}."
        elif "medical" in details or "health" in details:
            generated_text = f"For medical assistance, reach out to {UNIVERSITY_CONTACTS['medical']}."
        elif "maintenance" in details or "repair" in details:
            generated_text = f"To report a maintenance issue, contact {UNIVERSITY_CONTACTS['maintenance']}."
        elif "administration" in details or "admin" in details:
            generated_text = f"For administrative concerns, contact {UNIVERSITY_CONTACTS['administration']}."
        else:
            # Use AI to generate responses for non-critical and non-contact issues
            prompt = f"User has reported an issue regarding {issue_type}. Details: {details}. Provide guidance or response in not more than 100 words."
            model = genai.GenerativeModel(model_name="gemini-1.5-flash-exp-0827")
            
            # Generate text using the model
            response = model.generate_content(prompt)
            generated_text = response.text  # Get the generated text
        
        return render_template("ai.html", generated_text=generated_text)  # Pass the generated text to the template
    
    # If GET request, render the form
    return render_template('ai.html', generated_text=None)

@app.route('/report_issue_dashboard')
def report_issue_dashboard():
    # Render a page to allow users to submit critical issues in more detail
    return render_template('critical_issue_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

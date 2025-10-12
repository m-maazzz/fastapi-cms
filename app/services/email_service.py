from fastapi import BackgroundTasks
from app.core.templates import render_template
import smtplib
from email.message import EmailMessage

def send_thank_you_email(name: str, email: str, message: str):
    html_content = render_template("thank_you_email.html", {
        "name": name,
        "email": email,
        "message": message,
    })

    msg = EmailMessage()
    msg["Subject"] = "Thank You for Contacting Us!"
    msg["From"] = "your@email.com"
    msg["To"] = email
    msg.set_content("Thank you for contacting us.")  # Plain text fallback
    msg.add_alternative(html_content, subtype="html")

    # SMTP Example — adjust for your provider
    with smtplib.SMTP("smtp.yourprovider.com", 587) as server:
        server.starttls()
        server.login("dummy@gmail.com", "testing")
        server.send_message(msg)

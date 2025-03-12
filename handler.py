import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json

def send_email(event, context):
    try:
        # Parse the input data from the event
        body = json.loads(event['body'])
        receiver_email = body.get('receiver_email')
        subject = body.get('subject')
        body_text = body.get('body_text')

        if not receiver_email or not subject or not body_text:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'Missing required fields'})
            }

        
        sender_email = 'official.test.mail.13@gmail.com'
        password = 'lpgqfawrqhxpeixc' 

        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body_text, 'plain'))

        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  
        server.login(sender_email, password)

        
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Email sent successfully'})
        }

    except Exception as e:
        print(f'Error: {e}')
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error', 'error': str(e)})
        }

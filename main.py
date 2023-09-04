import requests
from bs4 import BeautifulSoup
import smtplib
import ssl
from email.mime.text import MIMEText

subject = "HAVE SPACE LA DIU"
body = "This is the body of the text message"
sender = "@gmail.com"
recipients = ["@gmail.com", "@gmail.com"]
password = "pw"

# Function to extract course information from the table (same as before)
def extract_course_info(table_row):
    columns = table_row.find_all('td')

    # Check if the number of columns is as expected
    if len(columns) < 6:
        return None

    course_code = columns[0].text.strip()
    course_title = columns[1].text.strip()
    sub_class = columns[2].text.strip()
    quota = int(columns[3].text.strip())
    vacancies = int(columns[4].text.strip())
    applicants = int(columns[5].text.strip())

    return {
        'course_code': course_code,
        'course_title': course_title,
        'sub_class': sub_class,
        'quota': quota,
        'vacancies': vacancies,
        'applicants': applicants
    }


# Function to send an email notification
def send_email_notification(course_code, vacancies, applicants):
    subject = f'Course {course_code} - Finally have place la diu!'
    body = f'The course {course_code} has a place available!\n\n' \
           f'Vacancies: {vacancies}\n' \
           f'Applicants: {applicants}'
    message = f'Subject: {subject}\n\n{body}'

    context = ssl.create_default_context()
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

def send_email_notification_no_place():
    subject = f'NO PLACE AH DIU!'
    body = "No place ah diu!"
    message = f'Subject: {subject}\n\n{body}'

    context = ssl.create_default_context()
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")    

def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = ', '.join(recipients)
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
       smtp_server.login(sender, password)
       smtp_server.sendmail(sender, recipients, msg.as_string())
    print("Message sent!")

# Function to monitor course changes (same as before)
def monitor_course_changes():
    url = 'https://sweb.hku.hk/ccacad/ccc_appl/enrol_stat.html'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table')
    table_rows = table.find_all('tr')

    course_data = []
    for row in table_rows[1:]:
        course_info = extract_course_info(row)
        if course_info:
            course_data.append(course_info)

    # Find the specific courses of interest
    course_1 = next((course for course in course_data if course['course_code'] == 'CCGL9074'), None)
    course_2 = next((course for course in course_data if course['course_code'] == 'CCCH9031'), None)

    # Check for changes in the columns
    if course_1 and course_2:
        if course_1['vacancies'] != 0 or course_1['applicants'] != 0:
            print('CCGL9074 has changed!')
            print('Previous Vacancies:', course_1['vacancies'])
            print('Previous Applicants:', course_1['applicants'])
            print('Current Vacancies:', course_1['vacancies'])
            print('Current Applicants:', course_1['applicants'])

            # Send email notification
            send_email_notification(course_1['course_code'], course_1['vacancies'], course_1['applicants'])

        if course_2['vacancies'] != 0 or course_2['applicants'] != 0:
            print('CCCH9031 has changed!')
            print('Previous Vacancies:', course_2['vacancies'])
            print('Previous Applicants:', course_2['applicants'])
            print('Current Vacancies:', course_2['vacancies'])
            print('Current Applicants:', course_2['applicants'])

            # Send email notification
            send_email_notification(course_2['course_code'], course_2['vacancies'], course_2['applicants'])
        else: 
            send_email_notification_no_place()
# Run the monitoring function
monitor_course_changes()
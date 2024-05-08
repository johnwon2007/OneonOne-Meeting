from .models.availability import Availability
from .models.meetingAvailability import MeetingAvailability
from datetime import timedelta
from typing import List

import smtplib
from email.mime.text import MIMEText

def SuggestionTimes(calendar_availabilities: List[Availability],
                    meeting_availabilities: List[MeetingAvailability],
                    meeting_duration: int):
    intersections = []
    for c_avail in calendar_availabilities:
        for m_avail in meeting_availabilities:
            c_start = c_avail.start_time
            c_end = c_avail.end_time
            m_start = m_avail.start_time
            m_end = m_avail.end_time

            # Finding the overlapping time
            start_max = max(c_start, m_start)
            end_min = min(c_end, m_end)

            if start_max < end_min and (end_min - start_max) >= timedelta(
                    minutes=meeting_duration):
                # There's an overlapping slot that can accommodate the meeting
                intersection = {
                    "start_time": start_max,
                    "end_time": end_min,
                    "preference": c_avail.preference + m_avail.preference
                }
                intersections.append(intersection)
                intersections.sort(
                    key=lambda x: (-x['preference'], x['start_time']))

    if intersections:
        best_slot = intersections[0]
        print(intersections)
        return {
            "start_time": best_slot['start_time'].strftime(
                "%Y-%m-%dT%H:%M:%SZ"),
            "end_time": (best_slot['start_time'] + timedelta(
                minutes=meeting_duration)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "preference": best_slot['preference']
        }

    return {}


smtp_server = "smtp-mail.outlook.com"
smtp_port = 587
username = "oneononealert@outlook.com"
password = "whddms0301!"
email_from = "oneononealert@outlook.com"

def SendEmail(email_to: str, inviter: str, meeting_title: str, url: str):
    email_subject = f'NEW MEETING INVITE: {meeting_title}'
    co_msg = f'Hey. You have been invited to a Meeting: "{meeting_title}" with {inviter}. \n Click the link below for more details. \n {url}'
    msg = MIMEText(co_msg)
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = email_to
    debuglevel = True
    mail = smtplib.SMTP(smtp_server, smtp_port)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(email_from, email_to, msg.as_string())
    mail.quit()


def SendNotification(email_to: str, inviter: str, meeting_title: str, url: str):
    email_subject = f'MEETING REMINDER: {meeting_title}'
    co_msg = f'Hey. {inviter} is waiting for you to book the meeting.\n Click the link below for more details. \n {url}'
    msg = MIMEText(co_msg)
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = email_to
    debuglevel = True
    mail = smtplib.SMTP(smtp_server, smtp_port)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(email_from, email_to, msg.as_string())
    mail.quit()


def SendFinalizedEmail(email_to: str, email_other: str, meeting_title: str, location: str, meeting_time):
    email_subject = f'MEETING CONFIRMATION: {meeting_title}'
    co_msg = f'The Meeting: {meeting_title} with {email_other} has been confirmed at {location}, {meeting_time}.\n'
    msg = MIMEText(co_msg)
    msg['Subject'] = email_subject
    msg['From'] = email_from
    msg['To'] = email_to
    debuglevel = True
    mail = smtplib.SMTP(smtp_server, smtp_port)
    mail.set_debuglevel(debuglevel)
    mail.starttls()
    mail.login(username, password)
    mail.sendmail(email_from, email_to, msg.as_string())
    mail.quit()

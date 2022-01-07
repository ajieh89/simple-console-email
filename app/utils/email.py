import pandas as pd
import numpy as np
import os
import smtplib
import json

from email.message import EmailMessage
from dotenv import load_dotenv
from datetime import datetime as dt
from helpers.helpers import get_absolute_url, multiple_replace

EMAIL_TEMPLATE_KEYS = [ 'to', 'from', 'subject', 'mimeType', 'body' ]

class EmailClass(object):
    def __init__(self, template_path, customer_path, output_path, error_path):
        load_dotenv()
        self.template_data = get_absolute_url(template_path)
        self.customer_data = get_absolute_url(customer_path)
        self.output_path = get_absolute_url(output_path)
        self.error_path = get_absolute_url(error_path)
        self.email_paths= []

        self.smtp_host = os.environ.get('SMTP_HOST')
        self.smtp_port = os.environ.get('SMTP_PORT')
        self.smtp_username = os.environ.get('SMTP_USERNAME')
        self.smtp_password = os.environ.get('SMTP_PASSWORD')

    @property
    def template_data(self):
        return self._template_data

    @template_data.setter
    def template_data(self, value):
        try:
            self._template_data = pd.read_json(value, orient='index')

            if not sorted(self._template_data.index) == sorted(EMAIL_TEMPLATE_KEYS):
                raise KeyError('Email template must contained keys: {}'.format(', '.join(EMAIL_TEMPLATE_KEYS)))
        except Exception as e:
            raise Exception('Failed to load email template provided: {}'.format(e))


    @property
    def customer_data(self):
        return self._customer_data

    @customer_data.setter
    def customer_data(self, value):
        try:
            self._customer_data = pd.read_csv(value)
        except pd.errors.ParserError as e:
            raise Exception('Failed to load customer data provided: {}'.format(e))


    def process_email_content(self) -> bool:
        try:
            state = False
            invalid_email = self._customer_data[self._customer_data.EMAIL.isnull()]
            valid_email = self._customer_data[self._customer_data.EMAIL.notnull()]

            if not invalid_email.empty:
                # WRITING THE INVALID EMAIL INTO ERROR CSV FILE PATH PROVIDED
                invalid_email.to_csv(self.error_path, index=False)

            if not valid_email.empty:
                # PROCESS THE CUSTOMER DATA WITH THE EMAIL TEMPLATE
                for customer in valid_email.itertuples(name="Customer", index=False):

                    json_content = self._template_data[0]
                    customer = customer._asdict()

                    json_content['to'] = customer['EMAIL']

                    str_to_replace = customer

                    str_to_replace['TODAY'] = dt.now().strftime('%d %b %Y')

                    json_content['body'] = multiple_replace(json_content['body'], str_to_replace)

                    file_name = '{email}_{timestamp}.json'.format(
                        email=customer['EMAIL'],
                        timestamp=dt.now().timestamp()
                    )
                    file_path = os.path.join(self.output_path, file_name)

                    if not os.path.isdir(self.output_path):
                        os.mkdir(self.output_path)

                    json_content.to_json(file_path , indent=4)
                    self.email_paths.append(file_path)

                state = True
        except pd.errors.ParserError as e:
            print('[ERROR] process data with pandas: {}'.format(e))
        except Exception as e:
            print('[ERROR] process email content: '.format(e))
        finally:
            return state


    def send_email(self)->bool:
        try:
            for mp in self.email_paths:
                with open(mp) as json_file:
                    data = json.load(json_file)

                    with smtplib.SMTP(self.smtp_host, self.smtp_port) as smtp:
                        smtp.starttls()
                        # smtp.login(self.smtp_username, self.smtp_password)
                        smtp.login('lim.zan.jieh@spectos.com', 'jieh8911070704')
                        # construct the email content
                        email = EmailMessage()
                        email['Subject'] = data.get('subject')
                        email['From'] = data.get('from')
                        email['To'] = data.get('to')
                        email.add_header('Content-Type', data.get('mimeType'))
                        email.set_payload(data.get('body'))

                        smtp.send_message(email)
                        os.remove(mp)

        except smtplib.SMTPException as e:
            print("[ERROR] STMPException: {}".format(e))
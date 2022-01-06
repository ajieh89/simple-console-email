import pandas as pd
import numpy as np
import json
import csv

from datetime import datetime as dt
from helpers.helpers import get_absolute_url, muiltple_replace

EMAIL_TEMPLATE_KEYS = [  'to', 'from', 'subject', 'mimeType', 'body' ]

class EmailGenerator():
    def __init__(self, template_path, customer_path, output_path, error_path):
        self.template_data = get_absolute_url(template_path)
        self.customer_data = get_absolute_url(customer_path)
        self.output_path = get_absolute_url(output_path)
        self.error_path = get_absolute_url(error_path)
        self.today = dt.now().strftime('%d %b %Y')

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


    def process_email_content(self) -> str:
        try:
            results = []
            customer_keys = self._customer_data.columns
            invalid_email = self._customer_data[self._customer_data.EMAIL.isnull()]
            valid_email = self._customer_data[self._customer_data.EMAIL.notnull()]

            if not invalid_email.empty:
                # WRITING THE INVALID EMAIL INTO ERROR CSV FILE PATH PROVIDED
                invalid_email.to_csv(self.error_path)

            if not valid_email.empty:
                # PROCESS THE CUSTOMER DATA WITH THE EMAIL TEMPLATE
                for customer in self._customer_data.itertuples(name="Customer", index=False):
                    json_content = self._template_data[0]
                    customer = customer._asdict()

                    json_content['to'] = customer['EMAIL']

                    str_to_replace = customer

                    str_to_replace['TODAY'] = self.today


                    json_content['body'] = muiltple_replace(json_content['body'], str_to_replace)

                    print(json_content)

        # for row in self._customer_data.itertuples():
            #     content = self._template_data

            #     if '{{TODAY}}' in content['body']:
            #         content['body'] = content['body'].replace('{{TODAY}}', self.today)

            #     row_dict = row._asdict()

            #     print('E: {}'.format(row_dict.get('EMAIL', None)))


            #     for rkey in customer_keys:
            #         if rkey == 'EMAIL':
            #             content['to'] = row_dict[rkey]


            #         str_to_replace = '{{' + rkey + '}}'
            #         if str_to_replace in content['body']:
            #             content['body'] = content['body'].replace(str_to_replace, row_dict[rkey])

            #     results.append(content)
            # print(results)
        except pd.errors.ParserError as e:
            print('[ERROR] process data with pandas: {}'.format(e))
        except Exception as e:
            print('[ERROR] process email content: '.format(e))

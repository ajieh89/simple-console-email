import os
import logging
import argparse

from utils.email_generator import EmailGenerator



parser = argparse.ArgumentParser(description='sending email')
parser.add_argument('-t', metavar='template', default=None, help='email template that define the sending format')
parser.add_argument('-r', metavar='customer', default=None, help='csv file path contain list of customers')
parser.add_argument('-o', metavar='output', default='output/output_emails', help='output file path that allow system to writ')
parser.add_argument('-e', metavar='error', default='output/error.csv', help='error file path that allow system to write')

args = vars(parser.parse_args())

try:
    email_template = args['t']

    if not email_template:
        raise ValueError('email template is required')

    customers_file = args['r']

    if not customers_file:
        raise ValueError('customer file is required')

    output_file = args['o']
    error_file = args['e']

    email_genarator = EmailGenerator(email_template, customers_file, output_file, error_file)

    email_genarator.process_email_content()

except KeyError as e:
    print('Invalid arguments: {}'.format(e))
except ValueError as e:
    print('Invalid Value: {}'.format(e))
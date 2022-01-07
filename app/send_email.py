import argparse

from utils.email import EmailClass

parser = argparse.ArgumentParser(description='sending email')
parser.add_argument('-t', metavar='template', default=None, help='email template that define the sending format')
parser.add_argument('-r', metavar='customer', default=None, help='csv file path contain list of customers')
parser.add_argument('-o', metavar='output', default='output/emails/', help='output file path that allow system to writ')
parser.add_argument('-e', metavar='error', default='output/errors.csv', help='error file path that allow system to write')
parser.add_argument('-s', metavar='send_email', default='N' , help='Y to send email, N not send email')

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

    email = EmailClass(email_template, customers_file, output_file, error_file)

    state = email.process_email_content()

    if state:
        if args['s'] == 'Y':
            print('[Message] Sending Email')
            email.send_email()
        else:
            print('[Success] All email content generate and store at {}'.format(email.output_path))
    else:
        print('[Failed] Something went wrong, contact the support for assist')
except KeyError as e:
    print('[Error] Invalid arguments: {}'.format(e))
except ValueError as e:
    print('[Error] Invalid value: {}'.format(e))
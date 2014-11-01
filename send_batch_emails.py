# coding=utf-8
__author__ = 'pshort'

def send_email(recipient, **data):
    import smtplib

    gmail_user = "<email_address>"
    gmail_pwd = "<app_passwords>"
    FROM = '<email_address>'
    TO = [recipient]  # must be a list
    SUBJECT = data['subject']
    TEXT = data['body']

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
    """ % (FROM, ", ".join(TO), SUBJECT, TEXT)

    server = smtplib.SMTP("smtp.gmail.com", 587)  # or port 465 but it doesn't seem to work!
    server.ehlo()
    server.starttls()
    server.login(gmail_user, gmail_pwd)
    server.sendmail(FROM, TO, message)
    server.close()
    print 'Sending email to %s' %recipient
    return


def _read_csv(filename='csv_file_with_names_emails_etc.csv'):
    import csv
    return csv.DictReader(open(filename, 'rU'))

email_body = """

Dear %s (will be name from csv file)

Long message here...

May insert extra %s (details) from csv.

Sincerely,
Patrick

"""


if __name__ == '__main__':
    # Example for sending confirmation of an order with records in csv
    for line in _read():
        recipient = line['Email Address']
        if line['Shipping Address']:
            ship_address = "\n" + line['Shipping Address']
            ship_details = """Our records indicate that you requested shipping. Here is the address we have on file:\n%s""" % ship_address
        else:
            ship_address = ""
            ship_details = "Our records indicate that you prefer to pick the t-shirts up. If this is not the case, please " \
                           "respond to me with a preferred shipping address. Otherwise, please let me know if you would" \
                           "prefer to pick the shirt up or have it dropped off to you."
        sizes = []
        num = []
        for size in ['Shirt Order [Small]',	'Shirt Order [Medium]',	'Shirt Order [Large]',	'Shirt Order [XL]']:
            try:
                if int(line[size]) > 0:
                    sizes.append(size.split('[')[-1][:-1])
                    num.append(line[size])
            except ValueError:
                pass
        order_str = "".join([j + " " + i + '\n' for i, j in zip(sizes, num)])

        data = {'subject': 'Alumni T-Shirt Order Confirmation', 'body': email_body % (order_str, ship_details)}
        send_email(recipient, **data)


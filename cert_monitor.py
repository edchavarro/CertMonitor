import OpenSSL, time
import ssl, socket
import smtplib
import argparse

#SMTP configuration parameters
from_addr='myemailaccount@gmail.com' 
smtpserver='smtp.gmail.com'             #Configure your SMTP server
login="myemailaccount"                #Configure your own credentials
password="mysecurepassword"               #Configure your own credentials    
to_addr_list=['myemailaccount@gmail.com'] #Configure all the email addresses yo want to be informed as To
cc_addr_list = ['myotheremailaccount@gmail.com']              #Configure all the email addresses yo want to be informed as CC


url=''
port=443

def smtpsend(subject, message):
    header  = 'From: %s\n' % from_addr
    header += 'To: %s\n' % ','.join(to_addr_list)
    header += 'Cc: %s\n' % ','.join(cc_addr_list)
    header += 'Subject: %s\n\n' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    print message
    problems = server.sendmail(from_addr, to_addr_list, message)
    print problems
    server.quit()

def notify(diff, x509):
    date_=x509.get_notAfter()
    issuer=x509.get_issuer()
    subjectc=x509.get_subject()
    subject='[Alert] '
    if diff < 30: subject='[Urgent] '
    subject=subject+ ' Iminent certificate expiration ' + url
    message='\nCertificate ' + str(subjectc) + ' will expire on ' + str (diff) + ' days.\n' 
    message=message + '\n\t Issuer: ' + str(issuer)
    message=message + '\n\t Subject: ' + str(subjectc)
    message=message + '\n\t Domain: ' + url
    message=message + '\n\t Port: ' + str(port)
    print "Start mail notification ..."
    smtpsend(subject,message)
    
parser = argparse.ArgumentParser(description='Certificate monitor for iminent expiration.')
parser.add_argument('-d','--domain', help='Domain to analyze', required=True)
parser.add_argument('-p','--port', help='Domin port for cert analysis, default 443', required=False, default='443')
args = parser.parse_args()
argsdict = vars(args)
url = argsdict['domain']
port = argsdict['port']

cert=ssl.get_server_certificate((url, port))
x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
if x509.has_expired():
    smtpsend("Certificate expired for " + url,"Certificate expired. \n Please update it ASAP.")
else:
    date_=x509.get_notAfter()[0:8]
    t = time.strftime("%Y,%m,%d").split(',')
    now = [ int(x) for x in t ]

    yeard=  now[0] - int(date_[0:4]) 
    monthd= now[1] - int(date_[5:6]) 
    dayd=   now[2] - int(date_[7:8]) 

    diff= yeard*365 + monthd * 30 + dayd

    if diff <= 60:
        notify(diff,x509)


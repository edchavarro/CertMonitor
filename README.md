# CertMonitor
This is a script for monitoring certificates date of expiration.

Usage:

  python cert_monitor.py -d <domain>
  
Parameters:

  -d  --domain  Domain or IP address to analyze
  -p  --port    Port to test.

Results:

  This script will verify if the expiration date of the certificate is lower than 60 days, if so, it will send an email to these addresses configured in the to_addr_list and cc_addr_list.
  
Example:

python cert_monitor.py -d barcamp.se
Start mail notification ...  
From: ***@gmail.com
To: ***@gmail.com
Cc: ***@csiete.org
Subject: [Alert]  Iminent certificate expiration servidoranonimo.org

Certificate <X509Name object '/CN=servidoranonimo.org'> will expire on 59 days.

           Issuer: <X509Name object '/C=US/ST=TX/L=Houston/O=cPanel, Inc./CN=cPanel, Inc. Certification Authority'>
           Subject: <X509Name object '/CN=servidoranonimo.org'>
           Domain: barcamp.se
           Port: 443
 

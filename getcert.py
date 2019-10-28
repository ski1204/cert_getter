import OpenSSL
import socket
import ssl
import csv
import signal

from datetime import datetime

yearDays = 365
certPort = '443'

#socket timeout wasnt working like I thought it should.
class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException

# Change the behavior of SIGALRM
signal.signal(signal.SIGALRM, timeout_handler)

print("Cert script started")

today = datetime.today()
todaydate = today.strftime("%b-%d-%Y")
print("today's date", todaydate)

#create file to write to
certFileNameUrgent = "certificateReport_URGENT_" + todaydate + ".csv"
certFileNameWarning = "certificateReport_WARNING_" + todaydate + ".csv"
f = open(certFileNameUrgent, "w+")
f = open(certFileNameWarning, "w+")

#open file that had subdomains

with open('subdomainsOnly.csv', 'rt') as f:
    reader = csv.reader(f)
    subdomainsList = list(reader)

#loop subdomains
for i in range(len(subdomainsList)):
    domainStr = subdomainsList[i]

    errorMsg = ''
    signal.alarm(8)
    try:
        cert=ssl.get_server_certificate((domainStr[0], certPort))
        x509 = OpenSSL.crypto.load_certificate( OpenSSL.crypto.FILETYPE_PEM, cert )
        expirationDate = x509.get_notAfter()
        #compareDate #compare against 365 days
        certExp = x509.get_notAfter() #YYYYMMDDhhmmssZ ASN1 GENERALIZEDTIME
        certExpDate = certExp[:8] #YYYYMMDD
        expirationDate = datetime.strptime(certExpDate, '%Y%m%d')
        diff = expirationDate - today
        if diff.days < 0:
            f = open(certFileNameUrgent, "a")
            f.write("Domain: " + domainStr[0] + " SSL cert expired for " + str(diff.days*-1) + " days\n")
            f.close()
            continue
        if diff.days < yearDays:
            f = open(certFileNameWarning, "a")
            f.write("Domain: " + domainStr[0] + " SSL cert expires in " + str(diff.days) + " days\n")
            f.close()
            continue
    except socket.gaierror as e:
        errorMsg = str(e)
        print('socket exepetion thrown around domain: ' + domainStr[0])
    except socket.error as e:
        errorMsg = str(e)
        print('socket exepetion thrown around domain: ' + domainStr[0])
    except TimeoutException:
        errorMsg = 'socket timed out'
        print(errorMsg)
        continue

    f = open(certFileNameUrgent, "a")
    f.write("Domain: " + domainStr[0] + " SSL cert Error: " + errorMsg + " \n")
    f.close()
    signal.alarm(0)


print('script is done')
exit()
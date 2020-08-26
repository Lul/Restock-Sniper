from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from email.mime.text import MIMEText
import os, sys, smtplib, time, configparser

class InStockChecker:
    def __init__(self):
        self.email = ''
        self.password = ''
        self.smtp_server = ''
        self.port = ''
        self.receiver = ''
        self.receiver2 = ''
        self.mode = 0
        self.config = ''
        
    def configuration(self):
        self.email = input('Login Email: ')
        if self.email[int(self.email.find('@') + 1):] == 'gmail.com':
            self.smtp_server = 'smtp.gmail.com'
            self.port = 587
        elif self.email[int(self.email.find('@') + 1):] == 'outlook.com' or self.email[int(self.email.find('@') + 1):] == 'live.com' or self.email[int(self.email.find('@') + 1):] == 'hotmail.com':
            self.smtp_server = 'smtp.office365.com'
            self.port = 587
        elif self.email[int(self.email.find('@') + 1):] == 'yahoo.com' or self.email[int(self.email.find('@') + 1):] == 'rocketmail.com':
            self.smtp_server = 'smtp.mail.yahoo.com'
            self.port = 587
        else:
            redo = input('Email domain not recognized. Please enter your SMTP server information, or enter 1 to restart.\n')
            if redo == '1':
                self.configuration()
            else:
                self.smtp_server = input('SMTP Server: ')
                try:
                    self.port = int(input('Port: '))
                except: 
                    print('Improper input, try again.')
                    self.configuration()
                    self
        self.password = input('Password: ')
    
    def mode_select(self):
        carrier_list = ['@txt.att.net', '@sms.boostmobile.com', 'mms.cricketwireless.net', '@msg.fi.google.com', '@messaging.sprintpcs.com', '@vtext.com', '@tmomail.net', '@vtext.com', '@vmobl.com']
        try:
            tc = int(input('1. Text only\n2. Email self\n3. Text & Email\n\nSelect mode: '))
        except:
            print('Improper input, try again.')
            self.mode_select()
        if tc == 1:
            try:
                number = input('Phone number: ')
            except:
                print('Improper input, try again.')
                self.mode_select()
            print('1. AT&T\n2. Boost Mobile\n3. Cricket Wireless\n4. Google Project Fi\n5. Sprint\n6. Straight Talk\n7. T-Mobile\n8. Verizon\n9. Virgin Mobile')
            try:
                carrier = int(input('Select your carrier: '))
            except:
                print('Improper input, try again.')
                self.mode_select()
            self.mode = 1
            self.receiver = str(number + carrier_list[int(carrier - 1)])
        elif tc == 2:
            self.mode = 2
            self.receiver = self.email
        elif tc == 3:
            try:
                number = input('Phone number: ')
            except:
                print('Improper input, try again.')
                self.mode_select()
            print('1. AT&T\n2. Boost Mobile\n3. Cricket Wireless\n4. Google Project Fi\n5. Sprint\n6. Straight Talk\n7. T-Mobile\n8. Verizon\n9. Virgin Mobile')
            try:
                carrier = int(input('Select your carrier: '))
            except:
                print('Improper input, try again.')
                self.mode_select()
            self.mode = 3
            self.receiver = str(number + carrier_list[int(carrier - 1)])
            self.receiver2 = self.email
        
    def notify(self, receiver, message):
        msg = MIMEText(str(message))
        server = smtplib.SMTP(self.smtp_server, self.port)
        server.starttls()
        server.login(self.email, self.password)
        server.send_message(msg, self.email, receiver)
        server.quit()

    def load_settings(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.email = self.config['SETTINGS']['email']
        self.password = self.config['SETTINGS']['password']
        self.smtp_server = self.config['SETTINGS']['smtp_server']
        self.port = self.config['SETTINGS']['smtp_server']

    def save_settings(self):
        self.config = configparser.ConfigParser()
        self.config.read('settings.ini')
        self.config['SETTINGS']['email'] = self.email
        self.config['SETTINGS']['password'] = self.password
        self.config['SETTINGS']['smtp_server'] = self.smtp_server
        self.config['SETTINGS']['port'] = str(self.port)
        with open('settings.ini', 'w') as filewrite:
            self.config.write(filewrite)

if not os.path.isfile('geckodriver.exe') and not os.path.isfile('chromedriver.exe') and not os.path.isfile('IEDriverServer.exe'):
    print('Webdriver not found. Go to "https://pypi.org/project/selenium/" and download the proper webdriver for your browser of choice, and copy the .exe into %s' % os.getcwd())
    tixe = input('Press enter to exit.')
    if tixe:
        sys.exit()
        
weblist = []
unsupportedsites = []

with open('websites.txt','r') as websites:
    sites = websites.read().split()
    with open('websites.bak', 'w') as backup:
        for site in sites:
            backup.write(site + '\n')
    with open('supportedsites.txt','r') as supsites:
        supportedsites = supsites.read().split()
        for i in sites:
            weblist.append(i.strip('http://').strip('https://').strip('www.'))
        for i,n in enumerate(weblist):
            weblist[i] = n[:int(n.find('/'))]

for i in weblist:
    if not i in supportedsites:
        unsupportedsites.append(i)
if len(unsupportedsites) > 0:
    print('The following websites are not in supportedsites.txt:')
    for i in unsupportedsites:
        print(i)
    print('Add websites to supportedsites.txt. Additionally, ensure definitions.txt is updated with proper class name.')
    tixe = input('Press enter to exit.')
    if tixe:
        sys.exit()

print('[Restock Sniper by: John]\n[Version: 1.0]\n\nStarting web driver..')
try:
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options, executable_path='geckodriver.exe')
except Exception as e:
    print('Error occured: ' + e.__doc__ + '\n')
    tixe = input('Press enter to exit')
    if tixe:
        sys.exit()
driver.get('https://raw.githubusercontent.com/Lul/Restock-Sniper/master/version.txt')
versioncheck = driver.page_source.strip('<html><head><link rel="stylesheet" href="resource://content-accessible/plaintext.css"></head><body><pre>').strip('</pre></body></html>')
with open('version.txt','r') as ver:
    check = ver.read()
if check != versioncheck:
    print('Update available for this program, supported sites, or definitions. Please check out https://www.GitHub.com/Lul/Restock-Sniper for the newest version')
    cont = input('Continue with program? [Y/N]\n\n')
    if 'y' in cont or 'Y' in cont:
        None
    else:
        tixe = input('Press enter to exit.')
        sys.exit()
        
isc = InStockChecker()
isc.load_settings()

if isc.config['SETTINGS']['email'] == '':
    flushsettings = input('Previous session detected, do you want to use same login credentials? [Y/N]\n\n')
    if 'y' in flushsettings or 'Y' in flushsettings:
        isc.email = isc.config['SETTINGS']['email']
        isc.password = isc.config['SETTINGS']['password']
        isc.smtp_server = isc.config['SETTINGS']['smtp_server'] 
        isc.port = isc.config['SETTINGS']['port']
    else:
        isc.configuration()
        isc.save_settings()
else:    
    isc.configuration()
    isc.save_settings()
    
isc.mode_select()

defcount = 0
httpreplace = ['http://','https://','http://www.','https:///www.']

print('Running... press ctrl+c to exit.')

while True:
    try:
        with open('websites.txt', 'r+') as sitelist:
            sites = sitelist.read().split()
            with open('websites.bak', 'w') as backup:
                for site in sites:
                    backup.write(site + '\n')
            for i in sites:
                tm = str(i)
                driver.get(i)
                time.sleep(2)
                with open('definitions.txt', 'r') as x:
                    definitionlist = x.read().split()
                    for definition in definitionlist:
                        try:
                            if driver.find_element_by_class_name(definition):
                                defcount = 0
                                driver.delete_all_cookies()
                                break
                        except:
                            defcount+=1
                            driver.delete_all_cookies()
                    if defcount == int(len(definitionlist) * 2):
                        if isc.mode == 1 or isc.mode == 2:
                            for hr in httpreplace:
                                if hr in tm:
                                    tm = tm.replace(hr,'')
                                    isc.notify(receiver=isc.receiver, message=str('%s\nNOW IN STOCK\n' % tm))
                                    sitelist.seek(0)
                                    for line in sites:
                                        if line != i:
                                            sitelist.write(line + '\n')
                                    sitelist.truncate()
                                else:
                                    isc.notify(receiver=isc.receiver, message=str('%s\nNOW IN STOCK\n' % tm))
                                    sitelist.seek(0)
                                    for line in sites:
                                        if line != i:
                                            sitelist.write(line + '\n')
                                    sitelist.truncate()
                        elif isc.mode == 3:
                            for hr in httpreplace:
                                if hr in str(i):
                                    tm = tm.replace(hr,'')
                                    isc.notify(receiver=isc.receiver, message=str('%s\nNOW IN STOCK\n' % tm))
                                    isc.notify(receiver=isc.receiver2, message=str('%s\nNOW IN STOCK\n' % tm))
                                    sitelist.seek(0)
                                    for line in sites:
                                        if line != i:
                                            sitelist.write(line + '\n')
                                    sitelist.truncate()
                                else:
                                    isc.notify(receiver=isc.receiver, message=str('%s\nNOW IN STOCK\n' % tm))
                                    isc.notify(receiver=isc.receiver2, message=str('%s\nNOW IN STOCK\n' % tm))
                                    sitelist.seek(0)
                                    for line in sites:
                                        if line != i:
                                            sitelist.write(line + '\n')
                                    sitelist.truncate()
    except KeyboardInterrupt:
        sys.exit()
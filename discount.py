import requests, random, json, datetime, time, os
from imap_tools import AND, MailBox
from colorama import Fore
from os import name

# Function to get the time and date in a specific format
def getTime():
    monthList = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    currentMonth = monthList[int(str(datetime.datetime.today()).split('-')[1].split('-')[0].strip('0')) - 1]
    currentDay = str(datetime.datetime.today()).split('-')[2].split(' ')[0]

    return f"{currentMonth} {currentDay} @ {str(datetime.datetime.today()).split(' ')[1].split('.')[0]}"

# Print out message in a specific format
def Logger(message, taskNumber, color):
    print(Fore.WHITE + f"    {getTime()} || {color}ZALANDO-DISCOUNT{Fore.WHITE} || {color}{taskNumber}{Fore.WHITE} || {color}{message}{Fore.RESET}")

# Class genning discounts and then also fetching the discounts
class Gen:
    # Function to gen a random email with catchall
    def genEmail(self):
        # List with random names
        names = ['Alessandro', 'Riccardo', 'Diego', 'Tommaso', 'Matteo', 'Lorenzo', 'Gabriele', 'Samuele', 'Giacomo', 'beatrice', 'sofia', 'ginevra', 'gaia', 'Rossi', 'Ferrari', 'Russo', 'Bianchi', 'Romano', 'Gallo', 'Costa', 'Fontana', 'conti', 'esposito','ricci', 'bruno', 'greco']

        # Get random number
        RandomNum = str(random.randint(1111, 9999))
        # Get random name from list
        RandomName = str(random.choice(names))

        # Create email with random names and number using user catchall
        self.email = RandomName + RandomName + RandomNum + self.catchall


    # Function to get a random proxy from 'proxies.txt'
    def getProxy(self):
        try:
            # Open proxy file
            with open('proxies.txt', 'r') as reader:
                Proxies = reader.read().splitlines()

            # Check proxies are loaded
            if len(Proxies) == 0:
                Logger("No proxies loaded, running on local", self.taskNum, Fore.LIGHTRED_EX)
                self.proxy = None
                return

            # Grab random proxy
            randomProxy = random.choice(Proxies)
            # Set proxy adjusted for requests format
            self.proxy = {
                "http": f"http://{randomProxy.split(':')[2]}:{randomProxy.split(':')[3]}@{randomProxy.split(':')[0]}:{randomProxy.split(':')[1]}",
                "https": f"http://{randomProxy.split(':')[2]}:{randomProxy.split(':')[3]}@{randomProxy.split(':')[0]}:{randomProxy.split(':')[1]}"
            }
        except Exception:
            Logger('Error getting proxy', self.taskNum, Fore.LIGHTRED_EX)
            self.proxy = None

    # Function to gen the discount from zalando using requests
    def genDiscount(self):
        # Request "info"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
            'Content-Type': 'application/json',
        }
        payload = {
            "id": "06fe5b50b4218612aa3fa8494df326aef7ff35a75a8563b3455bb53c15168872",
            "variables": {
            "input": {
                "email": self.email,
                "preference": {
                    "category": "MEN",
                    "topics": [
                        {
                            "id": "item_alerts",
                            "isEnabled": True
                        },
                        {
                            "id": "survey",
                            "isEnabled": True
                        },
                        {
                            "id": "recommendations",
                            "isEnabled": True
                        },
                        {
                            "id": "fashion_fix",
                            "isEnabled": True
                        },
                        {
                            "id": "follow_brand",
                            "isEnabled": True
                        },
                        {
                            "id": "subscription_confirmations",
                            "isEnabled": True
                        },
                        {
                            "id": "offers_sales",
                            "isEnabled": True
                        }
                    ]
                },
                "referrer": "nl_subscription_banner_one_click",
                "clientMutationId": "1620930739401"
            }
            }
        }

        # Send request to zalando
        try:
            Logger('Generating discount', self.taskNum, Fore.LIGHTYELLOW_EX)
            sendDiscountToMail = self.session.post("https://www.zalando." + self.region + "/api/graphql/", headers=headers, json=payload, proxies=self.proxy)
        except Exception as e:
            Logger('Error generating discount', self.taskNum, Fore.LIGHTRED_EX)
            return False

        # Check if request was successful
        if sendDiscountToMail.status_code == 200:
            if sendDiscountToMail.json()["data"]['subscribeToNewsletter']['isEmailVerificationRequired'] == False:
                Logger('Generated discount', self.taskNum, Fore.LIGHTMAGENTA_EX)

            else:
                Logger(f'Error generating discount, {sendDiscountToMail.json()}', self.taskNum, Fore.LIGHTRED_EX)
                return False

        else:
            Logger(f'Error generating discount, {sendDiscountToMail.reason}', self.taskNum, Fore.LIGHTRED_EX)
            return False


    def getEmail(self):
        try:
            Logger('Getting email', self.taskNum, Fore.LIGHTYELLOW_EX)
            while True:
                # Login to inbox
                mb = MailBox(self.imapServer).login(self.imapEmail, self.imapPassword)

                # Get all messages from Zalando Team
                messages = mb.fetch(criteria=AND(from_='Zalando Team'), mark_seen=True)

                # Go through all messages to find correct email. Doing this by checking it was received the same day and that it was the same receiver
                for msg in messages:
                    if str(datetime.datetime.now()).split(' ')[0] in str(msg.date) and self.email.lower() == msg.to[0].lower() and '10%' in msg.subject:
                        self.discountCode = msg.text.split('[→]')[0].split('\n')[len(msg.text.split('[→]')[0].split('\n')) - 1].replace(' ', '').replace('\n', '')
                        Logger(f'Got discount from email, {self.discountCode}', self.taskNum, Fore.LIGHTGREEN_EX)

                        # Write discount to file
                        with open('discounts.txt', 'a+') as writer:
                            writer.write(f'\n{self.discountCode}')

                        # Logout
                        mb.logout()
                        # Return
                        return True

                # Logout
                mb.logout()
                # Wait 5 sec until running again
                time.sleep(5)
        except Exception as e:
            # Make sure you have enabled less secure apps on the same device
            Logger(f'Error getting email, {e}', self.taskNum, Fore.LIGHTRED_EX)
            return False


    def __init__(self, taskNum, catchall, region, imapServer, imapEmail, imapPassword):
        self.taskNum = taskNum
        self.catchall = catchall
        self.region = region
        self.imapServer = imapServer
        self.imapEmail = imapEmail
        self.imapPassword = imapPassword
        self.session = requests.session()

        self.genEmail()
        self.getProxy()
        gen = self.genDiscount()
        if gen == False:
            return
        self.getEmail()



def Start():
    # Open and read config file
    try:
        os.system('clear')
        with open('config.json', 'r') as reader:
            Config = json.loads(reader.read())
        region = Config['region']
        catchall = Config['catchall']
        imapServer = Config['imap']['imap-server']
        imapEmail = Config['imap']['imap-email']
        imapPassword = Config['imap']['imap-password']

        # Ask user for task amount
        taskAmount = int(input(Fore.WHITE + '    Input task amount: ').strip('\n').strip(' '))

        # Windows
        if name == 'nt':
            os.system('cls')

        # Mac and linux
        else:
            os.system('clear')
    except Exception:
        Logger('Error reading config.json', 0, Fore.LIGHTRED_EX)
        return

    for i in range(taskAmount):
        Gen(i + 1, catchall, region, imapServer, imapEmail, imapPassword)

Start()

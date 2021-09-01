import os
import requests
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

BOT_TOKEN = os.environ['TOKEN']

bot = telebot.TeleBot(BOT_TOKEN)

class Wallet:  
    def __init__(self):
        self.Information = None
        self.Address = None
        self.Status = None
        self.Currency = None
        self.Balance = None  

    def Create(self, information, address, status, currency, balance):
        self.Information = information
        self.Address = address  
        self.Status = status
        self.Currency = currency
        self.Balance = balance  

    def SetInformation(self, information):  
        self.Information = information

    def SetAddress(self, address):  
        self.Address = address

    def SetStatus(self, status):  
        self.Status = status
        
    def SetCurrency(self, currency):  
        self.Currency = currency

    def SetBalance(self, balance):  
        self.Balance = balance
  
    def GetInformation(self):  
        return self.Information

    def GetAddress(self):  
        return self.Address

    def GetStatus(self):  
        return self.Status
    
    def GetCurrency(self):  
        return self.Currency

    def GetBalance(self):  
        return self.Balance

global OurWallet
OurWallet = Wallet()

def InsertCharacterToString(string, character, index):
    string = string[:index] + str(character) + string[index:]
    return string

def ToCorrectView(string, numberOfDecimalPlaces):
    length = len(string)
    while length <= numberOfDecimalPlaces:
        string = InsertCharacterToString(string, '0', 0)
        length += 1
    string = InsertCharacterToString(string, '.', -numberOfDecimalPlaces)
    while string[-1] == '0':
        string = string[0:-1]
    if string[-1] == '.':
        string = string + '0'
    return string

def GetEthOrAirBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance

def GetUsdtbnbBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 6)
    return walletBalance

def GetTetherBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 6)
    return walletBalance

def GetTronBalance(wallet):
    walletBalance = str(wallet.Information.json()['balance'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 6)
    return walletBalance

def GetTonBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 8)
    return walletBalance

def GetBnbBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance

def GetEthBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance

def GetBtcBalance(wallet):
    walletBalance = str(wallet.Information.json()[wallet.Address]['final_balance'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 8)
    return walletBalance

def GetAirInformation(walletAddress):
    airTokenAddress = '0xa47d9c7ab5e244dc5b22f88ae860802250d31a75'
    return requests.get(f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={airTokenAddress}&address={walletAddress}&tag=latest')

def GetUsdtbnbInformation(walletAddress):
    usdbnbTokenAddress = '0x55d398326f99059ff775485246999027b3197955'
    return requests.get(f'https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={usdbnbTokenAddress}&address={walletAddress}&tag=latest')

def GetTronInformation(walletAddress):
     return requests.get(f'https://apilist.tronscan.org/api/account?address={walletAddress}')
    
def GetTonInformation(walletAddress):
     return requests.get(f'https://api.ton.sh/getAddressInformation?address={walletAddress}')   
    
def GetBnbInformation(walletAddress):
    return requests.get(f'https://api.bscscan.com/api?module=account&action=balance&address={walletAddress}&tag=latest')

def GetTetherInformation(walletAddress):
    usdTokenAddress = '0xdac17f958d2ee523a2206206994597c13d831ec7'
    return requests.get(f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={usdTokenAddress}&address={walletAddress}&tag=latest')

def GetEthInformation(walletAddress):
    return requests.get(f'https://api.etherscan.io/api?module=account&action=balance&address={walletAddress}&tag=latest')

def GetBtcInformation(walletAddress):
    return requests.get(f'https://blockchain.info/balance?active={walletAddress}')

@bot.message_handler(commands = ['start'])
def SendWelcome(message):
    userFirstName = str(message.from_user.first_name)
    userLastName = str(message.from_user.last_name)
    if (userLastName == 'None'):
        welcomeMessage = f'Привет, {userFirstName}! Чтобы узнать баланс кошелька, просто отправь:\n /getwalletbalance :)'
    else:
        welcomeMessage = f'Привет, {userFirstName} {userLastName}! Чтобы узнать баланс кошелька, просто отправь(To find out the wallet balance, simply send):\n /getwalletbalance :)'
    bot.send_message(message.chat.id, welcomeMessage)

@bot.message_handler(commands = ['help'])
def SendHelp(message):
    helpMessage = '• /start - Запускает бота (Launches the bot)\n• /help - Информирует о командах (Informs about the commands)\n• /getwalletbalance - Отправляет баланс кошелька\n\nIf you have any questions, write support @inDaBots'
    bot.send_message(message.chat.id, helpMessage)

@bot.message_handler(commands = ['getwalletbalance'])
def SendWalletBalance(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    airButton = KeyboardButton(text = 'Atmosphere(AIR)')
    tonButton = KeyboardButton(text = 'Ton(TON)')
    ethButton = KeyboardButton(text = 'Ethereum(ETH)')
    btcButton = KeyboardButton(text = 'Bitcoin(BTC)')
    bnbButton = KeyboardButton(text = 'BinanceCoin(BNB)')
    erc20Button = KeyboardButton(text = 'Tether(ERC20)')
    bep20Button = KeyboardButton(text = 'Tether(BEP20)')
    tronButton = KeyboardButton(text = 'Tron(TRX)')
    keyboard.add(btcButton, ethButton, bep20Button, erc20Button, airButton, tronButton, tonButton, bnbButton)
    bot.send_message(message.chat.id, 'Пожалуйста, выберите валюту', reply_markup = keyboard)
    bot.register_next_step_handler(message, SetNameOfCurrency)

def SetNameOfCurrency(message):
    currency = str(message.text)
    if (currency != 'Atmosphere(AIR)'and currency != 'Ton(TON)' and currency != 'Ethereum(ETH)' and currency != 'Bitcoin(BTC)' and currency != 'BinanceCoin(BNB)' and currency != 'Tron(TRX)' and currency != 'Tether(ERC20)' and currency != 'Tether(BEP20)'):
        bot.send_message(message.chat.id, 'Такой криптовалюты у нас нет (We do not have such a cryptocurrency)', reply_markup = ReplyKeyboardRemove())
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJcV6Wrw3fxfGMo_gIyRcUnxMpQlocAAI4AANVLHgLguRsLYTyaJYYBA')
    else:
        OurWallet.SetCurrency(currency)
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте адрес кошелька (Please send the wallet address)', reply_markup = ReplyKeyboardRemove())
        bot.register_next_step_handler(message, SetWalletAddress)

def SetWalletAddress(message):
    OurWallet.SetAddress(str(message.text))
    SetWalletBalance(message)

def SetWalletBalance(message):
    if (OurWallet.Currency == 'Atmosphere(AIR)'):
        OurWallet.SetInformation(GetAirInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetEthOrAirBalance(OurWallet))        
  
    elif (OurWallet.Currency == 'Ethereum(ETH)'):
        OurWallet.SetInformation(GetEthInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetEthBalance(OurWallet))
            
    elif (OurWallet.Currency == 'BinanceCoin(BNB)'):
        OurWallet.SetInformation(GetBnbInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetBnbBalance(OurWallet))
     
    elif (OurWallet.Currency == 'Tether(ERC20)'):
        OurWallet.SetInformation(GetTetherInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetTetherBalance(OurWallet))
            
    elif (OurWallet.Currency == 'Tron(TRX)'):
         OurWallet.SetInformation(GetTronInformation(OurWallet.Address))
         try:
             if str(OurWallet.Information.json()['message']):   
                 OurWallet.Status = '0'
         except:
             OurWallet.Status = '1'
             OurWallet.SetBalance(GetTronBalance(OurWallet))  
            
    elif (OurWallet.Currency == 'Ton(TON)'):
         OurWallet.SetInformation(GetTonInformation(OurWallet.Address))
         try:
             if str(OurWallet.Information.json()['false']):   
                 OurWallet.Status = '0'
         except:
             OurWallet.Status = '1'
             OurWallet.SetBalance(GetTonBalance(OurWallet))           
    
    elif (OurWallet.Currency == 'Tether(BEP20)'):
        OurWallet.SetInformation(GetUsdtbnbInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetUsdtbnbBalance(OurWallet))       
    
    elif (OurWallet.Currency == 'Bitcoin(BTC)'):
        OurWallet.SetInformation(GetBtcInformation(OurWallet.Address))
        try:
            if str(OurWallet.Information.json()['error']):
                OurWallet.Status = '0'
        except:
            OurWallet.Status = '1'
            OurWallet.SetBalance(GetBtcBalance(OurWallet))

    if OurWallet.Status == '0':
        keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        yesButton = KeyboardButton(text = 'Yes')
        noButton = KeyboardButton(text = 'No')
        keyboard.add(yesButton, noButton)
        bot.send_message(message.chat.id, 'Данного адреса не существует. Желаете ввести адрес повторно? (This address does not exist. Would you like to enter the address again?)', reply_markup = keyboard)
        bot.register_next_step_handler(message, SendAddressAgain)
    else:
        bot.send_message(message.chat.id, f'Balance: {OurWallet.Balance} {OurWallet.Currency}')

def SendAddressAgain(message):
    answer = str(message.text)
    if (answer == 'Yes'):
        bot.send_message(message.chat.id, 'Отправьте другой адрес кошелька (Send another wallet address)', reply_markup = ReplyKeyboardRemove())
        bot.register_next_step_handler(message, SetWalletAddress)
    elif (answer == 'No'):
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJel6Wr_XyYDH4gnCDcfQ8Bqf_6fGpAAJmAANVLHgLgjTQuyJudYYYBA', reply_markup = ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'What are you talking about, this answer is not in my code', reply_markup = ReplyKeyboardRemove())
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJcV6Wrw3fxfGMo_gIyRcUnxMpQlocAAI4AANVLHgLguRsLYTyaJYYBA')

bot.polling()


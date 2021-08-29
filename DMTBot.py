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

def GetEthOrDmtBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance
def GetEthOrAirBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance
def GetBnbtestBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance
def GetBnbBalance(wallet):
    walletBalance = str(wallet.Information.json()['result'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 18)
    return walletBalance

def GetBtcBalance(wallet):
    walletBalance = str(wallet.Information.json()[wallet.Address]['final_balance'])
    if walletBalance != '0':
        walletBalance = ToCorrectView(walletBalance, 8)
    return walletBalance

def GetDmtInformation(walletAddress):
    dmtTokenAddress = '0xe80eeb5df2478f948427fba1ffd3160bde99e976'
    return requests.get(f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={dmtTokenAddress}&address={walletAddress}&tag=latest')

def GetBnbInformation(walletAddress):
    return requests.get(f'https://api.bscscan.com/api?module=account&action=balancemulti&address={walletAddress}&tag=latest')

def GetBnbtestInformation(walletAddress):
    return requests.get(f'https://api.bscscan.com/api?module=account&action=balancemulti&address={walletAddress}&tag=latest')

def GetAirInformation(walletAddress):
    dmtTokenAddress = '0xa47d9c7ab5e244dc5b22f88ae860802250d31a75'
    return requests.get(f'https://api.etherscan.io/api?module=account&action=tokenbalance&contractaddress={AirTokenAddress}&address={walletAddress}&tag=latest')

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
        welcomeMessage = f'Привет, {userFirstName} {userLastName}! Чтобы узнать баланс кошелька, просто отправь:\n /getwalletbalance :)'
    bot.send_message(message.chat.id, welcomeMessage)

@bot.message_handler(commands = ['help'])
def SendHelp(message):
    helpMessage = '• /start - Запускает бота\n• /help - Информирует о командах\n• /getwalletbalance - Отправляет баланс кошелька\n\nЕсли есть вопросы, пиши @inDaBots'
    bot.send_message(message.chat.id, helpMessage)

@bot.message_handler(commands = ['getwalletbalance'])
def SendWalletBalance(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
    dmtButton = KeyboardButton(text = 'DMT')
    airButton = KeyboardButton(text = 'AIR')
    ethButton = KeyboardButton(text = 'ETH')
    btcButton = KeyboardButton(text = 'BTC')
    bnbButton = KeyboardButton(text = 'BNB')
    bnbtestButton = KeyboardButton(text = 'BNBtest')
    keyboard.add(dmtButton, airButton, ethButton, btcButton, bnbButton, bnbtestButton )
    bot.send_message(message.chat.id, 'Пожалуйста, выберите валюту', reply_markup = keyboard)
    bot.register_next_step_handler(message, SetNameOfCurrency)

def SetNameOfCurrency(message):
    currency = str(message.text)
    if (currency != 'DMT' and currency != 'AIR' and currency != 'ETH' and currency != 'BTC' and currency != 'BNB' and currency != 'BNBtest'):
        bot.send_message(message.chat.id, 'Такой валюты у нас нет', reply_markup = ReplyKeyboardRemove())
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJcV6Wrw3fxfGMo_gIyRcUnxMpQlocAAI4AANVLHgLguRsLYTyaJYYBA')
    else:
        OurWallet.SetCurrency(currency)
        bot.send_message(message.chat.id, 'Пожалуйста, отправьте адрес кошелька', reply_markup = ReplyKeyboardRemove())
        bot.register_next_step_handler(message, SetWalletAddress)

def SetWalletAddress(message):
    OurWallet.SetAddress(str(message.text))
    SetWalletBalance(message)

def SetWalletBalance(message):
    if (OurWallet.Currency == 'DMT'):
        OurWallet.SetInformation(GetDmtInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetEthOrDmtBalance(OurWallet))
            
    def SetWalletBalance(message):
    if (OurWallet.Currency == 'AIR'):
        OurWallet.SetInformation(GetAirInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetEthOrAirBalance(OurWallet))        

    elif (OurWallet.Currency == 'ETH'):
        OurWallet.SetInformation(GetEthInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetEthOrDmtBalance(OurWallet))
            
    elif (OurWallet.Currency == 'BNB'):
        OurWallet.SetInformation(GetBnbInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetBnbBalance(OurWallet))
     
    elif (OurWallet.Currency == 'BNBtest'):
        OurWallet.SetInformation(GetBnbtestInformation(OurWallet.Address))
        OurWallet.SetStatus(OurWallet.Information.json()['status'])
        if (OurWallet.Status == '1'):
            OurWallet.SetBalance(GetBnbtestBalance(OurWallet))
            
    elif (OurWallet.Currency == 'BTC'):
        OurWallet.SetInformation(GetBtcInformation(OurWallet.Address))
        try:
            if str(OurWallet.Information.json()['reason']):
                OurWallet.Status = '0'
        except:
            OurWallet.Status = '1'
            OurWallet.SetBalance(GetBtcBalance(OurWallet))

    if OurWallet.Status == '0':
        keyboard = ReplyKeyboardMarkup(resize_keyboard = True, one_time_keyboard = True)
        yesButton = KeyboardButton(text = 'Да')
        noButton = KeyboardButton(text = 'Нет')
        keyboard.add(yesButton, noButton)
        bot.send_message(message.chat.id, 'Данного адреса не существует. Желаете ввести адрес повторно?', reply_markup = keyboard)
        bot.register_next_step_handler(message, SendAddressAgain)
    else:
        bot.send_message(message.chat.id, f'Баланс кошелька: {OurWallet.Balance} {OurWallet.Currency}')

def SendAddressAgain(message):
    answer = str(message.text)
    if (answer == 'Да'):
        bot.send_message(message.chat.id, 'Отправьте другой адрес кошелька', reply_markup = ReplyKeyboardRemove())
        bot.register_next_step_handler(message, SetWalletAddress)
    elif (answer == 'Нет'):
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJel6Wr_XyYDH4gnCDcfQ8Bqf_6fGpAAJmAANVLHgLgjTQuyJudYYYBA', reply_markup = ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, 'Данного ответа нет в моем коде', reply_markup = ReplyKeyboardRemove())
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIJcV6Wrw3fxfGMo_gIyRcUnxMpQlocAAI4AANVLHgLguRsLYTyaJYYBA')

bot.polling()


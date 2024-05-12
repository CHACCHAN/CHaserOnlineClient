import time
import requests
import re
import sys
import random
import os
import copy

# os.environ["http_proxy"] = "http://proxy.spec.ed.jp:80"
defineOptions = {
  'url':'http://www7019ug.sakura.ne.jp/CHaserOnline003/user/',
  'proxy':None,
  'debug':True,
  'user':'cool',
  'password':'cool',
  'room':5794,
}
"""
  @param
"""
class CHaserOnlineClient:
  def __init__(self, url=defineOptions['url'], proxy=defineOptions['proxy'], debug=defineOptions['debug'], user=defineOptions['user'], password=defineOptions['password'], room=defineOptions['room'])->None:
    self._url = url
    self._proxy = proxy
    self._debug = debug
    self._user = user
    self._password = password
    self._room = room
    self.turn = 0
    self.message(message='Import', code=f'')
    self.message(message='Created CHaserOnlineClient!')
  
  def htmlReplace(self)->None:
    self._code = re.sub(r'\\r|\s+', '\n', self._response.text)
    self.message(message='🔽Replaced html!', code=self._code)
    
  def session(self)->None:
    self._session = requests.session()
    self._response = self._session.get(self._url)
    self._jsessionid = self._session.cookies.get('JSESSIONID')
    self.htmlReplace()
    self.message(message='Connect complete!')
  
  def login(self)->None:
    self.message(message=f'Login with {self._user}')
    while True:
      self._response = self._session.get(f'{self._url}UserCheck?user={self._user}&pass={self._password}')
      self._session.headers.update({'User-Agent': 'CHaserOnlineClient/2024'})
      self._session.cookies.set('jsession', self._jsessionid)
      self.htmlReplace()
      if self._code.find('user=')<0 or self._code.find('pass=')<0:
        break
  
  def room(self)->None:
    self.message(message=f'Join with room{self._room}')
    while self._code.find('roomNumber=')>-1 and self._code.find('command1=')<0:
      self._response = self._session.get(f'{self._url}RoomNumberCheck?roomNumber={self._room}')
      self.htmlReplace()
    
  def getready(self)->None:
    self.message(message='GetReady')
    while self._code.find('command1=')>-1:
      self._response = self._session.get(f'{self._url}GetReadyCheck?command1=gr')
      self.htmlReplace()
    
  def action(self):
    self.message(message='Action')
    while self._code.find('command2=')>-1:
      self._response = self._session.get(f'{self._url}CommandCheck?command2=wu')
      self.htmlReplace()
  
  def complete(self):
    self.message(message='Complete')
    while self._code.find('command3=')>-1:
      self._response = self._session.get(f'{self._url}EndCommandCheck?command3=%23')
      self.htmlReplace()
  
  def returnCode(self)->None:
    print(f'{self._code.find('ReturnCode=')}')
    if self._code.find('ReturnCode=')>-1:
      print(f'{self._code[self._code.find('ReturnCode=')+11:len(self._code)]}')
      codeTemp = self._code[self._code.find('ReturnCode=')+11:len(self._code)]
      codeEnd = codeTemp[0:codeTemp.find('\n')]
      print(f'{codeEnd}')
      RCodeInfo = codeEnd.split(',')
      print(f'debug{RCodeInfo}')
      point = {}
      if self.turn==0:
        for i in RCodeInfo:
          print(i)
          if int(i)>=1000:
            point[str(i)] = -9999
            mynum = i
      self.message(message=f'ReturnCode={codeEnd}')
  
  def message(self, message=False, code=False)->None:
    if self._debug:
      print(f'\033[42;37m{message}\033[0m\n')
      if code:
        print(code)
  
  def main(self)->None:
    try:
      self.session()
      self.login()
      self.room()
      
      while self._code.find('user=')==-1 and self._code.find('command1=')>-1:
        print(f'{self._code.find('user=')} {self._code.find('command1=')}')
        self.getready()
        self.returnCode()
        self.action()
        self.returnCode()
        self.complete()
        print(f'{self._code.find('user=')} {self._code.find('command1=')}')
        self.turn += 1
    except:
      print('Error')

Instance = CHaserOnlineClient(
  url='http://www7019ug.sakura.ne.jp/CHaserOnline003/user/',
  user='cool19',
  password='cool',
  room=6070,
)

Instance.main()

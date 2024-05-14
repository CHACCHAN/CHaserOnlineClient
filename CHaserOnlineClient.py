import requests
import re
import os

defineOptions = {
  'url':'http://www7019ug.sakura.ne.jp/CHaserOnline003/user/',
  'proxy':None,
  'debug':True,
  'user':'cool',
  'password':'cool',
  'room':5794,
}
"""
   作成日 - 2024/05/14
   更新日 - 2024/05/14
   作成者 - 中山 裕哉(CHACCHAN)
   ライセンス - MIT LICENSE
"""
class CHaserOnlineController:
    def __init__(self, url=defineOptions['url'], proxy=defineOptions['proxy'], debug=defineOptions['debug'], user=defineOptions['user'], password=defineOptions['password'], room=defineOptions['room'])->None:
        self._url = url
        self._debug = debug
        self._user = user
        self._password = password
        self._room = room
        self._gameSet = False
        self._returnNumberCode = ['9999', '9999', '9999', '9999', '9999', '9999', '9999', '9999', '9999']
        self.turn = 0
        if proxy:
            os.environ["http_proxy"] = proxy
        self.message(message='Import', code=f'')
        self.message(message='Created CHaserOnlineClient!')
    
    def htmlReplace(self)->None:
        self._code = re.sub(r'\\r|\s+', '\n', self._response.text)
        self.message(message='🔽Replaced html!', code='')

    def fill_array(self, arr, default_value, target_length):
        if len(arr) < target_length:
            arr.extend([default_value] * (target_length - len(arr)))
        for i in range(len(arr)):
            if arr[i] == '':
                arr[i] = default_value
        return arr
        
    def session(self)->None:
        self._session = requests.session()
        self._response = self._session.get(self._url)
        self._jsessionid = self._session.cookies.get('JSESSIONID')
        self.htmlReplace()
        self.message(message='Connect complete!')
    
    def login(self)->None:
        self.message(message=f'Login with {self._user}')
        loginAgainCount = 0
        while True:
            loginAgainCount += 1
            self._response = self._session.get(f'{self._url}UserCheck?user={self._user}&pass={self._password}')
            self._session.headers.update({'User-Agent': 'CHaserOnlineClient/2024'})
            self._session.cookies.set('jsession', self._jsessionid)
            self.htmlReplace()
            if self._code.find('user=')<0 or self._code.find('pass=')<0:
                break
            if loginAgainCount>10:
                exit(1)
    
    def room(self)->None:
        self.message(message=f'Join with room{self._room}')
        while self._code.find('roomNumber=')>-1 and self._code.find('command1=')<0:
            self._response = self._session.get(f'{self._url}RoomNumberCheck?roomNumber={self._room}')
            self.htmlReplace()
        
    def getready(self, GetReadyMode='gr')->None:
        self.message(message='GetReady')
        while self._code.find('command1=')>-1:
            self._response = self._session.get(f'{self._url}GetReadyCheck?command1={GetReadyMode}')
            self.htmlReplace()
    
    def getready_py(self, func):
        def getready():
            self.message(message='GetReady')
            GetReadyModeInt = [int(x) for x in self._returnNumberCode if isinstance(x, str)]
            GetReadyMode = func(GetReadyModeInt)
            while self._code.find('command1=')>-1:
                self._response = self._session.get(f'{self._url}GetReadyCheck?command1={GetReadyMode}')
                self.htmlReplace()
        return getready
        
    def action(self, mode='wu')->None:
        self.message(message='Action')
        while self._code.find('command2=')>-1:
            self._response = self._session.get(f'{self._url}CommandCheck?command2={mode}')
            self.htmlReplace()
    
    def action_py(self, func):
        def action():
            self.message(message='Action')
            mode = func([int(x) for x in self._returnNumberCode if isinstance(x, str)])
            while self._code.find('command2=')>-1:
                self._response = self._session.get(f'{self._url}CommandCheck?command2={mode}')
                self.htmlReplace()
        return action
    
    def complete(self)->None:
        self.message(message='Complete')
        while self._code.find('command3=')>-1:
            self._response = self._session.get(f'{self._url}EndCommandCheck?command3=%23')
            self.htmlReplace()
            self.turn += 1
    
    def gameSet(self)->bool:
        if self._code.find('command1=')==-1 and self._code.find('command2=')==-1 and self._code.find('command3=')==-1:
            return True
        else:
            return False
    
    def gameTurn(self)->int:
        return self.turn
    
    def returnNumber(self)->dict:
        if self._code.find('ReturnCode=')>-1:
            codeTemp = self._code[self._code.find('ReturnCode=')+11:len(self._code)]
            codeEnd = codeTemp[0:codeTemp.find('\n')]
            returnCode = codeEnd.split(',')
            self._returnNumberCode = returnCode
            
            self._returnNumberCode = self.fill_array(self._returnNumberCode, '9999', 9)
            print(self._returnNumberCode)
            self.message(message=f'ReturnCode={codeEnd}')
            return self._returnNumberCode
    
    def message(self, message=False, code=False)->None:
        if self._debug:
            print(f'\033[42;37m{message}\033[0m\n')
        if code:
            print(code)
    
    def connect(self)->bool:
        try:
            self.session()
            self.login()
            self.room()
            return True
        
        except:
            print('Connect Error')
            return False
        
    def run(self, getreadyFunc, actionFunc)->None:
        self.session()
        self.login()
        self.room()
        
        while self._code.find('user=')==-1 and self._code.find('command1=')>-1:
            getreadyFunc()
            self.returnNumber()
            actionFunc()
            self.returnNumber()
            self.complete()
            self.turn += 1

# CHaserOnlineのライブラリをインポート
from CHaserOnlineClient import CHaserOnlineController

"""
    説明
    CHaserOnlineClient.pyはCHaserOnlineをPythonかつ簡単に実行するためのライブラリです。
    また、Flaskとの連携で他言語でも記入可能になっています。(今回は関係ない)
    ライブラリが勝手にやってくれるものは[サーバーへの接続-><作戦の処理を読み取る>->サーバーへ送信->自動最適化]です。
    今見ているこのファイルは<作戦の処理を読み取る>ための元のファイルになります。
    つまり、このファイルで記述した作戦はすべてライブラリによって管理されます。
"""

# インスタンス化(クライアントの初期化)
_CHaserOnlineClient = CHaserOnlineController(
    url='http://www7019ug.sakura.ne.jp/CHaserOnline003/user/',
    proxy=None,
    debug=True,
    user='cool8',
    password='cool',
    room=6090
)

# GetReadyのロジックを記述
@_CHaserOnlineClient.getready_py
def getready(ActionReturnNumber):
    if ActionReturnNumber[1] >= 70 and ActionReturnNumber[1] <= 79:
        GetReadyMode = 'gru'
    elif ActionReturnNumber[3] >= 70 and ActionReturnNumber[3] <= 79:
        GetReadyMode = 'grl'
    elif ActionReturnNumber[5] >= 70 and ActionReturnNumber[5] <= 79:
        GetReadyMode = 'grr'
    elif ActionReturnNumber[7] >= 70 and ActionReturnNumber[7] <= 79:
        GetReadyMode = 'grd'
    else:
        GetReadyMode = 'gr'
    return GetReadyMode

# Actionのロジックを記述
@_CHaserOnlineClient.action_py
def action(returnNumber):
    if returnNumber[1] >= 70 and returnNumber[1] <= 79:
        mode = 'wu'
    elif returnNumber[3] >= 70 and returnNumber[3] <= 79:
        mode = 'wl'
    elif returnNumber[5] >= 70 and returnNumber[5] <= 79:
        mode = 'wr'
    elif returnNumber[7] >= 70 and returnNumber[7] <= 79:
        mode = 'wd'
    else:
        mode = 'wu'
    return mode

# 実行
_CHaserOnlineClient.run(getreadyFunc=getready, actionFunc=action)
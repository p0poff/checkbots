import os
import urllib.request
import time

class Init:
    def __init__(self):
        self.botId = os.environ.get('BOTID', '')
        self.chatId = os.environ.get('CHATID', '')
        self.chatIdTwo = os.environ.get('CHATIDTWO', '')
        self.url = os.environ.get('URL', '')
        self.timeout = int(os.environ.get('TIMEOUT', 10))
        self.sleep = int(os.environ.get('SLEEP', 60))
        self.interval = int(os.environ.get('INTERVAL', 120)) #интервал, через сколько итераций пойдет сообщений что бот работает self.sleep * self.interval = 2 часа
        self.test = os.environ.get('TEST', 'python test')
        self.countWrong = os.environ.get('COUNTWRONG', 3)

class ShowWrong:
    def __init__(self, init):
        self.count = 0
        self.init = init

    def check(self, status):
        if status == 200:
            self.down()
        else:
            self.add()
        return self.count >= self.init.countWrong

    def add(self):
        if self.count < self.init.countWrong + 2:
            self.count += 1

    def down(self):
        if self.count > 0:
            self.count -= 1

#docker run --name checkbot -e TIMEOUT=15 -e CHATID=-1001118239010 -e BOTID=631495294:AAE0WhAKNbqYlvtAp0_fJLsu5GHZyS4WXcs -e INTERVAL=240 --restart=always -d checkbot

def checkSite(**args):
    init = args['init']
    try:
        req = urllib.request.urlopen(init.url, timeout=init.timeout)
        code = req.code
    except urllib.request.socket.timeout:
        code = 504
    except Exception as args:
        print(args)
        code = 500
    return code

def send_message(**args):
    botId = args['botId']
    chatId = args['chatId']
    text = args.get('text', '')
    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (botId, chatId, text)
    urllib.request.urlopen(url)


def main():
    init = Init()
    showWrong = ShowWrong(init)
    __iter = 0
    while True:
        if __iter == init.interval:
            __iter = 0
        status = checkSite(init = init)
        __show = showWrong.check(status)
        print(status, __iter)
        if status != 200:
            if __show == True:
                send_message(botId = init.botId, chatId = init.chatId, text = 'site tasmarket response code %s' % (status))
        if __iter == 0:
            send_message(botId = init.botId, chatId = init.chatIdTwo, text = 'bot is RUN')
        __iter += 1
        time.sleep(init.sleep)
    

if __name__ == '__main__':
	main()
import os
import urllib.request
import time
import paramiko

class Init:
    def __init__(self):
        self.botId = os.environ.get('BOTID', '')
        self.chatId = os.environ.get('CHATID', '')
        self.chatIdTwo = os.environ.get('CHATIDTWO', '')
        self.url = os.environ.get('URL', '')
        self.timeout = int(os.environ.get('TIMEOUT', 20))
        self.sleep = int(os.environ.get('SLEEP', 120))
        self.interval = int(os.environ.get('INTERVAL', 120))

def send_message(**args):
    botId = args['botId']
    chatId = args['chatId']
    text = args.get('text', '')
    url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&text=%s' % (botId, chatId, text)
    urllib.request.urlopen(url)

def connect(init):
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    result = ''
    try:
        client.connect(init.url, auth_timeout = init.timeout, timeout = init.timeout)
    except Exception as inst:
        result = inst.args[0]
    
    client.close()
    return result


def main():
    init = Init()
    __iter = 0
    while True:
        result = connect(init)
        print(result)
        if __iter == init.interval:
            __iter = 0

        if result != 'Authentication failed.' and result != 'No authentication methods available' :
            send_message(botId = init.botId, chatId = init.chatId, text = 'crm worker server have error %s' % (result))

        if __iter == 0:
            send_message(botId = init.botId, chatId = init.chatIdTwo, text = 'bot crm is RUN')
        __iter += 1
        time.sleep(init.sleep)



def test():
    print('test mode')
    init = Init()
    send_message(botId = init.botId, chatId = init.chatId, text = 'test')
    client = paramiko.client.SSHClient()
    client.load_system_host_keys()
    try:
        # client.connect(init.url, auth_timeout = 0.5, timeout = 2)
        client.connect(init.url)
    except paramiko.ssh_exception.SSHException:
        print('timeout')
    except paramiko.ssh_exception.AuthenticationException:
        print('auth')
    except:
        print('wtf')
    client.close()

if __name__ == '__main__':
    # test()
	main()
import configparser

## 인스타그램 계정 관리 INI파이릉 생성한다.
config = configparser.ConfigParser()
config['instagram'] = {}
example = config['instagram']
example['ID'] = 'kjk92_IT'
example['PASSWORD'] = '***'

with open('config.ini', 'w') as configfile:
    config.write(configfile)
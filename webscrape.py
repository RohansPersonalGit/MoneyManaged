from webparser import  WebParser
from webparser import  Account


def get_credentials(file_name, input_mapping):
    with open(file_name) as f:
        input_mapping['password'] = f.readline()
        input_mapping['username'] = f.readline()



def main():
    input_mapping = {"username": '', "password": ''}
    get_credentials('password.text',input_mapping)
    parser = WebParser(True)
    parser.login_td(input_mapping)
    parser.get_info(Account.credit)





if __name__ == '__main__':
    main()
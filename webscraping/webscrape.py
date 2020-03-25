from webscraping.webparser import  WebParser


def get_credentials(file_name, input_mapping):
    with open(file_name) as f:
        input_mapping['password'] = f.readline()
        input_mapping['username'] = f.readline()



def main():
    input_mapping = {"username": '', "password": ''}
    get_credentials('../password.text', input_mapping)
    parser = WebParser(True)
    parser.login_td(input_mapping)
    parser.choose_account('//a[contains(text(),"VISA CARD")]')
    check = parser.click_download()
    parser.click_next






if __name__ == '__main__':
    main()
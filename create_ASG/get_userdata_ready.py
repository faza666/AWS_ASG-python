import base64


def user_data_envelop(user_data_file_name):
    try:
        with open(user_data_file_name, 'r') as user_data:
            user_data_script = user_data.read()
            encoded_data = base64.b64encode(user_data_script.encode('ascii')).decode('ascii')
        return encoded_data
    except FileNotFoundError:
        return 'Cannot open file for writing'


def user_data_unpack():
    pass

# if __name__ == '__main__':
# user_data_string = user_data_envelop('ec2-user-data.txt')
# print(user_data_string)

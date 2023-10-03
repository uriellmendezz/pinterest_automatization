from functions import PinterestClient
import pandas as pd
import os
import json
import time
import json

import json

def are_json_values_empty(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        return all(value == '' or value is None for value in data.values())

if __name__ == '__main__':
    df_accounts = pd.read_excel('../accounts_excel.xlsx')
    df_accounts['PATH TO IMAGES'] = df_accounts['PATH TO IMAGES'].str.strip('"').replace("\\",'/')

    if are_json_values_empty('../paths.json') == True:
        with open('../paths_owner.json', 'r') as jfile:
            data = json.load(jfile)
    else:
        with open('../paths.json', 'r') as jfile:
            data = json.load(jfile)

    path_webdriver = data['WebDriver_Path'].replace('\\','/').strip()
    path_googlechrome = data['Chrome_Path'].replace('\\','/').strip()

    client = PinterestClient(webdriver_path = path_webdriver,
                            chrome_exe_path = path_googlechrome)

    client.Initialize_WebDriver()
    general_time_start = time.time()

    accounts = []
    total_pins = []
    time_executed = []

    for number_account in range(len(df_accounts)):
        start_time = time.time()
        #1
        client.Open_Pinterest()
        #2
        client.Log_In(email = df_accounts.iloc[number_account]['PINTEREST EMAIL'],
               password = df_accounts.iloc[number_account]['PINTEREST PASSWORD'])
        #3
        client.Create_Pin()
        #4
        client.Load_Images(path_to_imgs = df_accounts.iloc[number_account]['PATH TO IMAGES'])
        #5
        client.Edit_Pins(title_ = df_accounts.iloc[number_account]['PINS TITLE'],
                  description_ = df_accounts.iloc[number_account]['PINS DESCRIPTION'],
                  link_ = df_accounts.iloc[number_account]['PINS LINK'])
        
        number_of_pins = client.Count_Pins()
        #6
        client.Publish_Pins()

        client.Random_Duration_Action(
            start =  int(number_of_pins) * 2.5,
            end   = (int(number_of_pins) * 2.5) + 10
        )

        client.Delete_Images()

        client.Random_Duration_Action(10,20)

        #7
        client.Log_Out()

        finish_time = time.time()

        total_time = client.duration(start_time,finish_time)

        accounts.append(df_accounts.iloc[number_account]['ACCOUNT NAME'])
        total_pins.append(number_of_pins)
        time_executed.append(total_time)

        if number_account == len(df_accounts):
            break
        else:
            client.Random_Duration_Action(36,78)

    general_time_finish = time.time()
    total_general_time = client.duration(general_time_start, general_time_finish)

    body = ''
    for i,e in enumerate(accounts):
        message = f'''Account: {e}\n - Total Pins uploaded: {total_pins[i]}\n - Process duration: {time_executed[i]}\n\n'''
        body += message

    body += f'\nProcess total duration: {total_general_time}'

    client.Send_Email(
        receiver_email = df_accounts.iloc[number_account]['YOUR GMAIL'],
        subject='Uploading Pins to Pinterest',
        body=body
    )

    client.Turn_Off_WebDriver()


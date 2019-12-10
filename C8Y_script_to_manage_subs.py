import requests
import base64
import json
import params
import time


def show_tenants(url, headers):
    """
    This function shows all tenants registered on the platform
        Parameters:
            url: (str) platform url + path to tenants list defined in params.py file
            headers: (str) login and secret defined in params.py file and converted to base64 + apps json headers
        Returns:
            List of strings with all tenant names to stdout
    """
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code == 200:
        response_list = json.loads(response.content)
        full_info_tenants_list = (response_list['tenants'])
        for i in range(0, len(full_info_tenants_list)):
            element = full_info_tenants_list[i]
            full_info_tenants_list.append(element['id'])
            if element['id'] != 'management':
                print(element['id'])
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def create_tenants_list(url, headers):
    """
    This function shows all tenants registered on the platform and writes it to file
        Parameters:
            url: (str) platform url + path to tenants list defined in params.py file
            headers: (str) login and secret defined in params.py file and converted to base64 + apps json headers
        Returns:
            List of strings with all tenant names to stdout and writes it to all_tenants_list.txt file to current dir
    """
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code == 200:
        file = open("all_tenants_list.txt", "w+")
        response_list = json.loads(response.content)
        full_info_tenants_list = (response_list['tenants'])
        for i in range(0, len(full_info_tenants_list)):
            element = full_info_tenants_list[i]
            full_info_tenants_list.append(element['id'])
            if element['id'] != 'management':
                print(element['id'])
                file.write(element['id'] + "\r")
        file.close()
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def show_apps(url, headers):
    """
    This function shows all apps registered on the platform
        Parameters:
            url: (str) platform url + path to applications list defined in params.py file
            headers: (str) login and secret defined in params.py file and converted to base64 + apps json headers
        Returns:
            Strings in table like formatting with all application names and IDs to stdout
    """
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    if response.status_code == 200:
        response_list = json.loads(response.content)['applications']
        print("\n"
              "\n"
              "Application                      | ID       | Type\n"
              "---------------------------------|----------|-----------------")
        for iterator in range(0, len(response_list)):
            elem = response_list[iterator]
            aname = elem['name'].strip()
            aid = elem['id'].strip()
            atype = elem['type'].strip()
            aavail = elem['availability'].strip()
            print(
                str(aname).ljust(32), "|", str(aid).rjust(8), "|", str(atype), ",", str(aavail))
        print("\n")
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def show_tenants_subscribed_to_app_id(url, headers):
    """
    This function shows all tenants subscribed to user defined application ID
        Parameters:
            user input: app ID
            url: (str) platform url + path to applications list defined in params.py file
            headers: (str) login and secret defined in params.py file and converted to base64 + apps json headers
        Returns:
            Strings with all tenant names subscribed to application with user defined ID to stdout
    """
    application_id = input("Provide application ID: ")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    c = 0
    if response.status_code == 200:
        response_list = json.loads(response.content)
        full_info_apps_list = (response_list['tenants'])
        for i in range(0, len(full_info_apps_list)):
            element = full_info_apps_list[i]
            elem_apps = element['applications']
            elem_ref = elem_apps['references']
            for i_refer in range(0, len(elem_ref)):
                element_application = elem_ref[i_refer]
                if element_application['application']['id'] == application_id:
                    start = '/tenant/tenants/'
                    end = '/applications/'
                    s = element_application['self']
                    if c == 0:
                        print('\nApplication with ID: \t' + element_application['application']['id'],
                              '\nApplication name is: \t' + element_application['application']['name'],
                              '\nis subscribed to tenants: \t\n')
                        c = c + 1
                    print(s[s.find(start) + len(start):s.rfind(end)])
                # elif element_application['application']['id'] != application_id:
                #     if c == 0:
                #         print('\nTenants subscribed to application with ID: \t' + element_application['application'][
                #             'id'],
                #               '\nand name: \t' + element_application['application']['name'],
                #               '\n not found!')
                #         c = c + 1
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def create_tenants_list_subscribed_to_app_id(url, headers):
    """
    This function shows all tenants subscribed to user defined application ID and creates file with this list
        Parameters:
            user input: app ID
            url: (str) platform url + path to applications list defined in params.py file
            headers: (str) login and secret defined in params.py file and converted to base64 + apps json headers
        Returns:
            Strings with all tenant names subscribed to application with user defined ID to stdout and writes it to file
    """
    application_id = input("Provide application ID: ")
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    c = 0
    if response.status_code == 200:
        file = open("tenants_list_subscribed_to_app.txt", "w+")
        response_list = json.loads(response.content)
        full_info_apps_list = (response_list['tenants'])
        for i in range(0, len(full_info_apps_list)):
            element = full_info_apps_list[i]
            elem_apps = element['applications']
            elem_ref = elem_apps['references']
            for i_refer in range(0, len(elem_ref)):
                element_application = elem_ref[i_refer]
                if element_application['application']['id'] == application_id:
                    start = '/tenant/tenants/'
                    end = '/applications/'
                    s = element_application['self']
                    sub_tenant = (s[s.find(start) + len(start):s.rfind(end)])
                    print(sub_tenant)
                    file.write(sub_tenant + "\r")
        file.close()

    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def unsubscribe_tenants_list_from_app_id(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    application_id = input("Provide application ID to unsubscribe: ")
    if response.status_code == 200:
        try:
            with open('tenants_list_subscribed_to_app.txt', 'r') as f:
                contents = f.readlines()
                for line in contents:
                    print('Unsubscribing application with ID ' + application_id + ' from tenant: '
                                                                                  '' + line.rstrip("\n\r"))
                    url = (base_url + '/tenant/tenants/' + line.rstrip("\n\r") + '/applications/' + application_id)
                    print(url)
                    delete_sub = requests.delete(url, headers=headers)
                    print('Server response {}'.format(delete_sub.content) + '\n')
        except IOError:
            print("File not accessible or not present in catalog!")
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def subscribe_tenants_list_to_app_id(url, headers):
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    application_id = input("Provide application ID to subscribe: ")
    timeout = float(input("Provide timeout between subscriptions in seconds default is 10 sec: ") or "10")
    if response.status_code == 200:
        try:
            with open('tenants_list_to_subscribe_to_app.txt', 'r') as f:
                contents = f.readlines()
                for line in contents:
                    print('Subscribing tenant ' + line.rstrip("\n\r") + ' to application with ID ' + application_id)
                    url = (base_url + '/tenant/tenants/' + line.rstrip("\n\r") + '/applications')
                    payload = ('{ "application": { "id" : "' + application_id + '"}}')
                    print(payload)
                    create_sub = requests.post(url, data=payload, headers=headers)
                    time.sleep(timeout)
                    print('Server response {}'.format(create_sub.content) + '\n')
        except IOError:
            print("File not accessible or not present in catalog!")
    else:
        print("Status: " + str(response.status_code) + " Message: " + str(response.content))


def main():
    print("\nThis script can show all applications on the platform with IDs, \n"
          "\n"
          "\n")

    while True:
        print("\nMake a choice\n"
              "1. Show all applications registered on the platform \n"
              "2. Show all tenants registered on the platform\n"
              "3. Show all tenants registered on the platform and create all_tenants_list.txt file in script dir\n"
              "4. Show tenants subscribed to a specific application with the provided id\n"
              "5. Show all tenants subscribed to application with provided ID and create tenants_list_sub_app_id.txt "
              "file in script dir\n"
              "80. Subscribe to application with provided ID to tenants defined in "
              "tenants_list_to_subscribe_to_app.txt\n"
              "99. Unsubscribe application with provided ID from tenants list defined in tenants_list_sub_app_id.txt\n"
              "0. To exit from a program\n")
        choice = input('Waiting for your choice > ')
        if choice == '1':
            show_apps(apps_url, user_headers)
        elif choice == '2':
            show_tenants(tenants_url, user_headers)
        elif choice == '3':
            create_tenants_list(tenants_url, user_headers)
        elif choice == '4':
            show_tenants_subscribed_to_app_id(tenants_url, user_headers)
        elif choice == '5':
            create_tenants_list_subscribed_to_app_id(tenants_url, user_headers)
        elif choice == '80':
            subscribe_tenants_list_to_app_id(tenants_url, user_headers)
        elif choice == '99':
            unsubscribe_tenants_list_from_app_id(tenants_url, user_headers)
        elif choice == '0':
            print('Exiting...')
            exit()
        else:
            print('Function not found')


base_url = params.base_url
login_pass = ('management/' + params.login + ':' + params.secret)
adminCredentials = base64.b64encode(login_pass.encode()).decode()
user_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                'Authorization': 'Basic %s' % adminCredentials}
apps_url = base_url + '/application/applications?pageSize=10000'
tenants_url = base_url + '/tenant/tenants?pageSize=1000'

if __name__ == '__main__':
    main()

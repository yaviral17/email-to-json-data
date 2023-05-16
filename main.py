from __future__ import print_function
import base64

import os.path
import time

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.modify', 'https://www.googleapis.com/auth/gmail.labels', 'https://www.googleapis.com/auth/gmail.metadata', 'https://www.googleapis.com/auth/gmail.settings.basic']

LastEmail = None

def main():
    global LastEmail
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build('gmail', 'v1', credentials=creds)
        
        
       
       
        
        results = service.users().messages().list(userId='me',labelIds = ['INBOX'],q = "is:unread").execute()
        messages = results.get('messages', [])
        # print(messages)
        print(len(messages))
        list_of_messages = []
        
        if not messages:
            print('No messages found.')
        else:
            messages_count = 0
            for i in range(0,1):
                msg = service.users().messages().get(userId='me', id=messages[i]['id']).execute()
                list_of_messages.append(msg)
                messages_count += 1
                print(messages_count)
            count =0
            for messege in messages:
                if count != 1:
                    count += 1
                else:
                    break
                msg = service.users().messages().get(userId='me', id=messege['id']).execute()
                body = ''
                try:
                    body = msg['payload']['parts'][0]['body']['data']
                except:
                    try:
                        body =  msg['payload']['parts'][1]['body']['data']
                    except:
                        try:
                            body = msg['payload']['body']['data']
                        except:
                            pass
                email_data = msg['payload']['headers']
                for values in email_data:
                    name = values['name']                
                    if name == 'From':
                        from_email = values['value']
                        if  LastEmail != None and LastEmail == {"from":from_email,"subject":msg['snippet'],"date":msg['internalDate'],"body":base64.urlsafe_b64decode(body).decode('utf-8')}:
                            return {"from":"", "subject":"", "date":"", "body":""}
                            # print("\t\t\t\t...\t\t\t\t\n\n")
                        print("\t\t\t\t\t\t\t\t\n\n")
                        print("From: "+from_email)
                        print("Subject: "+msg['snippet'])
                        print("Date: "+msg['internalDate'])
                        print("Body: "+ base64.urlsafe_b64decode(body).decode('utf-8'))
                        # print(msg)
                        LastEmail = {"from":from_email,"subject":msg['snippet'],"date":msg['internalDate'],"body":base64.urlsafe_b64decode(body).decode('utf-8')}
                        return LastEmail
                        # print("\t\t\t\t...\t\t\t\t\n\n")

    
                        # # print(from_email)
                        # time.sleep(1)
            else:
                print("No new emails")
        # labels = results.get('labels', [])

        # if not labels:
        #     print('No labels found.')
        #     return
        # print('Labels:')
        # for label in labels:
        #     print(label['name'])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    while True:
        resp = main()
        if resp == {"from":"", "subject":"", "date":"", "body":""}:
            print("No new emails")
        else:  
            print(resp)
            
        time.sleep(5)
import email
import imaplib
import mimetypes
import os


username = 'GMail account'
password = 'Your password'

mail = imaplib.IMAP4_SSL('imap.gmail.com') #https://google.com/settings/security/lesssecureapps
mail.login(username, password)

mail.select('inbox')

#Create new folder
mail.create('Folder1')

#List folders
mail.list()

result, data = mail.uid('search', None, 'ALL')

inbox_item_list = data[0].split()

for item in inbox_item_list:
	result2, email_data = mail.uid('fetch', item, '(RFC822)')
	raw_email = email_data[0][1].decode('utf-8')
	email_message = email.message_from_string(raw_email)
	to_ = email_message['To']
	from_ = email_message['From']
	subject_ = email_message['Subject']
	date_ = email_message['date']
	counter = 1
	for part in email_message.walk():
		if part.get_content_maintype() == 'multipart':
			continue
		filename = part.get_filename()
		content_type = part.get_content_type()
		if not filename:
			ext = mimetypes.guess_extension(content_type)
			if not ext:
				ext = '.bin'
			if 'text' in content_type:
				ext = '.txt'
			if 'html' in content_type:
				ext = '.html'
			filename = 'msg-part-%08d%s' %(counter, ext)
		counter += 1
	#save file
	save_path = os.path.join(os.getcwd(), 'emails', subject_)
	if not os.path.exists(save_path):
		os.makedirs(save_path)
	with open(os.path.join(save_path, filename), 'wb') as fp:
		fp.write(part.get_payload(decode=True))

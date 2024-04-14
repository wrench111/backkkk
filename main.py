import pyrebase
import datetime
import os


user_info={}
firebaseConfig = {
  "apiKey": "AIzaSyA4f3AO0Y7eMK9iAd_Mz07TP3Du3siJvHk",
  "authDomain": "denis-bc788.firebaseapp.com",
  "databaseURL": "https://denis-bc788-default-rtdb.firebaseio.com/",
  "projectId": "denis-bc788",
  "storageBucket": "denis-bc788.appspot.com",
  "messagingSenderId": "855759274571",
  "appId": "1:855759274571:web:6b9226ca4454c8b0fb43ce",
  "measurementId": "G-58HVNQ0C55"}

firebase = pyrebase.initialize_app(firebaseConfig)
auth=firebase.auth()
db=firebase.database()
storage=firebase.storage()

def signin(email, password, flag=True):
  global user_info
  try:
    user=auth.sign_in_with_email_and_password(email, password)
    user_info['id'] = user['localId']
    user_page = dict(db.child('users').child(user['localId']).get().val())
    user_info = dict(list(user_info.items()) + list(user_page.items()))
    return docs_info(user['localId'])
  except Exception as ex:
    print('Неыкрный логин или пароль')
    print(ex)

def docs_info(user_id):
  data=db.child('users').child(user_id).get()
  files=dict(data.val())['docs']
  full_info={}
  for file in files:
    file_dict=list(dict(db.child('docs').get().val()).values())
    full_info[file]=file_dict[file-1]
  return full_info


def create():
  filename=input()
  type=input()
  name=input()
  storage.child(filename).put(filename)
  data={'type': type,'sender': user_info['name'],'organisation': user_info['org'],'theme': name,'time': '.'.join(str(datetime.datetime.now())[2::].split()[0].split('-')[::-1]), 'status': False, 'name':filename}
  q=db.child('docs').get()
  mx=q.val()
  last=q.each()[-1].key()
  last_doc=db.child('docs').get().each()[-1].key()
  db.child('users').child(user_info['id']).child('docs').update({int(last)+1:len(mx)+1})
  db.child('docs').child(int(last_doc)+1).set(data)


def downloadd(num):
  dir=r"C:\Users\User\Downloads"
  docs=list(db.child('docs').get().val().values())
  docs=[i for i in docs if i != None]
  doc_name=docs[num-1]['name']
  storage.child(doc_name).download('', doc_name)
  flag=True
  k=0
  cur_dir=os.getcwd()
  while True:
    k+=1
    try:
      if flag:
        flag=False
        os.rename(rf"{cur_dir}\{doc_name}", rf"{dir}\{doc_name}")
      else:
        os.rename(rf"{cur_dir}\{doc_name}", rf"{dir}\{doc_name.split('.')[0]} ({k}).{doc_name.split('.')[1]}")
    except Exception as ex:
      if 'Не удается найти указанный файл' in str(ex):
        break
      print(ex)
def send(id):
  num=db.child('users').child('E258W587qleAw31PmNsT4bZZyJ73').child('docs').get().val()
  num=[c for c in num if c !=None]
  if id not in num:
    db.child('users').child('E258W587qleAw31PmNsT4bZZyJ73').child('docs').update({len(num)+1:id})
  else:
    print('Этот файл уже есть у пользователя')


if __name__=='__main__':
  # signin('mrteh@gmail.com', '123456789')
  # create()
  downloadd(3)


#Mfx8seI9LcUZ6eg55hST8kzPzeL2
#C:\Users\mrteh\Downloads
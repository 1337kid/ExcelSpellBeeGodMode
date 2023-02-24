import requests,sys
d=requests.get('https://spelling-bee-five.vercel.app/api/question')
jsondata=d.json()
#==
refresh_token='your refresh token here'
words_new=[]
question_id=jsondata['_id']
letters=jsondata['letters']
mainletter=jsondata['mainLetter']
#==
def refresh(r_token):
    new_token=requests.post('https://accountsbackend-xgveswperq-uc.a.run.app/auth/refresh',headers={'Content-Type': 'application/json'},json={'refreshToken':refresh_token}).json()['accessToken']
    return new_token
def get_score(token):
    Headers={'Content-Type': 'application/json','Authorization':'Bearer '+token}
    d=requests.post('https://spelling-bee-five.vercel.app/api/getTodayScoreAndAnswersByUser',headers=Headers,json={'questionId':question_id}).json()
    return str(d['totalScore'])
asdf=int(input('Pick any\n1) Tiny wordlist (lower score)\n2) Large wordlist (higher score)\nChoice:'))
if asdf==1:wlits='tiny.txt'
elif asdf==2:wlits='large.txt'
else:sys.exit()
words=open(wlits).readlines()
words_tmp=words[:]
for i in words_tmp:
    for j in i.strip('\n'):
        if j.upper() not in letters+[mainletter]:
            words.remove(i)
            break
for i in words:
    if mainletter.lower() in i:words_new.append(i.strip())
for i in words_new:
    access_token=refresh(refresh_token)
    Headers={'Content-Type': 'application/json','Authorization':'Bearer '+access_token}
    d=requests.post('https://spelling-bee-five.vercel.app/api/checkAnswer',headers=Headers,json={'questionId':question_id,'answer':i.upper()}).json()
    access_token=refresh(refresh_token)
    print('Current Score: ',get_score(access_token))
access_token=refresh(refresh_token)
print('Final Score: ',get_score(access_token))

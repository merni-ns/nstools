## OLD VERSION. REQUIRES PYNATIONSTATES WRAPPER.

#RMB archiving script by Merni
#Version 2
 
import nationstates as ns
from datetime import datetime
 
#This block accepts input from the user.
print('Your useragent should have your email/NS name, as well as the purpose of this program (RMB archiving). The mods need this info.')
ua=input('Enter your useragent : ')
rname=input('Enter your region name : ')
rnamef=rname.casefold().replace(' ','_')
print('You must enter the full path of the text file, including extension. If the file is in your Python directory, you can enter the filename and extension only. If the file does not exist it will be created.')
fn=input('Enter path/name of text file : ')
adv=input('Advanced options? Y/N : ').casefold()
if adv=='y':
    print('>>>If you want to start from the first post, press Enter for the next two prompts.<<<')
    print('The archive assigns a serial number 1,2,3... to each post. If you are starting from a later post,you may want to change the first serial number. Otherwise press Enter.')
    sid=input('Enter starting post ID : ')
    sn=input('Enter starting serial number : ')
else: sid=sn=''
 
#This block sets up the API and other stuff.
nt=datetime.utcnow().strftime('%Y-%m-%d at %H:%M:%S UTC')
init=1 if sn=='' else int(sn)
n=init
f=open(fn,mode='a+',errors='replace')
api=ns.Nationstates(ua)
reg=api.region(rnamef)
pid='0' if sid=='' else sid
start='\nArchive starts from Post ID '+pid+' as Post '+str(n)+'\n'+'='*80 if pid!='0' or n!=1 else '' # Adds archive start info to heading
 
#Prints the heading to the file.
f.write('='*80+'\n'+rname+' NationStates RMB Archive\non '+nt+'\n'+'='*80+'\nPython script by Merni\npynationstates API wrapper by DolphDev (github)/United Island Tribes (NS)\n'+'='*80+start)
 
while True:
    #Gets messages as list 'msgs' of dicts
    shd=ns.Shard('messages',limit='100',fromid=str(int(pid)+1))
    x=reg.get_shards(shd)
    if x['messages']==None or x['messages']['post']==None: break
    msgs=x['messages']['post']
 
    for i in msgs:
        #unpacks individual attributes of each message (i) and processed them to be ready to write
        t=int(i['timestamp'])
        dt=datetime.utcfromtimestamp(t).strftime('%Y-%m-%d at %H:%M:%S UTC')
        #Previous line by 'rkachach' at Stack Overflow
        poster=i['nation']
        pid=i['id']
        likes=int(i['likes'])
        status=int(i['status'])
        if likes!=0:
            likers=i['likers']
        else:
            likers=''
        if status==1:
            stat='suppressed by '
            supp=i['suppressor']
        elif status==2:
            stat='self-deleted'
            supp=''
        elif status==9:
            stat='moderator deleted'
            supp=''
        else:
            stat=supp=''
        mess=i['message']
        if mess==None: mess=''
 
        #writes message to file
        f.write('\n'+('-'*80)+'\n'+pid+': Post '+str(n)+' by '+poster+' on '+dt+'\nLikes: '+str(likes)+'('+likers+')'+'\n'+stat+supp+'\n'+mess)
 
        n=n+1 #next serial post number
 
    print(n-init) # this prints the number of msgs saved to the output screen every 100 msgs
 
print('Archival appears to have finished. Check the text file.')
f.close()

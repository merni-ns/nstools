## OLD VERSION. REQUIRES PYNATIONSTATES WRAPPER.
import nationstates as ns
from datetime import datetime
n=1
f=open('ENTER FILENAME',mode='a',errors='replace')
api=ns.Nationstates('ENTER YOUR USERAGENT: NS/EMAIL AND DESCRIPTION OF WHAT YOU ARE USING THE API FOR')
reg=api.region('ENTER REGION NAME')
pid='0'
while True:
    shd=ns.Shard('messages',limit='100',fromid=str(int(pid)+1))
    x=reg.get_shards(shd)
    msgs=x['messages']['post']
    for i in msgs:
        t=int(i['timestamp'])
        dt=datetime.utcfromtimestamp(t).strftime('%Y-%m-%d at %H:%M:%S GMT')
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
        f.write('\n'+('-'*80)+'\n'+pid+': Post '+str(n)+' by '+poster+' on '+dt+'\nLikes: '+str(likes)+'('+likers+')'+'\n'+stat+supp+'\n'+mess)
        n=n+1
    print(n) # this prints the number of msgs saved to the output screen every 100 msgs
f.close()

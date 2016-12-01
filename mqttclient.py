total_x=0
total_x10=0
total_mis=0
summ=0
round_count=0
subject="tw/arch_score"
tdlist=" "
#tdlist="\
# 0.0.0.0.0.0 \n 0.0.0.0.0.0 \n\
# 0.0.0.0.0.0 \n 0.0.0.0.0.0 \n\
# 0.0.0.0.0.0 \n 0.0.0.0.0.0 \n"

import sys
import paho.mqtt.client as mqtt
from datetime import datetime


def remem(org_score,round_count):
    global tdlist
    if round_count>0 :
        print("-----------------")
        if round_count==1 :
            tdlist=" "+org_score
        else :
            tdlist=tdlist+"\n "+org_score
            
        print (tdlist,"\n-----------------")
    else :
        print ("ready to start!")
    #tdlist=org_score
    #result=list(map(str, org_score.split('.')))

def scoreing(msg1,client1):
       global total_x
       global total_x10
       global total_mis
       global summ
       global round_count
       #print(msg.topic+"-->"+str(msg.payload))
       if round_count>0 :
             org_score=str(msg1.payload)
             org_score=org_score.replace("b","")
             org_score=org_score.replace("'","")
             org_score=org_score.replace("x","X")
             org_score=org_score.replace("m","M")
             print("\n \n  Round",round_count," -> "+org_score)
             x_num=org_score.count('X')  # number of X
             reint1=org_score.replace('X','10')     #x -> 10
             x10_num=reint1.count('10')  #number of X+10
             reint2=reint1.replace('M','0')        #m -> 0
             mis_num=org_score.count('M')
             result=list(map(int, reint2.split('.')))
             arrow_amount=len(result)
             if arrow_amount<6 :
                 print("Too less... only ",arrow_amount," arrows, it should be 6")
             elif arrow_amount>6 :
                 print("Too many... ",arrow_amount," is more than 6")
             else :
              #--------- adding to total score----------
                 total_x=total_x+x_num;
                 total_x10=total_x10+x10_num
                 total_mis=total_mis+mis_num
                 summ=summ+sum(result)
              #--------- recode the detail score--------
                 print("  Sub tot : ",sum(result),"\n\n")
                 remem(org_score,round_count)
                 print("Total : ",summ)
                 print("X : ",total_x,",   X+10 : ",total_x10,",   M : ",total_mis)
              #--------- ending  this round----------
                 round_count=round_count+1
                 print("\n========================")
                 if round_count>6 :
                     print("END of Game")
                     client1.loop_stop()
                     text_file = open("Output.txt", "a+")
                     timeing=str(datetime.now())
                     text_file.write("\n===================================================\n")
                     text_file.write("this is the score recade at \"%s\" and shot by \"%s\"\n" %(timeing , subject))
                     text_file.write("%s\n" %tdlist)
                     text_file.write("---------------------\n")
                     temp_line="Total Sum : "+str(summ)
                     text_file.write("%s\n" %temp_line )
                     temp_line="X : "+str(total_x)+",   X+10 : "+str(total_x10)+",   M : "+str(total_mis)
                     text_file.write("%s\n" %temp_line )
                     text_file.close()
                        #clear up
                     total_x=0
                     total_x10=0
                     total_mis=0
                     summ=0
                     round_count=0
                     client.publish("tw/arch_score","0.0.0.0.0.0",0)
                     quit()
       else :
            print ("start scoreing !!! Link is estabish\n")
            round_count=round_count+1




# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with Error respones: "+str(rc))
    client.subscribe("tw/arch_score")
# Subscribing in on_connect() means that if we lose the connection and
# reconnect then subscriptions will be renewed.


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+"-->"+str(msg.payload))
    scoreing(msg,client)
       
def on_publish(client, msgs,mid):
    dammy_list=0


print (tdlist)
client = mqtt.Client()
client.username_pw_set('id_here','password_here')
#client.subscribe("tw/arch_score")
client.on_connect = on_connect
client.on_message = on_message
client.on_publish = on_publish
client.connect("server_ip_here", server_port_here, 60)
client.publish("tw/arch_score","0.0.0.0.0.0",0)


# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever(1) #chack update every sec

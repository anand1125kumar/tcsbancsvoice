import boto3
import random
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
import datetime

global username
global loginFlag


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to Tata Consultancy Services Bancs solution, turning our technology to your advantage, we offer a large variety insurance products at an affordable premium. I can help you to buy a policy online best suited to your needs. Would you like to proceed to buy a life insurance policy online or login to TCS bancs voice portal.").set_should_end_session(False)
        return handler_input.response_builder.response 
################################# I would like yo buy a policy online ##################################################################################
class BancsRegisterUserIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterUserIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Great!, Please tell what should be your user name for online registration").set_should_end_session(False)
        return handler_input.response_builder.response
#####################################################################################################################
############################### My user name for registration should be ****** ####################################
class BancsRegisterUserNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterUserNameIntent")(handler_input)

    def handle(self, handler_input):
        
        username = handler_input.request_envelope.request.intent.slots['username'].value
        username = str(username.lower())

        ########################### verify existing user #############################################################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('BancsLogin')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except Exception:
            status = 'inactive'
            
              
        try: 
            status = data1['Item']['status']
            status = status.lower()

        except Exception:
            status = 'inactive'


        
            

        ################################################################################################################

        if status != 'active':

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Log')
                data1 = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('BancsLogin')
                data1 = table.put_item(
                    Item={
                        'username': username,
                        'status': 'active'
                        
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)


            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Temp')
                data1 = table.put_item(
                    Item={
                        'username': username,
                        'status': 'False'
                    
                    }
                )
            except BaseException as e:
                print(e)
                raise(e)



            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data1 = table.put_item(
                    Item={
                        'username': username
                        
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

            speak_text = "OK, Please set your 4 digit pin"


        else:
            speak_text = 'username already exists, please try some other username'


        handler_input.response_builder.speak(speak_text).set_should_end_session(False)
        return handler_input.response_builder.response
########################################################################################################################
############################### My pin should be ****** ####################################
class BancsRegisterPasswordIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterPasswordIntent")(handler_input)

    def handle(self, handler_input):

        pin = handler_input.request_envelope.request.intent.slots['pin'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        pin = str(pin)
    ##############################################################################

        try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('BancsLogin')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set password=:pn",
                        ExpressionAttributeValues={':pn': pin}         
                                                
                    )

        except BaseException as e:
                print(e)
                raise(e)

        handler_input.response_builder.speak("OK, Please tell your full name").set_should_end_session(False)
        return handler_input.response_builder.response
########################################################################################################################
############################### My full name is ****** ####################################
class BancsRegisterFullNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterFullNameIntent")(handler_input)

    def handle(self, handler_input):

        fullname = handler_input.request_envelope.request.intent.slots['fullname'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('BancsLogin')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set fullname=:fn",
                    ExpressionAttributeValues={':fn': fullname}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("OK, Please tell your current city").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################

########################################################################################################################
############################### My current city is ****** ####################################
class BancsRegisterCityIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterCityIntent")(handler_input)

    def handle(self, handler_input):

        city1 = handler_input.request_envelope.request.intent.slots['city'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update city in bancs login table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('BancsLogin')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set city=:ln",
                    ExpressionAttributeValues={':ln': str(city1)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)


        

        handler_input.response_builder.speak("OK, please tell me how much insurance cover amount you want").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################

############################### Insurance cover amount should be ****** ####################################
class BancsRegisterCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramount = handler_input.request_envelope.request.intent.slots['coveramount'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update cover amount  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set coveramount=:ca",
                    ExpressionAttributeValues={':ca': str(coveramount)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)


        

        handler_input.response_builder.speak("OK, please tell me how much should be the term of the insurance").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################


############################### Insurance term should be ****** ####################################
class BancsRegisterInsuranceTermIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsRegisterInsuranceTermIntent")(handler_input)

    def handle(self, handler_input):

        term = handler_input.request_envelope.request.intent.slots['term'].value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)
        

        ## update cover amount  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set term=:ca",
                    ExpressionAttributeValues={':ca': int(term)}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)

        ############################ fetch cover amount    #####################

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Policy_Details')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        coveramount = data1['Item']['coveramount']

        coveramount = int(coveramount)
        term = int(term)

        policynumber = random.randint(100000000000,999999999999)
        #policynumber = '112211221122'
        premiumamount = coveramount/(term*120)
        premiumamount = "{:.2f}".format(premiumamount)

        today = datetime.datetime.today()
        

        dd = "05"
        mm = int(today.month)
        yy = int(today.year)

        if(mm < 12):
            mm = mm + 1
        else:
            mm = 1
            yy = yy + 1

        mm =str(mm)
        yy = str(yy)

        nextduedate = dd+"-"+mm+"-"+yy
        today = str(today.day) +"-"+ str(today.month) +"-"+ str(today.year)
        
        ## update policy number  in bancs policy details table ##########
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Policy_Details')
            data = table.update_item(
                Key={
                    'username': username
                    },
                    UpdateExpression="set policynumber=:pn, premiumamount=:pa, premiumduedate=:pdd,advisorname=:adv",
                    ExpressionAttributeValues={':pn': str(policynumber), ':pa': str(premiumamount), ':pdd': nextduedate, ':adv': 'TCS BaNCS Voice'}         
                                                
                )

        except BaseException as e:
            print(e)
            raise(e)



        handler_input.response_builder.speak("Congratulations, you have successfully purchased a policy from world leading insurance company today, the  "+str(today)+", we will provide the best in class insurance services, your policy number is "+str(policynumber)+", your premium amount is "+str(premiumamount)+" rupees and your next premium due is on "+str(nextduedate)+", Please let me know if you need any other services. Thank you").set_should_end_session(False)
        return handler_input.response_builder.response

########################################################################################################################


#########################################################################################################################
class BancsLoginIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsLoginIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Please tell your user name").set_should_end_session(False)
        return handler_input.response_builder.response


class BancsUserNameIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsUserNameIntent")(handler_input)

    def handle(self, handler_input):
        username = handler_input.request_envelope.request.intent.slots['username'].value
        username = username.lower()
        try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Log')
                data1 = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
        except BaseException as e:
               print(e)
               raise(e)

        handler_input.response_builder.speak("Please tell your pin").set_should_end_session(False)
        return handler_input.response_builder.response




######################################## 10-Oct-2020  #####################################################

class BancsPremiumAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsPremiumAmountIntent")(handler_input)


    #fetch premium amount
    

    def handle(self, handler_input):
        
        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)

    ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        if(status == 'True'):
        #####################################################################
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                premiumamount = str(data['Item']['premiumamount'])
                print(premiumamount)

                speakText = "Your next premium due amount is Rupees "+premiumamount

              
            except BaseException as e:
                print(e)
                raise(e) 
        else:
                speakText = "Please enter valid username and pin for successfull login."

        
        
        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response

###########################################################################################################
#BancsPINIntentHandler
#BancsLoginDetailsIntentHandler
class BancsPINIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsPINIntent")(handler_input)

    def handle(self, handler_input):

        pin = handler_input.request_envelope.request.intent.slots['pin'].value
        #pin = str(pin)
        #a = username.split(' and ')
        #b = a[1].replace("pin is ","")

        #username = a[0].lower()
        #pin = b
        #print(pin)

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
        except BaseException as e:
            print(e)
            raise(e)

        username = str(data['Item']['username'])
        

       # pin = handler_input.request_envelope.request.intent.slots['pin'].value
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('BancsLogin')
            data = table.get_item(
                Key={
                    'username': username
                    }
            )
        except BaseException as e:
            print(e)
            raise(e)


        pinActual = str(data['Item']['password'])

        if(pin != pinActual):
            speech_text = "Invalid username and pin, please try again."
           # speech_text = "pin actual = "+pinActual+"pin entered = "+str(pin)
            loginFlag = 'False'
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Log')
                data = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   'null'
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)

        else:
            speech_text = "Hello " + data['Item']['fullname'] + ".   You have successfully logged in TCS Bancs application,    hope you are doing great, your current location is " + data['Item']['city'] + ".   How may I help you?"
            loginFlag = 'True'
        
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Log')
                data = table.put_item(
                    Item={
                        'SerialNumber': '1',
                        'username':   username
                        }
                )
            except BaseException as e:
                print(e)
                raise(e)


            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Temp')
                data = table.put_item(
                    Item={
                        'username': username,
                        'status':   loginFlag
                        }
                    )
            except BaseException as e:
                print(e)
                raise(e)

            

        #speech_text = username + "and" + b

        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response  

#########  Fetch Premium Due Date   #######################################################################

class BancsPremiumDueDateIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsPremiumDueDateIntent")(handler_input)

    def handle(self, handler_input):

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)

        #####################################################################
        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        if(status =='True'):

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                premiumduedate = data['Item']['premiumduedate']          
                speakText = "Your next premium due date is "+str(premiumduedate)

                     
            except BaseException as e:
                print(e)
                raise(e) 
        
        else:
            speakText = "Please enter valid username and pin for successfull login."

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################


#########  Fetch cover amount   #######################################################################

class BancsViewCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsViewCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )

                coveramount = str(data['Item']['coveramount'])
            

                speakText = "Your total insurance cover amount is Rupees "+coveramount

              
            except BaseException as e:
                print(e)
                raise(e) 

        else:
            speakText = "Please enter valid username and pin for successfull login."

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

#########  Increase cover amount   #######################################################################

class BancsIncreaseCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsIncreaseCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramountincrease = handler_input.request_envelope.request.intent.slots['coveramountincrease'].value
        #coveramountincrease = str(coveramountincrease)

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )
                coveramount = data['Item']['coveramount']
                newCoverAmount = int(coveramount)+int(coveramountincrease)
                newCoverAmount = str(newCoverAmount)          

                speakText = "Ok Your insurance total cover amount has been successfully updated to Rupees "+newCoverAmount

                ########  Premium Calculation   #############
                insuranceTerm = int(data['Item']['term'])
                newCoverAmount = int(newCoverAmount)
                premiumamount = newCoverAmount/(insuranceTerm*120)
                premiumamount = "{:.2f}".format(premiumamount)
                ##############################################

            except BaseException as e:
                print(e)
                raise(e) 

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set coveramount=:ca, premiumamount = :pa",
                        ExpressionAttributeValues={':ca': str(newCoverAmount), ':pa': str(premiumamount)}         
                                                
                    )

            except BaseException as e:
                print(e)
                raise(e)


        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

#########  Decrease cover amount   #######################################################################

class BancsDecreaseCoverAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsDecreaseCoverAmountIntent")(handler_input)

    def handle(self, handler_input):

        coveramountdecrease = handler_input.request_envelope.request.intent.slots['decreasecoveramount'].value
        #coveramountdecrease = str(coveramountdecrease)

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 
        print(username)


        ##### FETCH login status ########################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.get_item(
                Key={
                    'username': username
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        status = data1['Item']['status']
        status = str(status)
    ####################################################

        #####################################################################
        if(status == 'True'):
            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.get_item(
                    Key={
                        'username': username
                        }
                )
                coveramount = data['Item']['coveramount']
                newCoverAmount = int(coveramount) - int(coveramountdecrease)
                newCoverAmount = str(newCoverAmount)          

                speakText = "OK, Your total insurance cover amount has been successfully updated to Rupees "+newCoverAmount

                ########  Premium Calculation   #############

                insuranceTerm = int(data['Item']['term'])
                newCoverAmount = int(newCoverAmount)
                premiumamount = newCoverAmount/(insuranceTerm*120)
                premiumamount = "{:.2f}".format(premiumamount)


                ##############################################

            except BaseException as e:
                print(e)
                raise(e) 

            try:
                dynamodb = boto3.resource('dynamodb')
                table = dynamodb.Table('Bancs_Policy_Details')
                data = table.update_item(
                    Key={
                        'username': username
                        },
                        UpdateExpression="set coveramount=:ca, premiumamount = :pa",
                        ExpressionAttributeValues={':ca': str(newCoverAmount), ':pa': str(premiumamount)}         
                                                
                    )

            except BaseException as e:
                print(e)
                raise(e)


        else:
            speakText = "Please enter valid username and pin for successfull login."               

        handler_input.response_builder.speak(speakText).set_should_end_session(False)
        return handler_input.response_builder.response
#########################################################################################################################

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again!!").set_should_end_session(False)
        return handler_input.response_builder.response

class LogoutIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("LogoutIntent")(handler_input)

    def handle(self, handler_input):


        #usname = Intent.slots.username.value

        ## Fetch username from Bancs_log table##############################
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data1 = table.get_item(
                Key={
                    'SerialNumber': '1'
                    }
            )
              
        except BaseException as e:
            print(e)
            raise(e)    

        username = data1['Item']['username'] 

        #####################################################################

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data = table.put_item(
                Item={
                       'username': username,
                       'status':   'false'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e) 

            
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Log')
            data = table.put_item(
                Item={
                       'SerialNumber': '1',
                       'username': 'null'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e)

        handler_input.response_builder.speak("You have successfully logged out from TCS Bancs! Bye, take care of yourself, it was nice talking to you, I would like to meet you again.").set_should_end_session(True)
        return handler_input.response_builder.response


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BancsLoginIntentHandler())
sb.add_request_handler(BancsUserNameIntentHandler())
sb.add_request_handler(BancsPremiumAmountIntentHandler())
sb.add_request_handler(BancsPINIntentHandler())
sb.add_request_handler(BancsRegisterCityIntentHandler())
sb.add_request_handler(BancsPremiumDueDateIntentHandler())
sb.add_request_handler(BancsViewCoverAmountIntentHandler())
sb.add_request_handler(BancsIncreaseCoverAmountIntentHandler())
sb.add_request_handler(BancsDecreaseCoverAmountIntentHandler())
sb.add_request_handler(BancsRegisterUserIntentHandler())
sb.add_request_handler(BancsRegisterUserNameIntentHandler())
sb.add_request_handler(BancsRegisterPasswordIntentHandler())
sb.add_request_handler(BancsRegisterFullNameIntentHandler())
sb.add_request_handler(BancsRegisterCoverAmountIntentHandler())
sb.add_request_handler(BancsRegisterInsuranceTermIntentHandler())
sb.add_request_handler(LogoutIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)

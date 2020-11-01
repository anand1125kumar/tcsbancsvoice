import boto3
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name

global username
global loginFlag


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Welcome to Tata Consultancy Services Bancs solution, turning our technology to your advantage.").set_should_end_session(False)
        return handler_input.response_builder.response 

class BancsLoginIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsLoginIntent")(handler_input)

    def handle(self, handler_input):
        handler_input.response_builder.speak("Please tell your user name and pin").set_should_end_session(False)
        return handler_input.response_builder.response

######################################## 10-Oct-2020  #####################################################

class BancsPremiumAmountIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsPremiumAmountIntent")(handler_input)


    #fetch premium amount
    

    def handle(self, handler_input):
    
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.put_item(
                Item={
                    'username': 'ankita',
                    'status':   'qwert'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e)
        
        handler_input.response_builder.speak("Successfully updated login status").set_should_end_session(False)
        return handler_input.response_builder.response

###########################################################################################################

class BancsLoginDetailsIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("BancsLoginDetailsIntent")(handler_input)

    def handle(self, handler_input):

        username = handler_input.request_envelope.request.intent.slots['username'].value
        a = username.split(' and ')
        b = a[1].replace("pin is ","")

        username = a[0].lower()
        pin = b


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

        if(pin != data['Item']['password']):
            speech_text = "Invalid username and pin, please try again."
            loginFlag = 'false'

        else:
            speech_text = "Hello " + data['Item']['fullname'] + ".   You have successfully logged in TCS Bancs application,    hope you are doing great, your current location is " + data['Item']['location'] + ".   How may I help you?"
            loginFlag = 'true'
        
        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.put_item(
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

class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        print(exception)
        handler_input.response_builder.speak("Sorry, there was some problem. Please try again!!").set_should_end_session(False)
        return handler_input.response_builder.response

class CancelIntentHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input):
        return True

    def handle(self, handler_input):

        try:
            dynamodb = boto3.resource('dynamodb')
            table = dynamodb.Table('Bancs_Temp')
            data1 = table.put_item(
                Item={
                       'status':   'false'
                    }
              )
        except BaseException as e:
            print(e)
            raise(e)        
        handler_input.response_builder.speak("Bye, you have successfully logged out from TCS Bancs!!").set_should_end_session(True)
        return handler_input.response_builder.response


sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(BancsLoginIntentHandler())
sb.add_request_handler(BancsLoginDetailsIntentHandler())
sb.add_request_handler(BancsPremiumAmountIntentHandler())
sb.add_request_handler(CancelIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

def handler(event, context):
    return sb.lambda_handler()(event, context)

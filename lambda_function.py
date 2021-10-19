# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response
import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
API_URL = "https://c93b-152-166-113-56.ngrok.io"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        speak_output = "Welcome to your custom Liquor Store, how can I help you?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ListProductsIntentHandler(AbstractRequestHandler):
    """Handler for intent ListProducts."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListProducts")(handler_input)

    def handle(self, handler_input):
        
        speak_output = ""
        url = "{}/products".format(API_URL)
        response = requests.get(url)
        if response.status_code == 200:
            speak_output = response.text
        else:
            speak_output = "I had trouble getting the info you ask."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class GetProductIntentHandler(AbstractRequestHandler):
    """Handler for intent GetProduct."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("GetProduct")(handler_input)

    def handle(self, handler_input):
        
        speak_output = ""
        product_name = handler_input.request_envelope.request.intent.slots['product'].value
        url = "{}/products/{}".format(API_URL, product_name)
        response = requests.get(url)
        if response.status_code == 200:
            speak_output = response.text
        else:
            speak_output = "I had trouble getting the product info you ask."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class AddProductToCartIntentHandler(AbstractRequestHandler):
    """Handler for intent AddProductToCart."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("AddProductToCart")(handler_input)

    def handle(self, handler_input):
        
        speak_output = ""
        product_name = handler_input.request_envelope.request.intent.slots['product_name'].value
        count = handler_input.request_envelope.request.intent.slots['count'].value
        url = "{}/cart/{}/{}".format(API_URL, product_name, count)
        response = requests.get(url)
        if response.status_code == 200:
            speak_output = response.text
        else:
            speak_output = "I had trouble adding the product to the cart."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class PlaceOrderIntentHandler(AbstractRequestHandler):
    """Handler for intent PlaceOrder."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("PlaceOrder")(handler_input)

    def handle(self, handler_input):
        
        speak_output = ""
        url = "{}/order".format(API_URL)
        response = requests.get(url)
        if response.status_code == 200:
            speak_output = response.text
        else:
            speak_output = "I had trouble processing the checkout."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class ListShoppingCartIntentHandler(AbstractRequestHandler):
    """Handler for intent ListShoppingCart."""
    def can_handle(self, handler_input):
        return ask_utils.is_intent_name("ListShoppingCart")(handler_input)

    def handle(self, handler_input):
        
        speak_output = ""
        url = "{}/cart".format(API_URL)
        response = requests.get(url)
        if response.status_code == 200:
            speak_output = response.text
        else:
            speak_output = "I had trouble processing the checkout."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ListProductsIntentHandler())
sb.add_request_handler(GetProductIntentHandler())
sb.add_request_handler(AddProductToCartIntentHandler())
sb.add_request_handler(PlaceOrderIntentHandler())
sb.add_request_handler(ListShoppingCartIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
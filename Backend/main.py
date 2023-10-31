import openai
import json
from flask import Flask, request, jsonify
import requests
from flask_cors import CORS


main = Flask(__name__)
CORS(main)
api_key=""
openai.api_key = api_key

wkey=""
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+"d5a257e58bbbbcb2186b37ebf3a761a3"+"&units=metric&sys=unix")
    data=response.json()
    weather_info= {
      "location": data["name"],
      "temperature": data["main"]["temp"],
      "unit": "celsius",
      }
    # weather_info = {
    #     "location": "delhi",
    #     "temperature": "72",
    #     "unit": unit,
    #     "forecast": ["sunny", "windy"],
    # }
    return json.dumps(weather_info)

@main.route("/getweather",methods=['POST'])
def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    data = request.json
    user_input = data.get("chat")
    # messages = [{"role": "user", "content": user_input}]
    messages = user_input
    functions = \
    [
        {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters":
            {
                "type": "object",
                "properties":
                    {
                    "location":
                        {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                         },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                "required": ["location"],
            }
        }


    ]

    # calling chat gpt api

    response = openai.ChatCompletion.create(

        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]



    print(response_message)

    # Step 2: check if GPT wanted to call a function

    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response

    else:
        return response





if __name__ == '__main__':
    main.run(debug=True)



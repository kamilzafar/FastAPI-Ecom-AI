import asyncio
import time
from openai import OpenAI
from ecom.utils.settings import ASSISTANT_ID, OPENAI_API_KEY
from openai.types.beta import Assistant
from openai.types.beta.threads import Run
import requests
import json

assistant_id = str(ASSISTANT_ID)

TOKEN =  "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJrYW1pbCIsImV4cCI6MTcxMzc4MzE4M30.ODEwzOsip8f85lb4p7m67LGFUctnqqmfgy2EZn1RgiA"

def get_order():
    url = "http://127.0.0.1:8000/api/orders"
    response = requests.get(url, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

def get_products():
    url = "http://127.0.0.1:8000/api/products"
    response = requests.get(url)
    return json.dumps(response.json())

def post_cart(product_id, quantity, size):
    url = "http://127.0.0.1:8000/api/cart"
    response = requests.post(url,json={"product_id": product_id, "qauntity": quantity, "size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

def update_cart(product_id, quantity, size):
    url = "http://127.0.0.1:8000/api/cart"
    response = requests.patch(url,json={"product_id": product_id, "qauntity": quantity, "size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())
    
def delete_cart(product_id, quantity, size):    
    url = "http://127.0.0.1:8000/api/cart"
    response = requests.delete(url,json={"product_id": product_id, "qauntity": quantity, "size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

def post_order(payment_method, first_name, last_name, address, city, state, contact_number):
    url = "http://127.0.0.1:8000/api/order"
    response = requests.post(url,json={"payment_method": payment_method, "first_name": first_name, "last_name": last_name, "address": address, "city": city, "state": state, "contact_number": contact_number}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

def update_order(payment_method, first_name, last_name, address, city, state, contact_number, order_id, order_status):
    url = "http://127.0.0.1:8000/api/order"
    response = requests.patch(url,json={"order_id": order_id, "order_status": order_status,"payment_method": payment_method, "first_name": first_name, "last_name": last_name, "address": address, "city": city, "state": state, "contact_number": contact_number}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

def cancel_order(order_id, order_status):
    url = "http://127.0.0.1:8000/api/order"
    response = requests.delete(url,json={"order_id": order_id, "order_status": order_status}, headers={f"Authorization": f"Bearer {TOKEN}"})
    return json.dumps(response.json())

available_functions = {
    "get_order": get_order,
    "get_products": get_products,
    "post_cart": post_cart,
    "update_cart": update_cart,
    "delete_cart": delete_cart,
    "post_order": post_order,
    "update_order": update_order,
    "cancel_order": cancel_order
}
from openai.types.beta.thread import Thread
from openai.types.beta.threads import Message
client = OpenAI(api_key=OPENAI_API_KEY)

def create_thread():
    thread: Thread = client.beta.threads.create()
    return thread.id

async def generate_message(prompt: str, thread_id: str) -> str:
    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    )
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        # Add run steps retrieval here
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
        print("Run Steps:", run_steps)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    response = function_to_call(**function_args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": response,
                    })

            # Submit tool outputs and update the run
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run.status == "completed":
            # List the messages to get the response
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            for message in messages.data:
                role_label = "User" if message.role == "user" else "Assistant"
                message_content = message.content[0].text.value
                print(f"{role_label}: {message_content}\n")
                return message_content
            break  # Exit the loop after processing the completed run

        elif run.status == "failed":
            print("Run failed.")
            break

        elif run.status in ["in_progress", "queued"]:
            print(f"Run is {run.status}. Waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

        else:
            print(f"Unexpected status: {run.status}")
            break

        await asyncio.sleep(1)  # Wait for a short period before checking again
        
    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

def submit_message(assistant_id, thread_id, user_message):
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(assistant_id, thread, user_input)
    return thread, run

def wait_on_run(run, thread_id):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
    while run.status == "requires_action":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id,
        )
        time.sleep(0.5)
        tool_calls = run.required_action.submit_tool_outputs.tool_calls
        tool_outputs = []

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name in available_functions:
                function_to_call = available_functions[function_name]
                response = function_to_call(**function_args)
                tool_outputs.append({
                    "tool_call_id": tool_call.id,
                    "output": response,
                })

        # Submit tool outputs and update the run
        client.beta.threads.runs.submit_tool_outputs(
            thread_id=thread_id,
            run_id=run.id,
            tool_outputs=tool_outputs
        )
    return run

def get_response(thread_id: str):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    return messages

# def generate_message(prompt: str) -> str:
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", "content": prompt}
#         ]
#     )
#     return response.choices[0].message.content


async def user_chat(thread_id: str, user_input: str):
    client.beta.threads.messages.create(
        thread_id=thread_id, role="user", content=user_input
    )

    # Run the Assistant
    run = client.beta.threads.runs.create(
        thread_id=thread_id, assistant_id=assistant_id
    )

    # Check if the Run requires action (function call)
    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        # Add run steps retrieval here
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)
        print("Run Steps:", run_steps)

        if run.status == "requires_action":
            tool_calls = run.required_action.submit_tool_outputs.tool_calls
            tool_outputs = []

            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)

                if function_name in available_functions:
                    function_to_call = available_functions[function_name]
                    response = function_to_call(**function_args)
                    tool_outputs.append({
                        "tool_call_id": tool_call.id,
                        "output": response,
                    })

            # Submit tool outputs and update the run
            client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread_id,
                run_id=run.id,
                tool_outputs=tool_outputs
            )

        elif run.status == "completed":
            # List the messages to get the response
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            for message in messages.data:
                role_label = "User" if message.role == "user" else "Assistant"
                message_content = message.content[0].text.value
                print(f"{role_label}: {message_content}\n")
                return message_content
            break  # Exit the loop after processing the completed run

        elif run.status == "failed":
            print("Run failed.")
            break

        elif run.status in ["in_progress", "queued"]:
            print(f"Run is {run.status}. Waiting...")
            time.sleep(5)  # Wait for 5 seconds before checking again

        else:
            print(f"Unexpected status: {run.status}")
            break
        
        await asyncio.sleep(1)   # Wait for a second before checking again

    # Retrieve and return the latest message from the assistant
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    response = messages.data[0].content[0].text.value

    print(f"Assistant response: {response}")  # Debugging line
    return {"response": response}
import json
import time
import asyncio
from typing import List
from openai import OpenAI
from ecom.utils.settings import OPENAI_API_KEY, ASSISTANT_ID, BACKEND_URL
import httpx

client: OpenAI = OpenAI(api_key=str(OPENAI_API_KEY))

assistant_id = str(ASSISTANT_ID)

def create_thread() -> str:
    thread = client.beta.threads.create()
    return thread.id

async def generate_message(prompt: str, thread_id: str, TOKEN: str) -> str:
    async def get_order():
        """Get all orders"""
        api_url = f"{BACKEND_URL}/api/orders"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()
        
    async def get_cart():
        """Get all products in cart"""
        api_url = f"{BACKEND_URL}/api/cart"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()
    
    async def get_products():
        """Get all products"""
        api_url = f"{BACKEND_URL}/api/products"
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url)
            return response.json()

    async def post_cart(product_id, quantity, size):
        """Add product to cart"""
        url = f"{BACKEND_URL}/api/cart"
        async with httpx.AsyncClient() as client:
            response = await client.post(url,json={"product_id": product_id, "quantity": quantity, "product_size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()

    async def update_cart(product_id, quantity, size):
        """Update product in cart"""
        url = f"{BACKEND_URL}/api/cart"
        async with httpx.AsyncClient() as client:
            response = await client.patch(url,json={"product_id": product_id, "quantity": quantity, "product_size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()
        
    async def delete_cart(product_id, quantity, size):  
        """Delete product from cart"""  
        url = f"{BACKEND_URL}/api/cart"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url,json={"product_id": product_id, "quantity": quantity, "product_size": size}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()

    async def post_order(payment_method, first_name, last_name, address, city, state, contact_number):
        """Create order"""
        url = f"{BACKEND_URL}/api/order"
        async with httpx.AsyncClient() as client:
            response = await client.post(url,json={"payment_method": payment_method, "first_name": first_name, "last_name": last_name, "address": address, "city": city, "state": state, "contact_number": contact_number}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()

    async def update_order(payment_method, first_name, last_name, address, city, state, contact_number, order_id, order_status):
        """Update order"""
        url = f"{BACKEND_URL}/api/order"
        async with httpx.AsyncClient() as client:
            response = await client.patch(url,json={"payment_method": payment_method, "first_name": first_name, "last_name": last_name, "address": address, "city": city, "state": state, "contact_number": contact_number, "id": order_id, "order_status": order_status}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()

    async def cancel_order(order_id, order_status):
        """Cancel order"""
        url = f"{BACKEND_URL}/api/order"
        async with httpx.AsyncClient() as client:
            response = await client.delete(url,json={"id": order_id, "order_status": order_status}, headers={f"Authorization": f"Bearer {TOKEN}"})
            return response.json()  

    available_functions = {
        "get_order": get_order,
        "get_cart": get_cart,
        "get_products": get_products,
        "post_cart": post_cart,
        "update_cart": update_cart,
        "delete_cart": delete_cart,
        "post_order": post_order,
        "update_order": update_order,
        "cancel_order": cancel_order
    }
    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=prompt
    )

    run = client.beta.threads.runs.create(
    thread_id=thread_id,
    assistant_id=assistant_id,
    )

    run = client.beta.threads.runs.retrieve(
    thread_id=thread_id,
    run_id=run.id,
    )

    while True:
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        # Add run steps retrieval here
        run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run.id)

        print(run.status ,'.....')

        if run.status == "requires_action":
            print(run.status ,'.....')

            if run.required_action.submit_tool_outputs and run.required_action.submit_tool_outputs.tool_calls:

                tool_calls = run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []

                for tool_call in tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name in available_functions:
                        function_to_call = available_functions[function_name]
                        if function_to_call.__name__ == "get_products":
                            response = await function_to_call(**function_args)
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(response),
                            })

                        else:
                            response = await function_to_call(**function_args)
                            tool_outputs.append({
                                "tool_call_id": tool_call.id,
                                "output": json.dumps(response),
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
                if message.role == "assistant":
                    return message.content[0].text.value
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

def get_response(thread_id: str) -> List[str]:
    message_list: List[str] = []
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for message in messages.data:
        message_content = message.content[0].text.value
        message_list.append(message_content)
        message_list.reverse()
    return message_list
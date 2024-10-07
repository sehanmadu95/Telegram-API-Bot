import http.client
import json
import asyncio  # Import asyncio to use async sleep
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' and 'YOUR_API_KEY' with your actual values
TELEGRAM_BOT_TOKEN = '7620151410:AAHSaGheLQ8R_Ir4KlHWzbqQ7P8OVKtlhO8'
API_KEY = 'ZDU4YzJlOWVjODU4MWY1OGE5Y2I5Y2JiODU2MDRjYjQ='

# Function to send the HLR request to DecisionTelecom API
def check_phone_status(phone_number):
    conn = http.client.HTTPSConnection("web.it-decision.com")
    payload = json.dumps({
        "phones": [phone_number]
    })
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    conn.request("POST", "/v1/api/hlr", payload, headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

# Function to get detailed status based on ID
def get_detailed_status(request_id):
    conn = http.client.HTTPSConnection("web.it-decision.com")
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    conn.request("GET", f"/v1/api/hlr-status?id={request_id}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)

# Define the start command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Welcome! Send a phone number to check its status.")

# Handler for receiving phone numbers and checking their status
async def check_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    phone_number = update.message.text
    if phone_number.isdigit() and len(phone_number) >= 10:
        await update.message.reply_text(f'Checking status for phone number: {phone_number}')
        
        # Check phone status
        status_data = check_phone_status(phone_number)
        print("Initial HLR response:", status_data)  # Debug print

        # Check if the response is a list and has at least one element
        if isinstance(status_data, list) and len(status_data) > 0:
            request_id = status_data[0].get('id')
            await update.message.reply_text(f'Status ID received: {request_id}. Waiting for a moment to check detailed status...')
            
            # Wait for a few seconds before checking detailed status
            await asyncio.sleep(10)  # Adjust the wait time as necessary
            
            # Get detailed status using the ID
            detailed_status = get_detailed_status(request_id)
            print("Detailed status response:", detailed_status)  # Debug print
            
            if detailed_status and 'error_code' not in detailed_status:  # Check if there is an error
                # Build a response message from the detailed status
                id = detailed_status.get('id', 'Unknown')
                phone = detailed_status.get('phone', 'Unknown')
                mcc = detailed_status.get('mcc', 'Unknown')
                mnc = detailed_status.get('mnc', 'Unknown')
                network = detailed_status.get('network', 'Unknown')
                ported = detailed_status.get('ported', 'Unknown')
                status = detailed_status.get('status', 'Unknown')
                error = detailed_status.get('error', 'Unknown')
                type_ = detailed_status.get('type', 'Unknown')  # Changed to avoid conflict with built-in type
                present = detailed_status.get('present', 'Unknown')
                status_message = detailed_status.get('status_message', 'Unknown')

                await update.message.reply_text(
                    f'ID: {id}\n'
                    f'Phone: {phone}\n'
                    f'MCC: {mcc}\n'
                    f'MNC: {mnc}\n'
                    f'Network: {network}\n'
                    f'Ported: {ported}\n'
                    f'Status: {status}\n'
                    f'Error: {error}\n'
                    f'Type: {type_}\n'
                    f'Present: {present}\n'
                    f'Status Message: {status_message}'
                )
            else:
                error_message = detailed_status.get('error_name', 'Unknown error')
                await update.message.reply_text(f'Error retrieving detailed status: {error_message}')
        else:
            await update.message.reply_text('No valid data returned from the API. Response was: ' + json.dumps(status_data))
    else:
        await update.message.reply_text('Please send a valid phone number.')

def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))
    app.run_polling()

if __name__ == '__main__':
    main()

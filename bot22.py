import http.client
import json
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
        status_data = check_phone_status(phone_number)
        print(status_data)

        if status_data:
            # Extract the ID from the response
            request_id = status_data[0].get('id')
            # Get detailed status using the ID
            detailed_status = get_detailed_status(request_id)
            print(detailed_status)
            
            if detailed_status:
                # Build a response message from the detailed status
                status_message = detailed_status.get('status_message', 'Unknown')
                network = detailed_status.get('network', 'Unknown')
                present = detailed_status.get('present', 'Unknown')
                await update.message.reply_text(
                    f'Status Message: {status_message}\n'
                    f'Network: {network}\n'
                    f'Present: {present}'
                )
            else:
                await update.message.reply_text('No detailed data returned from the API.')
        else:
            await update.message.reply_text('No data returned from the API.')
    else:
        await update.message.reply_text('Please send a valid phone number.')

def main() -> None:
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_number))
    app.run_polling()

if __name__ == '__main__':
    main()

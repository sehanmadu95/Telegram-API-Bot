import http.client
import json
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler,filters,ContextTypes

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' and 'YOUR_API_KEY' with your actual values
TELEGRAM_BOT_TOKEN = '7687623596:AAFoD2vRcJZKi45gQ3J7tTsn0FlGBx2ldOY'
API_KEY = '817E35380DCfC17acD9321AB1BCbCe76f48013A221Cdd556160b131AE167DD59'

# Function to get detailed status based on ID
def get_detailed_status(request_id):
    conn = http.client.HTTPSConnection("gateway.seven.io")
    headers = {
        'Authorization': f'Basic {API_KEY}',
        'Content-Type': 'application/json'
    }
    conn.request("GET", f"/api/lookup/hlr?number={request_id}", headers=headers)
    res = conn.getresponse()
    data = res.read().decode("utf-8")
    return json.loads(data)




#Define the start command handler function
async def start(update:Update,context:ContextTypes.DEFAULT_TYPE)-> None :
    await update.message.reply_text("Welcome! Send a phone number to check its status.")



# Handler for receiving phone numbers and checking their status
async def check_number(update: Update, context:ContextTypes.DEFAULT_TYPE)->None:
    phone_number = update.message.text
    if phone_number.isdigit() and len(phone_number) >= 10:
        await update.message.reply_text(f'Checking status for phone number: {phone_number}')
        status_data = get_detailed_status(phone_number)
        print(status_data)
        if status_data:
            status = status_data.get('status', 'Unknown')
            status_message = status_data.get('status_message', 'Unknown')
            lookup_outcome = status_data.get('lookup_outcome', 'Unknown')
            lookup_outcome_message = status_data.get('lookup_outcome_message', 'Unknown')
            international_format_number = status_data.get('international_format_number', 'Unknown')
            international_formatted = status_data.get('international_formatted', 'Unknown')
            national_format_number = status_data.get('national_format_number', 'Unknown')
            country_code = status_data.get('country_code', 'Unknown')
            country_name = status_data.get('country_name', 'Unknown')
            country_prefix = status_data.get('country_prefix', 'Unknown')
            
            current_carrier = status_data.get('current_carrier', {})
            current_carrier_name = current_carrier.get('name', 'Unknown')
            current_carrier_network_code = current_carrier.get('network_code', 'Unknown')
            current_carrier_country = current_carrier.get('country', 'Unknown')
            current_carrier_network_type = current_carrier.get('network_type', 'Unknown')

            original_carrier = status_data.get('original_carrier', {})
            original_carrier_name = original_carrier.get('name', 'Unknown')
            original_carrier_network_code = original_carrier.get('network_code', 'Unknown')
            original_carrier_country = original_carrier.get('country', 'Unknown')
            original_carrier_network_type = original_carrier.get('network_type', 'Unknown')

            valid_number = status_data.get('valid_number', 'Unknown')
            reachable = status_data.get('reachable', 'Unknown')
            ported = status_data.get('ported', 'Unknown')
            roaming = status_data.get('roaming', 'Unknown')
            gsm_code = status_data.get('gsm_code', 'None')
            gsm_message = status_data.get('gsm_message', 'None')
            await update.message.reply_text(
                    #f"status: {status}\n"
                    f"status message: {status_message}\n"
                    #f"lookup outcome: {lookup_outcome}\n"
                    f"lookup outcome message: {lookup_outcome_message}\n"
                    #f"international_format_number: {international_format_number}\n"
                    f"international formatted: {international_formatted}\n"
                    f"national format number: {national_format_number}\n"
                    f"country code: {country_code}\n"
                    f"country name: {country_name}\n"
                    f"country prefix: {country_prefix}\n"
                    f"current carrier name: {current_carrier_name}\n"
                    f"current carrier network code: {current_carrier_network_code}\n"
                    f"current carrier country: {current_carrier_country}\n"
                    f"current carrier network type: {current_carrier_network_type}\n"
                    f"original carrier name: {original_carrier_name}\n"
                    f"original carrier network_code: {original_carrier_network_code}\n"
                    f"original carrier country: {original_carrier_country}\n"
                    f"original carrier network_type: {original_carrier_network_type}\n"
                    f"valid_number: {valid_number}\n"
                    f"reachable: {reachable}\n"
                    f"ported: {ported}\n"
                    f"roaming: {roaming}\n"
                    f"gsm_code: {gsm_code}\n"
                    f"gsm_message: {gsm_message}\n"
                    
                    
                )
        else:
            await update.message.reply_text('No data returned from the API.')
    else:
        await update.message.reply_text('Please send a valid phone number.')




def main()->None:
    app=ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start",start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,check_number))


    app.run_polling()

if __name__== '__main__':
   main()
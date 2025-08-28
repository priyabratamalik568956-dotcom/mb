import phonenumbers
from phonenumbers import geocoder, carrier
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Put your bot token here
TOKEN = "8310300164:AAFSW7jiGHBiEEqHrQ0GTQuYOP-gbaLaTQc"

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Send me a phone number with country code, and I will tell you its details. "
        "Example: +14155552671"
    )

def get_number_details(update: Update, context: CallbackContext):
    text = update.message.text.strip()

    try:
        number = phonenumbers.parse(text, None)  # None means parse with country code included
        if not phonenumbers.is_valid_number(number):
            update.message.reply_text("That doesn't seem to be a valid phone number.")
            return

        country = geocoder.description_for_number(number, "en")
        service_provider = carrier.name_for_number(number, "en")
        possible = phonenumbers.is_possible_number(number)
        
        details = f"📞 Number: {text}\n"
        details += f"🌍 Country: {country or 'Unknown'}\n"
        details += f"📡 Carrier: {service_provider or 'Unknown'}\n"
        details += f"✅ Valid Number: {'Yes' if phonenumbers.is_valid_number(number) else 'No'}\n"
        details += f"⚠ Possible Number: {'Yes' if possible else 'No'}"

        update.message.reply_text(details)

    except phonenumbers.NumberParseException:
        update.message.reply_text("Please send a valid phone number, including the country code (e.g., +14155552671).")

def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_number_details))

    updater.start_polling()
    updater.idle()

if _name_ == "_main_":
    main()
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import random
import asyncio

# Hardcoded jokes
JOKES = [
    "Why don't scientists trust atoms? Because they make up everything!",
    "Why did the scarecrow win an award? Because he was outstanding in his field!",
    "Why don’t skeletons fight each other? They don’t have the guts.",
]

# Trivia questions
TRIVIA_QUESTIONS = [
    {"question": "What is the capital of France?", "answer": "paris"},
    {"question": "What is 5 + 7?", "answer": "12"},
    {"question": "What color is the sky on a clear day?", "answer": "blue"},
]

# Command Handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the user sends the /start command."""
    await update.message.reply_text("Welcome! Use /help to see what I can do.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Provide a list of available commands."""
    await update.message.reply_text("""
I can help with the following:
/start - Start the bot
/help - Show this help message
/joke - Get a random joke
/calculate <expression> - Perform a calculation (e.g., /calculate 5+7)
/trivia - Start a trivia game
/wordcount <text> - Count the words in a message
/remind <time_in_seconds> <message> - Set a reminder
    """)

async def joke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a random joke."""
    joke = random.choice(JOKES)
    await update.message.reply_text(joke)

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Perform a calculation from the user input."""
    if not context.args:
        await update.message.reply_text("Please provide an expression to calculate. Example: /calculate 5+7")
        return

    expression = ''.join(context.args)
    try:
        # Evaluate the math expression safely
        result = eval(expression)
        await update.message.reply_text(f"The result of {expression} is {result}")
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def trivia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start a trivia game."""
    question = random.choice(TRIVIA_QUESTIONS)
    context.user_data["trivia_answer"] = question["answer"]  # Save the answer for validation

    await update.message.reply_text(f"Trivia Time! {question['question']}")
    await update.message.reply_text("Reply with your answer.")

async def wordcount(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count words in the provided text."""
    if not context.args:
        await update.message.reply_text("Please provide some text. Example: /wordcount This is a test")
        return

    text = ' '.join(context.args)
    word_count = len(text.split())
    await update.message.reply_text(f"Your message contains {word_count} words.")

async def remind(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Set a reminder for the user."""
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /remind <time_in_seconds> <message>")
        return

    try:
        time = int(context.args[0])
        message = ' '.join(context.args[1:])
        await update.message.reply_text(f"Reminder set for {time} seconds. I will remind you soon!")

        await asyncio.sleep(time)
        await update.message.reply_text(f"⏰ Reminder: {message}")
    except ValueError:
        await update.message.reply_text("Time must be an integer (seconds).")
    except Exception as e:
        await update.message.reply_text(f"Error setting reminder: {e}")

# Message handler to validate trivia answers
async def trivia_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Validate the user's trivia answer."""
    correct_answer = context.user_data.get("trivia_answer")
    if correct_answer:
        user_answer = update.message.text.lower()
        if user_answer == correct_answer:
            await update.message.reply_text("Correct! 🎉 Well done!")
        else:
            await update.message.reply_text(f"Oops, the correct answer was {correct_answer}. Try again!")
        context.user_data["trivia_answer"] = None  # Reset trivia answer
    else:
        await update.message.reply_text("No trivia question is active. Start a new one with /trivia.")

# Main function to run the bot
def main():
    TOKEN = "7794731996:AAEIvSnQbRjbOcCCJ_uwg6w-aSEv5uIrlT8"  # Replace with your bot's token
    app = ApplicationBuilder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("joke", joke))
    app.add_handler(CommandHandler("calculate", calculate))
    app.add_handler(CommandHandler("trivia", trivia))
    app.add_handler(CommandHandler("wordcount", wordcount))
    app.add_handler(CommandHandler("remind", remind))

    # Register message handler for trivia responses
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, trivia_response))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()

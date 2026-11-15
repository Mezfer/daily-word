import os
from telegram import (Update, InlineKeyboardButton, InlineKeyboardMarkup,
                      WebAppInfo, LabeledPrice)
from telegram.ext import (Application, CommandHandler, PreCheckoutQueryHandler,
                          MessageHandler, filters, ContextTypes)

BOT_TOKEN = os.environ["BOT_TOKEN"]            # من BotFather
WEBAPP_URL = os.environ["WEBAPP_URL"]          # رابط GitHub Pages (HTTPS)

SHOP = {
    "hints5":  ("💡 5 Hints",        "Pack of 5 hints",                 25),
    "hints20": ("💡 20 Hints",       "Pack of 20 hints (best value)",   75),
    "streak":  ("🛡️ Streak Saver",  "Restore your lost streak",        50),
}


async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("🎮 Play now", web_app=WebAppInfo(url=WEBAPP_URL))]])
    await update.message.reply_text(
        "👋 Welcome to *Daily Word*!\n\nGuess the 5-letter word in 6 tries. New word every day.\n"
        "Share your result and challenge your friends! 🔥",
        reply_markup=kb, parse_mode="Markdown")


async def shop(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    for key, (title, desc, stars) in SHOP.items():
        await ctx.bot.send_invoice(
            chat_id=update.effective_chat.id,
            title=title, description=desc, payload=key,
            provider_token="",             # فارغ دائماً مع Telegram Stars
            currency="XTR",
            prices=[LabeledPrice(title, stars)],
        )


async def precheckout(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)


async def paid(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    p = update.message.successful_payment
    # TODO: خزّن الشراء في قاعدة بيانات (Supabase) ليقرأه الـ Mini App لاحقاً
    await update.message.reply_text(f"✅ Thank you! You bought: {p.invoice_payload}. Open the game to use it.")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("shop", shop))
    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, paid))
    app.run_polling()


if __name__ == "__main__":
    main()

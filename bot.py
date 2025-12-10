elif file_type == "video" and file_id:
                        context.bot.send_video(chat_id=update.effective_chat.id, video=file_id)
                    elif file_type == "audio" and file_id:
                        context.bot.send_audio(chat_id=update.effective_chat.id, audio=file_id)
                except Exception as e:
                    update.message.reply_text(f"⚠️ خطا در ارسال فایل: {e}")

        elif mode == "request_book":
            if REQUESTS_CHAT_ID:
                context.bot.send_message(chat_id=REQUESTS_CHAT_ID,
                                         text=f"📥 درخواست کتاب جدید:\n\n{update.message.text}\n\nاز طرف کاربر: {update.effective_user.first_name}")
                update.message.reply_text("✅ درخواست شما ثبت شد و برای مدیر ارسال گردید.")
            else:
                update.message.reply_text("⚠️ گروه درخواست‌ها تنظیم نشده است.")

def collect_messages(update: Update, context: CallbackContext):
    if update.message.chat.type in ["group", "supergroup"]:
        msg = update.message
        chat_id = msg.chat.id
        chat_title = msg.chat.title or ""
        message_id = msg.message_id
        date = msg.date.timestamp() if msg.date else 0
        text = msg.text or ""
        caption = msg.caption or ""

        file_type, file_id = "", ""
        if msg.document:
            file_type = "document"
            file_id = msg.document.file_id
        elif msg.photo:
            file_type = "photo"
            file_id = msg.photo[-1].file_id
        elif msg.video:
            file_type = "video"
            file_id = msg.video.file_id
        elif msg.audio:
            file_type = "audio"
            file_id = msg.audio.file_id

        save_record(chat_id, chat_title, message_id, date, text, caption, file_type, file_id)

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN تنظیم نشده. در محیط اجرای سرویس مقدار BOT_TOKEN را تعریف کن.")

    init_db()
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & (~Filters.command), handle_keyboard))
    dp.add_handler(MessageHandler(Filters.all & (~Filters.command), collect_messages))

    updater.start_polling()
    updater.idle()

if name == "main":
    main()

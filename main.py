import os
import ptbot
from dotenv import load_dotenv
from pytimeparse import parse


def render_progressbar(
    total,
    iteration,
    prefix='',
    suffix='',
    length=30,
    fill='█',
    zfill='░'
):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def main():
    load_dotenv()

    tg_token = os.getenv("TG_TOKEN")
    bot = ptbot.Bot(tg_token)

    def notify(chat_id):
        bot.send_message(chat_id, "Время вышло!")

    def notify_progress(secs_left, chat_id, message_id, total):
        progress = render_progressbar(total, total - secs_left)

        bot.update_message(
                    chat_id,
                    message_id,
                    "Осталось секунд {}\n{}".format(secs_left, progress)
        )

    def echo(chat_id, text):
        seconds = parse(text)

        message_id = bot.send_message(chat_id, "Запускаю таймер ...")

        bot.create_countdown(
            seconds,
            notify_progress,
            chat_id=chat_id,
            message_id=message_id,
            total=seconds,
        )

        bot.create_timer(seconds, notify, chat_id=chat_id)

    bot.reply_on_message(echo)
    bot.run_bot()


if __name__ == "__main__":
    main()

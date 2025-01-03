import os
import asyncio
import logging
from telegram import Bot, constants
from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

httplogger = logging.getLogger("httpx")
httplogger.level = logging.WARNING

telegramtoken = os.environ.get('API_KEY')
tgBotPollPeriodSeconds = float(os.environ.get('BOT_POLL_PERIOD_SECONDS'))
huggingfacetoken = os.environ.get('ACCESS_TOKEN')
huggingfacemodel = os.environ.get('MODEL')

async def main():
    agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=HfApiModel(model_id=huggingfacemodel, token=huggingfacetoken))
    bot = Bot(token=telegramtoken)
    offset = 0
    print("bot run!")

    while True:
        try:
            updates = await bot.get_updates(offset=offset, timeout=tgBotPollPeriodSeconds)

            for update in updates:
                if update.message and update.message.text:
                    offset = update.update_id + 1
                    await bot.send_chat_action(chat_id=update.message.chat.id , action = constants.ChatAction.TYPING)
                    result = agent.run(update.message.text)
                    await bot.send_message(chat_id=update.message.chat.id, text=result, reply_to_message_id=update.message.id)

            await asyncio.sleep(tgBotPollPeriodSeconds)

        except Exception as e:
            print(e)

if __name__ == "__main__":
    asyncio.run(main())
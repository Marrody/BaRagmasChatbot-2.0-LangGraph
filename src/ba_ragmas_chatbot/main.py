import sys
import warnings
from dotenv import load_dotenv
from telegram.error import NetworkError


from ba_ragmas_chatbot.chatbot import TelegramBot
from ba_ragmas_chatbot import logger_config

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")


def run():
    """Starts the Telegram Bot with LangGraph backend."""
    load_dotenv()
    logger = None
    try:

        logger = logger_config.get_logger("main")
        logger.info("🚀 Starting BA_RAGMAS Chatbot (LangGraph Edition)...")
        telegram_bot = TelegramBot()
        print("🤖 Bot is starting... Press Ctrl+C to stop.")
        telegram_bot.start_bot()
        logger.info("🛑 Telegram bot stopped.")

    except NetworkError:
        print("❌ No internet connection. Please connect to a network and restart.")
        if logger:
            logger.error("NetworkError: No internet connection.")

    except KeyboardInterrupt:
        print("\n👋 Bot stopped by user.")

    except Exception as e:
        print(f"❌ Critical Error: {e}")
        if logger:
            logger.exception(f"Critical Error in main: {e}")

    finally:
        logger_config.shutdown()


if __name__ == "__main__":
    run()

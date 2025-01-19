import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from dotenv import load_dotenv
from bot.conversations import analysis_conversation

# 환경 변수 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """에러 핸들러"""
    logger.error("Exception while handling an update:", exc_info=context.error)

def main():
    """봇 실행"""
    # 토큰 확인
    token = os.getenv('TELEGRAM_TOKEN')
    if not token:
        raise ValueError("TELEGRAM_TOKEN이 설정되지 않았습니다.")
    
    # 봇 생성
    application = Application.builder().token(token).build()
    
    # 대화 핸들러 등록
    application.add_handler(analysis_conversation)
    
    # 에러 핸들러 등록
    application.add_error_handler(error_handler)
    
    # 환경 변수에 따라 실행 모드 결정
    if os.getenv('RENDER') == 'true':
        # Render 배포 환경
        port = int(os.getenv('PORT', 3000))
        
        # 웹훅 URL 설정
        webhook_url = os.getenv('WEBHOOK_URL')
        if not webhook_url:
            webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}.onrender.com"
        
        # 웹훅 모드로 실행
        application.run_webhook(
            listen="0.0.0.0",
            port=port,
            webhook_url=webhook_url,
            allowed_updates=Update.ALL_TYPES
        )
        logger.info(f"봇이 웹훅 모드로 시작되었습니다. (포트: {port})")
    else:
        # 로컬 개발 환경
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("봇이 폴링 모드로 시작되었습니다.")

if __name__ == '__main__':
    main()

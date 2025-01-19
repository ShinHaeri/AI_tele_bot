"""
대화 흐름 관리 모듈

이 모듈은 텔레그램 봇의 대화 흐름을 관리합니다.
사용자와의 상호작용을 단계별로 처리하고, 각 단계에서 적절한 응답을 제공합니다.
"""

import asyncio
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    filters
)
from bot.messages import ElonStyleMessageFormatter as Elon
from services.langchain_service import LangChainService
from database import init_db, save_analysis

# 데이터베이스 초기화
init_db()

# AI 분석 서비스 인스턴스
langchain_service = LangChainService()

# 대화 상태 정의
(WAITING_START,
 CONTENT_CATEGORY,  # 콘텐츠 카테고리 선택
 CONTENT_TOPIC,    # 콘텐츠 주제 입력
 TARGET_AGE,       # 타겟 연령대 설정
 TARGET_INTEREST,  # 타겟 관심사 설정
 PLATFORM,         # 플랫폼 선택
 HOOK_POINT,       # 후킹포인트 선택
 ANALYZING,        # AI 분석 중
 HELP_MENU) = range(9)

# 키보드 메뉴 정의
# 콘텐츠 카테고리 선택 옵션
CATEGORY_KEYBOARD = [
    ['🎭 엔터테인먼트/예능', '🎓 교육/정보'],
    ['💄 뷰티/패션', '✈️ 여행/레저'],
    ['🍳 음식/요리', '🎮 게임/스포츠'],
    ['🎵 음악/댄스', '📹 일상/브이로그'],
    ['🐾 반려동물', '💻 테크/IT'],
    ['💰 재테크/투자', '💪 건강/운동']
]

# 타겟 연령대 선택 옵션
AGE_KEYBOARD = [
    ['👶 10대', '👩 20대'],
    ['👨 30대', '👴 40대'],
    ['👵 50대 이상']
]

# 타겟 관심사 선택 옵션
INTEREST_KEYBOARD = [
    ['🎯 트렌드/유행 정보', '📚 실용적/생활 정보'],
    ['📈 자기계발/성장', '🎨 취미/여가 활동'],
    ['🛍️ 쇼핑/소비', '🧘 건강/웰빙'],
    ['🎭 문화/예술', '👥 소셜/커뮤니티']
]

# 플랫폼 선택 옵션
PLATFORM_KEYBOARD = [
    ['📱 TikTok', '📸 Instagram Reels'],
    ['🎥 YouTube Shorts', '📺 기타']
]

# 후킹포인트 선택 옵션
HOOK_KEYBOARD = [
    ['😱 충격적인 사실/반전', '🤔 궁금증 유발'],
    ['💝 공감되는 상황', '💡 유용한 정보/팁'],
    ['🎭 재미있는 연출', '👀 시선 끄는 액션'],
    ['🌟 트렌디한 밈/챌린지', '💖 감동/힐링']
]

# 도움말 메뉴 옵션
HELP_KEYBOARD = [
    ['📚 도움말 1'],
    ['💡 도움말 2'],
    ['🤝 도움말 3'],
    ['📊 도움말 4'],
    ['❓ 도움말 5']
]

# 시작 메뉴 옵션
START_KEYBOARD = [
    ['✨ 시작하기'],
    ['📚 가이드']
]

async def start_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """대화 시작 핸들러"""
    try:
        await update.message.reply_photo(
            photo=Elon.WELCOME_IMG_URL,
            caption=Elon.WELCOME_MESSAGE,
            reply_markup=ReplyKeyboardMarkup(START_KEYBOARD, resize_keyboard=True)
        )
    except Exception as e:
        print(f"이미지 전송 실패: {e}")
        await update.message.reply_text(
            Elon.WELCOME_MESSAGE,
            reply_markup=ReplyKeyboardMarkup(START_KEYBOARD, resize_keyboard=True)
        )
    return WAITING_START

async def handle_start_response(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """시작 응답 처리 핸들러"""
    text = update.message.text
    
    if text == '✨ 시작하기':
        reply_markup = ReplyKeyboardMarkup(CATEGORY_KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(
            Elon.QUESTIONS['content_category'],
            reply_markup=reply_markup
        )
        return CONTENT_CATEGORY
    elif text == '📚 가이드':
        keyboard = [[
            InlineKeyboardButton(
                "✨✨✨✨✨✨✨✨✨\n✨✨가이드 보기✨✨",
                url="http://starlenz.notion.site"
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✨✨가이드✨✨",
            reply_markup=reply_markup
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text("안내 메세지 👀")
        return WAITING_START

async def handle_content_category(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """콘텐츠 카테고리 선택 처리 핸들러"""
    context.user_data['content_category'] = update.message.text
    await update.message.reply_text(
        Elon.QUESTIONS['content_topic'],
        reply_markup=ReplyKeyboardRemove()
    )
    return CONTENT_TOPIC

async def handle_content_topic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """콘텐츠 주제 입력 처리 핸들러"""
    context.user_data['content_topic'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(AGE_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['target_age'],
        reply_markup=reply_markup
    )
    return TARGET_AGE

async def handle_target_age(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """타겟 연령대 선택 처리 핸들러"""
    context.user_data['target_age'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(INTEREST_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['target_interest'],
        reply_markup=reply_markup
    )
    return TARGET_INTEREST

async def handle_target_interest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """타겟 관심사 선택 처리 핸들러"""
    context.user_data['target_interest'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(PLATFORM_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['platform'],
        reply_markup=reply_markup
    )
    return PLATFORM

async def handle_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """플랫폼 선택 처리 핸들러"""
    context.user_data['platform'] = update.message.text
    reply_markup = ReplyKeyboardMarkup(HOOK_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        Elon.QUESTIONS['hook_point'],
        reply_markup=reply_markup
    )
    return HOOK_POINT

async def handle_hook_point(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """후킹포인트 선택 처리 핸들러"""
    context.user_data['hook_point'] = update.message.text
    
    try:
        # 분석 시작 메시지 전송
        await update.message.reply_text(
            Elon.ANALYSIS_START,
            reply_markup=ReplyKeyboardRemove()
        )
        
        # AI 분석 수행 및 결과 대기
        analysis_result = await langchain_service.generate_content_ideas(context.user_data)
        
        if not analysis_result:
            await update.message.reply_text(
                "⚠️ 분석 중 오류가 발생했습니다. 다시 시도해주세요."
            )
            return ConversationHandler.END
            
        # 분석 결과 저장
        try:
            save_analysis(
                telegram_id=update.effective_user.id,
                input_data=context.user_data,
                result=analysis_result
            )
        except Exception as e:
            print(f"데이터베이스 저장 오류: {e}")
        
        # 분석 결과 구조 보존
        formatted_result = {
            'ideas': analysis_result.get('ideas', ''),
            'production_strategy': analysis_result.get('production_strategy', []),
            'engagement_strategy': analysis_result.get('engagement_strategy', []),
            'growth_strategy': analysis_result.get('growth_strategy', []),
            'trending_hashtags': analysis_result.get('trending_hashtags', [])
        }
        
        # 디버깅 로그
        print("\n=== Analysis Result Structure ===")
        for key, value in formatted_result.items():
            print(f"\n{key}:")
            if isinstance(value, list):
                for item in value:
                    print(f"  {item}")
            else:
                print(f"  {value}")
        
        context.user_data['analysis_result'] = formatted_result
        
        # 분석 결과 메시지 전송
        formatted_message = Elon.format_analysis_result(formatted_result)
        await update.message.reply_text(formatted_message)
        
        # 분석 완료 후 인라인 키보드 생성
        keyboard = [
            [
                InlineKeyboardButton("📱 틱톡 크리에이티브 센터", url="https://ads.tiktok.com/business/creativecenter/inspiration/popular/hashtag/pc/en")
            ],
            [
                InlineKeyboardButton("🎬 아이디어 공유", url="https://t.me/share/url?url=https://t.me/shortform_script_bot&text=✨숏폼 콘텐츠 아이디어 어시스턴트✨"),
                InlineKeyboardButton("💡 피드백", url="tg://resolve?domain=shortform_feedback")
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "분석이 완료되었습니다!",
            reply_markup=reply_markup
        )
        
        return ConversationHandler.END
        
    except Exception as e:
        print(f"분석 중 오류 발생: {e}")
        await update.message.reply_text(
            "⚠️ 시스템 오류가 발생했습니다. 다시 시도해주세요."
        )
        return ConversationHandler.END

async def handle_analysis(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """분석 결과 처리 핸들러"""
    if 'analysis_result' not in context.user_data:
        await update.message.reply_text(
            "❌ 분석 결과를 찾을 수 없습니다. 다시 시작해주세요."
        )
        return ConversationHandler.END
    
    await update.message.reply_text(
        Elon.format_analysis_result(context.user_data['analysis_result'])
    )
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """도움말 명령어 핸들러"""
    help_text = (
        "가이드:\n\n"
        "/start | 새로운 분석 시작\n"
        "/help | 도움말\n\n"
        "@starlenz_inc | 관리자 연결"
    )
    
    reply_markup = ReplyKeyboardMarkup(HELP_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(help_text, reply_markup=reply_markup)
    return HELP_MENU

async def handle_help_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """도움말 메뉴 처리 핸들러"""
    text = update.message.text
    
    # URL 매핑 정의
    urls = {
        'URL 연결 1...': 'http://starlenz.notion.site',
        'URL 연결 2': 'http://starlenz.notion.site',
        'URL 연결 3': 'http://starlenz.notion.site',
        'URL 연결 4': 'http://starlenz.notion.site'
    }
    
    if text in urls:
        keyboard = [[InlineKeyboardButton("✨ 바로가기 ✨", url=urls[text])]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "✨✨✨✨✨✨✨✨✨\n✨✨연결 메세지✨✨",
            reply_markup=reply_markup
        )
        return HELP_MENU
    
    reply_markup = ReplyKeyboardMarkup(HELP_KEYBOARD, resize_keyboard=True)
    await update.message.reply_text(
        "메뉴를 선택해주세요. /help",
        reply_markup=reply_markup
    )
    return HELP_MENU

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """취소 명령어 핸들러"""
    await update.message.reply_text(
        "🛑 분석이 취소되었습니다. 새로 시작하려면 /start 를 입력하세요.",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END

# 대화 핸들러 생성
analysis_conversation = ConversationHandler(
    entry_points=[
        CommandHandler("start", start_conversation),
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel)
    ],
    
    states={
        WAITING_START: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_start_response)],
        CONTENT_CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_content_category)],
        CONTENT_TOPIC: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_content_topic)],
        TARGET_AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_age)],
        TARGET_INTEREST: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_target_interest)],
        PLATFORM: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_platform)],
        HOOK_POINT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_hook_point)],
        ANALYZING: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_analysis)],
        HELP_MENU: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_help_menu)]
    },
    
    fallbacks=[
        CommandHandler("start", start_conversation), 
        CommandHandler("help", help_command),
        CommandHandler("cancel", cancel)
    ]
)

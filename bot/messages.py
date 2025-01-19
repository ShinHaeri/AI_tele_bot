"""
메시지 포맷팅 모듈

이 모듈은 텔레그램 봇의 모든 메시지 템플릿을 관리합니다.
봇의 성격과 목적에 맞게 메시지를 커스터마이징할 수 있습니다.

주요 구성:
1. 웰컴 메시지와 이미지
2. 질문 목록과 설명
3. 분석 결과 포맷팅

사용자 정의:
- 메시지 톤과 스타일
- 이모지 사용
- 설명 방식
"""

class ElonStyleMessageFormatter:
    """
    메시지 포맷팅 클래스
    
    봇과 사용자 간의 모든 상호작용에 사용되는 메시지를 정의합니다.
    메시지의 톤, 이모지 사용, 설명 방식 등을 일관되게 유지합니다.
    """
    
    # 웰컴 이미지 URL
    WELCOME_IMG_URL = "https://imagedelivery.net/csS3I11UbX4B6HoDdrP-iA/051ec1a7-9cff-4ad1-8c4b-9a55a0173700/public"
    
    # 웰컴 메시지
    WELCOME_MESSAGE = """
✨ 숏폼 콘텐츠 아이디어 어시스턴트

📍 이런 분들에게 추천해요:
🔹 트렌디한 콘텐츠 아이디어가 필요하신 분
🔹 새로운 콘텐츠 방향을 찾고 계신 분
🔹 인기 있는 콘텐츠 주제를 알고 싶으신 분

📍 진행 방법:
1️⃣ 콘텐츠 카테고리 선택
2️⃣ 원하는 콘텐츠 주제 입력
3️⃣ 타겟층 설정
4️⃣ 플랫폼 선택
5️⃣ AI 아이디어 생성

📍 명령어:
🔹 /start : 새로운 아이디어 찾기
🔹 /cancel : 취소
🔹 /help : 도움말

📍 소요시간: 2-3분

✨ "시작하기"를 선택해주세요!"""

    # 분석 시작 메시지
    ANALYSIS_START = """
⚙️ 트렌드와 인기 콘텐츠를 분석중입니다...

🤖 AI가 맞춤형 아이디어를 생성합니다.

⏱️ 잠시만 기다려주세요.
"""

    # 질문 목록
    QUESTIONS = {
        # 콘텐츠 카테고리 선택
        'content_category': """
🎯 콘텐츠 카테고리를 선택해주세요:

• 엔터테인먼트/예능
• 교육/정보
• 뷰티/패션
• 여행/레저
• 음식/요리
• 게임/스포츠
• 음악/댄스
• 일상/브이로그
• 반려동물
• 테크/IT
• 재테크/투자
• 건강/운동
""",

        # 콘텐츠 주제 입력
        'content_topic': """
✍️ 만들고 싶은 콘텐츠 주제나 키워드를 자유롭게 입력해주세요.

💡 구체적으로 설명해주실수록 더 좋은 아이디어를 제안해드릴 수 있습니다!

예시:
• "20대를 위한 재테크 꿀팁"
• "반려견과 함께하는 일상"
• "직장인 점심 메뉴 추천"
• "홈트레이닝 루틴"
• "해외여행 꿀팁"
""",
        
        # 연령대 선택
        'target_age': """
👥 주요 타겟층의 연령대를 선택해주세요:

• 10대
• 20대
• 30대
• 40대
• 50대 이상
""",

        # 관심사 선택
        'target_interest': """
🎯 주요 타겟층의 관심사를 선택해주세요:

• 트렌드/유행 정보
• 실용적/생활 정보
• 자기계발/성장
• 취미/여가 활동
• 쇼핑/소비
• 건강/웰빙
• 문화/예술
• 소셜/커뮤니티
""",
        
        # 플랫폼 선택
        'platform': """
📱 주로 어떤 플랫폼에서 활동하시나요?

• TikTok
• Instagram Reels
• YouTube Shorts
• 기타 (직접 입력)

각 플랫폼별 최적화된 아이디어를 제안해드립니다.
""",
        
        # 후킹포인트 선택
        'hook_point': """
🎯 어떤 후킹포인트를 활용하고 싶으신가요?

• 충격적인 사실/반전
• 궁금증 유발
• 공감되는 상황
• 유용한 정보/팁
• 재미있는 연출
• 시선 끄는 액션
• 트렌디한 밈/챌린지
• 감동/힐링
"""
    }

    @staticmethod
    def format_analysis_result(result: dict) -> str:
        """
        콘텐츠 아이디어 생성 결과를 포맷팅하는 메서드
        """
        if not result or not isinstance(result, dict):
            return "분석 중 오류가 발생했습니다."

        # 섹션별 데이터 추출
        ideas = result.get('ideas', '아이디어 생성 중...')
        production_strategy = result.get('production_strategy', [])
        engagement_strategy = result.get('engagement_strategy', [])
        growth_strategy = result.get('growth_strategy', [])
        hashtags = result.get('trending_hashtags', [])

        # 메시지 구성
        message_parts = ["✨ 콘텐츠 아이디어가 준비되었습니다!", ""]

        # 아이디어 섹션 포맷팅
        message_parts.extend(["💡 추천 콘텐츠 아이디어:"])
        for line in ideas.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('# '):
                    current_subsection = line[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif line.startswith('- '):
                    message_parts.append(f"• {line[2:].strip()}")
                else:
                    message_parts.append(f"  {line}")

        # 제작 전략 섹션 포맷팅
        if production_strategy:
            message_parts.extend(["", "🎬 콘텐츠 제작 전략:"])
            for item in production_strategy:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 참여 유도 전략 섹션 포맷팅
        if engagement_strategy:
            message_parts.extend(["", "🎯 참여 유도 전략:"])
            for item in engagement_strategy:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 성장 전략 섹션 포맷팅
        if growth_strategy:
            message_parts.extend(["", "📈 성장 전략:"])
            for item in growth_strategy:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 트렌딩 해시태그 섹션 포맷팅
        if hashtags:
            message_parts.extend([
                "",
                "🔥 틱톡 트렌딩 해시태그 TOP 10:",
                "현재 틱톡에서 인기 있는 해시태그입니다:"
            ])
            for i, tag in enumerate(hashtags, 1):
                message_parts.append(f"{i}. #{tag}")

        return "\n".join(message_parts)

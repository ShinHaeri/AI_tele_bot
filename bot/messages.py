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
    
    # 웰컴 이미지 URL - 자신의 브랜드에 맞는 이미지로 변경하세요
    WELCOME_IMG_URL = "https://imagedelivery.net/csS3I11UbX4B6HoDdrP-iA/051ec1a7-9cff-4ad1-8c4b-9a55a0173700/public"
    
    # 웰컴 메시지 - 숏폼 스크립트 작성 도우미 소개
    WELCOME_MESSAGE = """
✨ 숏폼 스크립트 작성 도우미

📍 이런 분들에게 추천해요:
🔹 숏폼 콘텐츠를 시작하고 싶으신 분
🔹 매력적인 스크립트가 필요하신 분
🔹 트렌드에 맞는 콘텐츠를 만들고 싶으신 분

📍 진행 방법:
1️⃣ 콘텐츠 유형 선택
2️⃣ 타겟/플랫폼 설정
3️⃣ 트렌드/벤치마킹 분석
4️⃣ 콘텐츠 세부 요소 설정
5️⃣ AI 스크립트 생성

📍 명령어:
🔹 /start : 새로운 스크립트 작성
🔹 /cancel : 작성 취소
🔹 /help : 도움말

📍 소요시간: 3-5분

✨ "시작하기"를 선택해주세요!"""

    # 분석 시작 메시지 - 사용자에게 진행 상황을 알려주는 메시지입니다
    ANALYSIS_START = """
⚙️ 입력된 정보를 분석중입니다...

🤖 AI가 분석을 시작합니다.

⏱️ 잠시만 기다려주세요.
"""

    # 질문 목록 - 숏폼 스크립트 작성을 위한 질문들
    QUESTIONS = {
        # 콘텐츠 유형 선택
        'content_type': """
🎯 어떤 유형의 콘텐츠를 만드실 건가요?

위 콘텐츠 유형 중에서 선택해주세요.
""",
        
        # 타겟 오디언스 선택
        'target_audience': """
👥 주요 시청자층은 누구인가요?

위 타겟 오디언스 중에서 선택해주세요.
""",
        
        # 플랫폼 선택
        'platform': """
📱 어떤 플랫폼에 업로드 하실 건가요?

위 플랫폼 중에서 선택해주세요.
""",
        
        # 트렌드 분석
        'trend_analysis': """
📈 현재 트렌드는 무엇인가요?

TIP: 해시태그, 음악, 챌린지 등을 입력해주세요.
예시: #일상 #OOTD #챌린지
""",
        
        # 벤치마킹 계정
        'benchmark': """
🔍 참고하고 싶은 계정이 있나요?

TIP: 계정명을 입력해주세요.
예시: @username, 여러 계정 입력 가능
""",
        
        # 벤치마킹 포인트
        'benchmark_point': """
💡 해당 계정의 어떤 점이 좋았나요?

TIP: 구체적으로 설명해주세요.
예시: 편집 스타일, 자막 활용, 음악 선정 등
""",
        
        # 콘텐츠 형식
        'content_format': """
📝 어떤 형식으로 만드실 건가요?

위 콘텐츠 형식 중에서 선택해주세요.
""",
        
        # 콘텐츠 주제
        'content_topic': """
📌 구체적인 주제는 무엇인가요?

TIP: 명확하게 설명해주세요.
예시: 일상 브이로그, 메이크업 튜토리얼
""",
        
        # 특별 요소
        'special_element': """
✨ 특별히 넣고 싶은 요소가 있나요?

TIP: 유머, 감동, 정보성 등을 입력해주세요.
예시: 반전 요소, 공감대 형성
""",
        
        # 영상 길이
        'video_length': """
⏱️ 영상 길이는 어떻게 할까요?

위 옵션 중에서 선택해주세요.
""",
        
        # 비주얼 요소
        'visual_element': """
🎨 어떤 비주얼 요소를 사용할까요?

위 옵션 중에서 선택해주세요.
""",
        
        # 스토리라인
        'storyline': """
📖 스토리라인을 설명해주세요.

TIP: 시작-중간-끝 구성을 설명해주세요.
예시: 문제 상황 - 해결 과정 - 결과
"""
    }

    @staticmethod
    def format_analysis_result(result: dict) -> str:
        """
        스크립트 생성 결과를 포맷팅하는 메서드
        
        AI가 생성한 스크립트와 제안사항을 사용자가 읽기 쉬운 형태로 변환합니다.
        
        포맷팅 규칙:
        1. 섹션 구분을 위한 이모지 사용
        2. 스크립트는 시간대별로 구분
        3. 제안사항은 글머리 기호로 강조
        
        Args:
            result (dict): AI 분석 결과 데이터
                - script: 완성된 스크립트
                - hooks: 후킹 문구 제안
                - visual_suggestions: 비주얼 요소 제안
                - trending_elements: 트렌드 요소
                - optimization_tips: 최적화 팁
                
        Returns:
            str: 포맷팅된 스크립트와 제안사항
        """
        if not result or not isinstance(result, dict):
            return "분석 중 오류가 발생했습니다."

        # 섹션별 데이터 추출
        script = result.get('script', '스크립트 생성 중...')
        hooks = result.get('hooks', [])
        visual_suggestions = result.get('visual_suggestions', [])
        trending_elements = result.get('trending_elements', [])
        optimization_tips = result.get('optimization_tips', [])

        # 메시지 구성
        message_parts = ["✨ 스크립트가 완성되었습니다!", ""]

        # 스크립트 섹션 포맷팅
        message_parts.extend(["📝 스크립트:"])
        for line in script.split('\n'):
            line = line.strip()
            if line:
                if line.startswith('[') and line.endswith(']'):  # 타임스탬프
                    message_parts.append(f"\n⏱️ {line}")
                elif line.startswith('# '):
                    current_subsection = line[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif line.startswith('- '):
                    message_parts.append(f"• {line[2:].strip()}")
                else:
                    message_parts.append(f"  {line}")

        # 후킹 문구 섹션 포맷팅
        if hooks:
            message_parts.extend(["", "🎯 후킹 문구 제안:"])
            for item in hooks:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 비주얼 요소 섹션 포맷팅
        if visual_suggestions:
            message_parts.extend(["", "🎨 비주얼 요소 제안:"])
            for item in visual_suggestions:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 트렌드 요소 섹션 포맷팅
        if trending_elements:
            message_parts.extend(["", "📈 트렌드 요소:"])
            for item in trending_elements:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        # 최적화 팁 섹션 포맷팅
        if optimization_tips:
            message_parts.extend(["", "💡 최적화 팁:"])
            for item in optimization_tips:
                if item.startswith('# '):
                    current_subsection = item[2:].strip()
                    if current_subsection.endswith(':'):
                        current_subsection = current_subsection[:-1].strip()
                    message_parts.append(f"\n📍 {current_subsection}")
                elif item.startswith('- '):
                    message_parts.append(f"• {item[2:].strip()}")

        return "\n".join(message_parts)

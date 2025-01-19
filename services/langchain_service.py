"""
LangChain 서비스 모듈

이 모듈은 Anthropic의 Claude AI를 사용하여 사용자 입력을 분석하고
체계적인 보고서를 생성하는 기능을 제공합니다.
"""

import os
import asyncio
from typing import Dict, Optional
import anthropic
from langchain.prompts import ChatPromptTemplate
import warnings

# SQLite 관련 경고 무시
warnings.filterwarnings('ignore', category=UserWarning, module='langchain')

# 틱톡 카테고리별 해시태그 매핑
TIKTOK_HASHTAGS = {
    "엔터테인먼트/예능": ["fyp", "viral", "funny", "comedy", "entertainment", "humor", "trending", "meme", "laugh", "fun"],
    "교육/정보": ["learnontiktok", "education", "facts", "knowledge", "study", "learning", "tips", "howto", "tutorial", "skills"],
    "뷰티/패션": ["beauty", "fashion", "makeup", "skincare", "style", "outfit", "cosmetics", "hairstyle", "fashionblogger", "beautytips"],
    "여행/레저": ["travel", "adventure", "explore", "wanderlust", "vacation", "trip", "tourism", "travelblogger", "nature", "destination"],
    "음식/요리": ["food", "cooking", "recipe", "foodie", "cook", "yummy", "delicious", "foodlover", "homemade", "chef"],
    "게임/스포츠": ["gaming", "sports", "game", "esports", "gamer", "athlete", "fitness", "workout", "training", "sport"],
    "음악/댄스": ["music", "dance", "song", "singer", "musician", "dancing", "choreography", "performance", "concert", "dancer"],
    "일상/브이로그": ["daily", "vlog", "lifestyle", "life", "dailylife", "routine", "dayinthelife", "vlogger", "reallife", "moment"],
    "반려동물": ["pet", "dog", "cat", "animal", "puppy", "kitten", "pets", "cute", "petsoftiktok", "animals"],
    "테크/IT": ["tech", "technology", "gadget", "innovation", "smartphone", "computer", "digital", "software", "coding", "programming"],
    "재테크/투자": ["finance", "money", "investment", "crypto", "stocks", "trading", "wealth", "financial", "business", "investing"],
    "건강/운동": ["health", "fitness", "workout", "gym", "exercise", "healthy", "training", "fit", "wellness", "motivation"]
}

class LangChainService:
    """LangChain 서비스 클래스"""
    def __init__(self):
        """서비스 초기화"""
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        self.client = anthropic.Client(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
        
        # 1단계: 콘텐츠 아이디어 생성
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 숏폼 콘텐츠 전문 크리에이터입니다.
            제공된 정보를 바탕으로 매력적인 숏폼 콘텐츠 아이디어를 제안해주세요.
            
            다음 형식을 정확히 따라주세요:
            
            # 트렌딩 콘텐츠 아이디어
            - [인기 있는 콘텐츠 아이디어 3-5개]
            - [각 아이디어별 핵심 포인트]
            
            # 니치 콘텐츠 아이디어
            - [차별화된 콘텐츠 아이디어 2-3개]
            - [각 아이디어의 독특한 가치]
            
            # 시리즈 콘텐츠 아이디어
            - [연속성 있는 콘텐츠 아이디어 2-3개]
            - [각 시리즈의 발전 방향]
            
            주의사항:
            1. 각 아이디어는 구체적이고 실현 가능해야 함
            2. 플랫폼 특성과 트렌드를 반영
            3. 타겟 시청자의 관심사에 부합
            4. 후킹포인트를 활용한 아이디어 제시
            5. 확장 가능성을 고려한 제안"""),
            
            ("human", """콘텐츠 카테고리: {content_category}
            콘텐츠 주제/키워드: {content_topic}
            타겟 연령대: {target_age}
            타겟 관심사: {target_interest}
            플랫폼: {platform}
            후킹포인트: {hook_point}""")
        ])
        
        # 2단계: 실행 전략 생성
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 숏폼 콘텐츠 전략 전문가입니다.

            1단계에서 제안된 아이디어를 바탕으로 실행 전략을 제시해주세요.

            다음 형식으로 응답해주세요:

            # 콘텐츠 제작 전략
            - 촬영 팁: [구도, 앵글, 조명 등]
            - 편집 포인트: [템포, 전환, 효과 등]
            - 사운드 활용: [BGM, 효과음 등]
            - 자막 전략: [폰트, 위치, 애니메이션 등]

            # 참여 유도 전략
            - 후킹 포인트: [시청자 관심 유도 방법]
            - 인터랙션: [댓글, 공유 유도 방법]
            - 해시태그: [검색 최적화 전략]
            - 업로드 타이밍: [최적 시간대]

            # 성장 전략
            - 시리즈화: [콘텐츠 확장 방안]
            - 크로스 프로모션: [협업 아이디어]
            - 트렌드 활용: [인기 요소 접목]
            - 커뮤니티: [팬층 형성 방안]

            주의사항:
            1. 각 섹션은 반드시 '# '으로 시작
            2. 모든 항목은 반드시 '- '으로 시작
            3. 빈 줄은 섹션 구분에만 사용
            4. 실제 트렌드와 성공 사례 기반의 구체적 제안"""),
            
            ("human", """아이디어: {ideas}""")
        ])

    def _get_trending_hashtags(self, category: str) -> list:
        """카테고리에 맞는 틱톡 트렌딩 해시태그 반환"""
        return TIKTOK_HASHTAGS.get(category, TIKTOK_HASHTAGS["엔터테인먼트/예능"])

    def _get_summary(self, data):
        """1단계: 기본 정보 정리 및 요약"""
        response = self.client.messages.create(
            model=self.model,
            system=self.summary_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": self.summary_prompt.messages[1].prompt.template.format(**data)}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    def _get_analysis(self, ideas):
        """2단계: 실행 전략 생성"""
        response = self.client.messages.create(
            model=self.model,
            system=self.analysis_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": f"아이디어: {ideas}"}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    async def debug_chain(self, data: Dict) -> None:
        """디버깅용 체인 실행"""
        try:
            summary_result = await asyncio.to_thread(self._get_summary, data)
            print("\n=== Summary Chain Result ===")
            print(f"Content: {summary_result}")
            
            analysis_result = await asyncio.to_thread(self._get_analysis, summary_result)
            print("\n=== Analysis Chain Result ===")
            print(f"Content: {analysis_result}")
            
        except Exception as e:
            print(f"\n=== Chain Debug Error ===")
            print(f"Error: {e}")
            print(f"Error Type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    def _parse_section_content(self, content: str) -> list:
        """섹션 내용을 리스트 형태로 파싱"""
        if not content:
            return []
        
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        result = []
        
        for line in lines:
            if line.startswith('- '):
                if ':' in line:
                    label, value = line[2:].split(':', 1)
                    result.append(f"# {label.strip()}")
                    if value.strip():
                        result.append(f"- {value.strip()}")
                else:
                    result.append(line)
            else:
                result.append(f"- {line.strip()}")
        
        result = [item.strip() for item in result if item.strip()]
        return result

    async def generate_content_ideas(self, data: Dict) -> Optional[Dict]:
        """숏폼 콘텐츠 아이디어 생성"""
        try:
            # 디버깅 실행
            await self.debug_chain(data)

            # 체인 실행
            print("\n=== Chain Execution ===")
            summary = await asyncio.to_thread(self._get_summary, data)
            analysis = await asyncio.to_thread(self._get_analysis, summary)
            
            # 틱톡 트렌딩 해시태그 가져오기
            trending_hashtags = self._get_trending_hashtags(data.get('content_category', ''))
            
            # 결과를 직접 구성
            content_result = {
                'ideas': summary,
                'production_strategy': [],
                'engagement_strategy': [],
                'growth_strategy': [],
                'trending_hashtags': trending_hashtags
            }
            
            # 섹션 매핑 정의
            section_mapping = {
                '콘텐츠 제작 전략': 'production_strategy',
                '참여 유도 전략': 'engagement_strategy',
                '성장 전략': 'growth_strategy'
            }
            
            # 분석 결과 파싱
            current_section = None
            current_content = []
            
            print("\n=== Parsing Analysis Result ===")
            
            for line in analysis.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('# '):
                    # 이전 섹션의 내용을 처리
                    if current_section and current_content:
                        parsed_content = self._parse_section_content('\n'.join(current_content))
                        if current_section in section_mapping:
                            mapped_section = section_mapping[current_section]
                            print(f"\nProcessing section: {current_section} -> {mapped_section}")
                            print(f"Parsed content: {parsed_content}")
                            content_result[mapped_section] = parsed_content
                    
                    # 새로운 섹션 시작
                    current_section = line[2:].strip()
                    print(f"\nNew section: {current_section}")
                    current_content = []
                else:
                    current_content.append(line)
                    print(f"Added content: {line}")
            
            # 마지막 섹션 처리
            if current_section and current_content:
                parsed_content = self._parse_section_content('\n'.join(current_content))
                if current_section in section_mapping:
                    mapped_section = section_mapping[current_section]
                    print(f"\nProcessing final section: {current_section} -> {mapped_section}")
                    print(f"Parsed content: {parsed_content}")
                    content_result[mapped_section] = parsed_content

            return content_result
            
        except Exception as e:
            print(f"분석 중 오류 발생: {e}")
            return None

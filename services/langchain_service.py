"""
LangChain 서비스 모듈

이 모듈은 Anthropic의 Claude AI를 사용하여 사용자 입력을 분석하고
체계적인 보고서를 생성하는 기능을 제공합니다.

주요 기능:
1. 사용자 입력 정보 정리 및 요약
2. 상세 분석 및 제안 생성
3. 결과 파싱 및 구조화

사용자 정의:
- 프롬프트 템플릿 수정
- 분석 섹션 구성 변경
- 결과 포맷 커스터마이징
"""

import os
import asyncio
from typing import Dict, Optional
import anthropic
from langchain.prompts import ChatPromptTemplate
import warnings

# SQLite 관련 경고 무시
warnings.filterwarnings('ignore', category=UserWarning, module='langchain')

class LangChainService:
    """
    LangChain 서비스 클래스
    
    이 클래스는 AI 분석 기능의 핵심 로직을 구현합니다.
    Anthropic의 Claude AI를 사용하여 두 단계로 분석을 수행합니다:
    1단계: 기본 정보 정리 및 요약
    2단계: 상세 분석 및 제안
    """
    def __init__(self):
        """
        서비스 초기화
        
        필요한 설정:
        1. ANTHROPIC_API_KEY 환경 변수
        2. Claude AI 모델 선택
        3. 프롬프트 템플릿 구성
        
        프롬프트 템플릿은 분석의 품질과 일관성을 결정하는 중요한 요소입니다.
        필요에 따라 템플릿을 수정하여 다른 용도로 활용할 수 있습니다.
        """
        # Anthropic API 키 확인
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")
        
        # Anthropic 클라이언트 설정
        self.client = anthropic.Client(api_key=self.api_key)
        self.model = "claude-3-haiku-20240307"
        
        # 1단계: 스크립트 생성
        self.summary_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 숏폼 콘텐츠 전문 작가입니다.
            제공된 정보를 바탕으로 매력적인 숏폼 스크립트를 작성해주세요.
            
            다음 형식을 정확히 따라주세요:
            
            # 오프닝
            [0:00-0:05]
            [시청자의 관심을 끄는 강력한 후킹 문구]
            
            # 메인 내용
            [0:05-0:45]
            [핵심 내용을 시간대별로 구성]
            [각 시간대별 구체적인 대사와 액션]
            
            # 클로징
            [0:45-1:00]
            [콜투액션과 마무리 멘트]
            
            주의사항:
            1. 시간대는 반드시 [시작-끝] 형식으로 표시
            2. 각 섹션은 반드시 '# '으로 시작
            3. 대사는 명확하고 간결하게
            4. 시청자의 관심을 끌 수 있는 요소 포함
            5. 플랫폼 특성에 맞는 톤앤매너 사용"""),
            
            ("human", """콘텐츠 유형: {content_type}
            타겟: {target_audience}
            플랫폼: {platform}
            트렌드: {trend_analysis}
            벤치마크: {benchmark}
            벤치마크 포인트: {benchmark_point}
            콘텐츠 형식: {content_format}
            주제: {content_topic}
            특별 요소: {special_element}
            영상 길이: {video_length}
            비주얼: {visual_element}
            스토리라인: {storyline}""")
        ])
        
        # 2단계: 제안사항 생성
        self.analysis_prompt = ChatPromptTemplate.from_messages([
            ("system", """당신은 숏폼 콘텐츠 전문 컨설턴트입니다.

            1단계에서 작성된 스크립트를 바탕으로 개선점과 제안사항을 제시해주세요.

            다음 형식으로 응답해주세요:

            # 후킹 문구 제안
            - [대안 1]: 더 강력한 후킹 문구
            - [대안 2]: 다른 접근 방식의 후킹 문구
            - [대안 3]: 트렌드를 활용한 후킹 문구

            # 비주얼 요소 제안
            - 화면 구성: [레이아웃과 구도]
            - 자막 활용: [효과적인 자막 배치]
            - 전환 효과: [추천 전환 효과]
            - 색감: [추천 색상 팔레트]

            # 트렌드 요소
            - 해시태그: [추천 해시태그]
            - 음악: [추천 배경음악]
            - 효과음: [추천 효과음]
            - 필터: [추천 필터/효과]

            # 최적화 팁
            - 타이밍: [시간 배분 조정]
            - 구성: [흐름 개선]
            - 강조점: [핵심 포인트]
            - 참고: [유사 콘텐츠 추천]

            주의사항:
            1. 각 섹션은 반드시 '# '으로 시작
            2. 모든 항목은 반드시 '- '으로 시작
            3. 빈 줄은 섹션 구분에만 사용
            4. 실제 트렌드와 성공 사례를 반영한 구체적인 제안"""),
            
            ("human", """스크립트: {script}""")
        ])

    def _get_summary(self, data):
        """
        1단계: 기본 정보 정리 및 요약
        
        입력된 데이터를 바탕으로 구조화된 요약을 생성합니다.
        
        Args:
            data (Dict): 사용자 입력 데이터
                - idea: 아이디어 설명
                - category: 서비스 분야
                - approach: 접근 방식
                - target: 목표 고객
                - problem: 해결할 문제
                - solution: 해결 방안
                - implementation: 구현 방식
                - goals: 목표
                - needs: 필요 사항
        
        Returns:
            str: 구조화된 요약 텍스트
        """
        response = self.client.messages.create(
            model=self.model,
            system=self.summary_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": self.summary_prompt.messages[1].prompt.template.format(**data)}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    def _get_analysis(self, script):
        """
        2단계: 제안사항 생성
        
        1단계에서 생성된 스크립트를 바탕으로 개선점과 제안사항을 생성합니다.
        
        분석 섹션:
        1. 후킹 문구: 대체 후킹 문구 제안
        2. 비주얼 요소: 화면 구성, 자막, 효과 등
        3. 트렌드 요소: 해시태그, 음악, 필터 등
        4. 최적화 팁: 타이밍, 구성, 강조점 등
        
        Args:
            script (str): 1단계에서 생성된 스크립트
            
        Returns:
            str: 제안사항 텍스트
        """
        response = self.client.messages.create(
            model=self.model,
            system=self.analysis_prompt.messages[0].prompt.template,
            messages=[
                {"role": "user", "content": f"스크립트: {script}"}
            ],
            max_tokens=4000
        )
        return response.content[0].text

    async def debug_chain(self, data: Dict) -> None:
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
        """
        섹션 내용을 리스트 형태로 파싱
        
        AI가 생성한 텍스트를 구조화된 형태로 변환합니다.
        
        파싱 규칙:
        1. 각 줄을 개별 항목으로 처리
        2. '- '로 시작하는 줄은 리스트 항목으로 처리
        3. 콜론(:)이 있는 경우 레이블과 값으로 분리
        4. 빈 줄은 무시
        
        Args:
            content (str): 파싱할 텍스트
            
        Returns:
            list: 파싱된 항목들의 리스트
        """
        if not content:
            return []
        
        # 줄바꿈으로 분리하고 빈 줄 제거
        lines = [line.strip() for line in content.split('\n') if line.strip()]
        
        # 결과 저장용 리스트
        result = []
        
        for line in lines:
            # 새로운 항목 시작 확인
            if line.startswith('- '):
                # 콜론이 있는 경우 처리
                if ':' in line:
                    label, value = line[2:].split(':', 1)
                    result.append(f"# {label.strip()}")
                    if value.strip():
                        result.append(f"- {value.strip()}")
                else:
                    result.append(line)
            # 일반 텍스트는 리스트 항목으로 변환
            else:
                result.append(f"- {line.strip()}")
        
        # 빈 문자열 제거
        result = [item.strip() for item in result if item.strip()]
        
        return result

    async def generate_script(self, data: Dict) -> Optional[Dict]:
        """숏폼 스크립트 생성"""
        try:
            # 디버깅 실행
            await self.debug_chain(data)

            # 체인 실행
            print("\n=== Chain Execution ===")
            summary = await asyncio.to_thread(self._get_summary, data)
            analysis = await asyncio.to_thread(self._get_analysis, summary)
            
            # 결과를 직접 구성
            script_result = {
                'script': summary,
                'hooks': [],
                'visual_suggestions': [],
                'trending_elements': [],
                'optimization_tips': []
            }
            
            # 섹션 매핑 정의
            section_mapping = {
                '후킹 문구 제안': 'hooks',
                '비주얼 요소 제안': 'visual_suggestions',
                '트렌드 요소': 'trending_elements',
                '최적화 팁': 'optimization_tips'
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
                            script_result[mapped_section] = parsed_content
                    
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
                    script_result[mapped_section] = parsed_content

            # 원본 입력 데이터를 결과에 포함
            script_result.update({
                'content_type': data.get('content_type', ''),
                'target_audience': data.get('target_audience', ''),
                'platform': data.get('platform', ''),
                'trend_analysis': data.get('trend_analysis', ''),
                'benchmark': data.get('benchmark', ''),
                'benchmark_point': data.get('benchmark_point', ''),
                'content_format': data.get('content_format', ''),
                'content_topic': data.get('content_topic', ''),
                'special_element': data.get('special_element', ''),
                'video_length': data.get('video_length', ''),
                'visual_element': data.get('visual_element', ''),
                'storyline': data.get('storyline', '')
            })
            
            return script_result
            
        except Exception as e:
            print(f"분석 중 오류 발생: {e}")
            return None

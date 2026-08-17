import copy
import random
from pathlib import Path

import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# 기본 설정
# ---------------------------------------------------------
st.set_page_config(
    page_title="과학 개념 빙고",
    page_icon="🧪",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------
# 문제 데이터
# 각 단어를 선택하면 해당 단어와 관련된 문제 중 하나가 무작위로 출제됩니다.
# ---------------------------------------------------------
QUESTIONS = {
    "광합성": [
        {"q": "식물이 광합성을 할 때 필요한 기체는 무엇일까요?", "a": "이산화 탄소"},
        {"q": "식물이 광합성을 하면 만들어지는 기체는 무엇일까요?", "a": "산소"},
    ],
    "호흡": [
        {"q": "식물도 낮과 밤에 모두 호흡을 할까요?", "a": "네. 식물은 낮과 밤에 모두 호흡합니다."},
        {"q": "식물이 호흡할 때 필요한 기체는 무엇일까요?", "a": "산소"},
    ],
    "엽록체": [
        {"q": "식물 세포에서 광합성이 일어나는 곳은 어디일까요?", "a": "엽록체"},
        {"q": "엽록체가 많이 들어 있어 광합성이 활발하게 일어나는 식물의 기관은 무엇일까요?", "a": "잎"},
    ],
    "기공": [
        {"q": "잎에서 이산화 탄소와 산소 같은 기체가 드나드는 작은 구멍을 무엇이라고 할까요?", "a": "기공"},
        {"q": "광합성에 필요한 이산화 탄소는 주로 잎의 어디를 통해 들어올까요?", "a": "기공"},
    ],
    "잎": [
        {"q": "식물에서 광합성이 가장 활발하게 일어나는 기관은 어디일까요?", "a": "잎"},
        {"q": "잎에서 광합성이 일어나려면 빛이 필요할까요?", "a": "네. 빛이 필요합니다."},
    ],
    "빛에너지": [
        {"q": "식물은 광합성에 필요한 에너지를 어디에서 얻을까요?", "a": "빛"},
        {"q": "광합성은 빛에너지를 이용하여 양분을 만드는 과정일까요?", "a": "네."},
    ],
    "이산화 탄소": [
        {"q": "식물은 광합성을 할 때 이산화 탄소를 흡수할까요, 방출할까요?", "a": "흡수합니다."},
        {"q": "세포호흡이 일어나면 이산화 탄소가 생길까요?", "a": "네. 생깁니다."},
    ],
    "산소": [
        {"q": "광합성이 일어나면 산소는 흡수될까요, 방출될까요?", "a": "방출됩니다."},
        {"q": "세포호흡에 필요한 기체는 무엇일까요?", "a": "산소"},
    ],
    "물": [
        {"q": "식물은 주로 어느 기관을 통해 물을 흡수할까요?", "a": "뿌리"},
        {"q": "물은 광합성에 필요한 물질일까요?", "a": "네."},
    ],
    "포도당": [
        {"q": "식물이 광합성을 통해 만드는 대표적인 양분은 무엇일까요?", "a": "포도당"},
        {"q": "세포호흡에서 에너지를 얻는 데 이용되는 대표적인 양분은 무엇일까요?", "a": "포도당"},
    ],
    "녹말": [
        {"q": "식물은 광합성으로 만든 양분을 어떤 물질로 바꾸어 저장하기도 할까요?", "a": "녹말"},
        {"q": "녹말을 확인할 때 사용하는 대표적인 용액은 무엇일까요?", "a": "아이오딘 용액"},
    ],
    "설탕": [
        {"q": "잎에서 만들어진 양분은 설탕의 형태로 다른 기관으로 이동할 수 있을까요?", "a": "네."},
        {"q": "잎에서 만들어진 양분이 이동하여 저장될 수 있는 기관을 한 가지 말해 볼까요?", "a": "뿌리, 줄기, 열매, 씨 등"},
    ],
    "빛의 세기": [
        {"q": "빛의 세기는 광합성량에 영향을 주는 환경 요인일까요?", "a": "네."},
        {"q": "빛이 전혀 없을 때 광합성이 일어날 수 있을까요?", "a": "아니요."},
    ],
    "온도": [
        {"q": "온도는 광합성량에 영향을 주는 환경 요인일까요?", "a": "네."},
        {"q": "온도가 달라져도 광합성량은 항상 똑같을까요?", "a": "아니요."},
    ],
    "열매": [
        {"q": "잎에서 만들어진 양분은 열매로 이동할 수 있을까요?", "a": "네."},
        {"q": "식물은 광합성으로 만든 양분을 열매에 저장할 수 있을까요?", "a": "네."},
    ],
    "소화": [
        {"q": "크기가 큰 영양소를 몸에 흡수될 수 있을 정도로 작게 분해하는 과정을 무엇이라고 할까요?", "a": "소화"},
        {"q": "소화된 영양소는 몸속으로 흡수될 수 있을까요?", "a": "네."},
    ],
    "소화 효소": [
        {"q": "소화 효소는 영양소를 작은 물질로 분해하는 데 도움을 줄까요?", "a": "네."},
        {"q": "침 속에서 녹말의 소화를 돕는 소화 효소는 무엇일까요?", "a": "아밀레이스"},
    ],
    "탄수화물": [
        {"q": "탄수화물이 소화되면 최종적으로 어떤 영양소가 될까요?", "a": "포도당"},
        {"q": "탄수화물의 소화는 입에서 시작될까요?", "a": "네."},
    ],
    "단백질": [
        {"q": "단백질이 소화되면 최종적으로 무엇이 될까요?", "a": "아미노산"},
        {"q": "단백질의 소화가 시작되는 기관은 어디일까요?", "a": "위"},
    ],
    "지방": [
        {"q": "지방도 소화 과정을 거쳐 더 작은 물질로 분해될까요?", "a": "네."},
        {"q": "지방의 소화를 돕는 소화액 중 간에서 만들어지는 것은 무엇일까요?", "a": "쓸개즙"},
    ],
    "위": [
        {"q": "단백질의 소화가 시작되는 기관은 어디일까요?", "a": "위"},
        {"q": "위에서 단백질의 소화를 돕는 대표적인 소화 효소는 무엇일까요?", "a": "펩신"},
    ],
    "작은창자": [
        {"q": "소화된 영양소가 주로 흡수되는 기관은 어디일까요?", "a": "작은창자"},
        {"q": "대부분의 영양소의 소화가 마무리되는 기관은 어디일까요?", "a": "작은창자"},
    ],
    "혈액": [
        {"q": "작은창자에서 흡수된 영양소를 온몸으로 운반하는 것은 무엇일까요?", "a": "혈액"},
        {"q": "폐에서 받아들인 산소를 온몸의 세포로 운반하는 것은 무엇일까요?", "a": "혈액"},
    ],
    "심장": [
        {"q": "혈액을 온몸으로 보내는 펌프 역할을 하는 기관은 무엇일까요?", "a": "심장"},
        {"q": "사람의 심장은 심방과 심실을 합쳐 모두 몇 개의 방으로 이루어져 있을까요?", "a": "4개"},
    ],
    "혈관": [
        {"q": "혈액이 이동하는 통로를 무엇이라고 할까요?", "a": "혈관"},
        {"q": "혈관에는 동맥, 정맥과 무엇이 있을까요?", "a": "모세혈관"},
    ],
    "폐": [
        {"q": "우리 몸에서 산소와 이산화 탄소의 교환이 일어나는 기관은 어디일까요?", "a": "폐"},
        {"q": "숨을 들이마실 때 폐의 부피는 커질까요, 작아질까요?", "a": "커집니다."},
    ],
    "가로막": [
        {"q": "숨을 들이마실 때 가로막은 위로 올라갈까요, 아래로 내려갈까요?", "a": "아래로 내려갑니다."},
        {"q": "숨을 내쉴 때 가로막은 위로 올라갈까요, 아래로 내려갈까요?", "a": "위로 올라갑니다."},
    ],
    "콩팥": [
        {"q": "혈액 속 노폐물을 걸러 오줌을 만드는 기관은 어디일까요?", "a": "콩팥"},
        {"q": "사람의 콩팥은 보통 몇 개일까요?", "a": "2개"},
    ],
    "동맥": [
        {"q": "심장에서 나가는 혈액이 흐르는 혈관은 무엇일까요?", "a": "동맥"},
        {"q": "동맥의 혈액은 심장에서 멀어지는 방향으로 흐를까요?", "a": "네."},
    ],
    "정맥": [
        {"q": "심장으로 들어오는 혈액이 흐르는 혈관은 무엇일까요?", "a": "정맥"},
        {"q": "정맥의 혈액은 심장을 향해 흐를까요?", "a": "네."},
    ],
    "허파꽈리": [
        {"q": "폐 속에서 실제로 기체 교환이 일어나는 작은 주머니 모양의 구조는 무엇일까요?", "a": "허파꽈리"},
        {"q": "허파꽈리 주변에는 어떤 혈관이 많이 분포할까요?", "a": "모세혈관"},
    ],
    "심방": [
        {"q": "심장으로 들어온 혈액을 먼저 받아들이는 곳은 심방일까요, 심실일까요?", "a": "심방"},
        {"q": "심방은 심실보다 위쪽에 있을까요, 아래쪽에 있을까요?", "a": "위쪽"},
    ],
    "심실": [
        {"q": "혈액을 심장 밖으로 내보내는 곳은 심방일까요, 심실일까요?", "a": "심실"},
        {"q": "심방과 심실 중 벽이 더 두꺼운 곳은 어디일까요?", "a": "심실"},
    ],
    "융털": [
        {"q": "작은창자 안쪽에 있는 수많은 돌기 모양의 구조는 무엇일까요?", "a": "융털"},
        {"q": "작은창자에 융털이 많으면 영양소를 흡수할 수 있는 면적이 넓어질까요, 좁아질까요?", "a": "넓어집니다."},
    ],
    "방광": [
        {"q": "콩팥에서 만들어진 오줌을 잠시 저장하는 기관은 어디일까요?", "a": "방광"},
        {"q": "방광에 모인 오줌은 결국 몸 밖으로 배출될까요?", "a": "네."},
    ],
    "모세혈관": [
        {"q": "혈액과 조직 세포 사이에서 물질 교환이 주로 일어나는 혈관은 무엇일까요?", "a": "모세혈관"},
        {"q": "모세혈관의 벽은 물질 교환이 쉽도록 두꺼울까요, 얇을까요?", "a": "얇습니다."},
    ],
    "세포호흡": [
        {"q": "세포호흡을 통해 생물이 얻는 것은 무엇일까요?", "a": "에너지"},
        {"q": "세포호흡에 필요한 대표적인 양분과 기체를 하나씩 말해 볼까요?", "a": "포도당과 산소"},
    ],
    "호흡계": [
        {"q": "호흡계는 우리 몸에 어떤 기체를 받아들이는 데 관여할까요?", "a": "산소"},
        {"q": "호흡계는 몸에서 생긴 어떤 기체를 밖으로 내보내는 데 관여할까요?", "a": "이산화 탄소"},
    ],
    "순환계": [
        {"q": "순환계를 이루는 주요 요소는 혈액, 혈관과 무엇일까요?", "a": "심장"},
        {"q": "순환계는 산소와 영양소를 온몸의 세포로 운반하는 데 관여할까요?", "a": "네."},
    ],
    "배설계": [
        {"q": "배설계에서 혈액 속 노폐물을 걸러 오줌을 만드는 기관은 어디일까요?", "a": "콩팥"},
        {"q": "콩팥에서 만들어진 오줌은 몸 밖으로 나가기 전에 어디에 잠시 저장될까요?", "a": "방광"},
    ],
}


# ---------------------------------------------------------
# 화면 상태
# ---------------------------------------------------------
if "selected_word" not in st.session_state:
    st.session_state.selected_word = None

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "answer_visible" not in st.session_state:
    st.session_state.answer_visible = False

# 실제 게임에서 사용하는 문제은행
if "question_bank" not in st.session_state:
    st.session_state.question_bank = copy.deepcopy(QUESTIONS)


def select_word(word):
    """단어를 선택하고 관련 문제를 무작위로 하나 뽑습니다."""
    st.session_state.selected_word = word
    st.session_state.current_question = random.choice(st.session_state.question_bank[word])
    st.session_state.answer_visible = False


def show_answer():
    st.session_state.answer_visible = True


def go_home():
    st.session_state.selected_word = None
    st.session_state.current_question = None
    st.session_state.answer_visible = False


def load_question_bank_from_excel(uploaded_file):
    """업로드한 엑셀의 '문제은행' 시트를 읽어 문제은행 딕셔너리로 변환합니다."""
    try:
        # 제공 양식은 5행이 열 제목이므로 header=4
        df = pd.read_excel(
            uploaded_file,
            sheet_name="문제은행",
            header=4,
            engine="openpyxl",
        )
    except ValueError as e:
        raise ValueError("'문제은행' 시트를 찾을 수 없습니다.") from e
    except Exception as e:
        raise ValueError(f"엑셀 파일을 읽을 수 없습니다: {e}") from e

    required = ["단어", "문제", "정답"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            "문제은행 시트의 5행에 '단어 / 문제 / 정답' 열 제목이 있어야 합니다."
        )

    df = df[required].copy()
    df = df.dropna(how="all")

    new_bank = {}
    for _, row in df.iterrows():
        word = "" if pd.isna(row["단어"]) else str(row["단어"]).strip()
        question = "" if pd.isna(row["문제"]) else str(row["문제"]).strip()
        answer = "" if pd.isna(row["정답"]) else str(row["정답"]).strip()

        # 완전히 빈 행은 무시
        if not word and not question and not answer:
            continue

        if not word or not question or not answer:
            raise ValueError(
                "단어, 문제, 정답 중 일부만 입력된 행이 있습니다. "
                "각 행의 세 칸을 모두 입력하거나 행 전체를 비워주세요."
            )

        new_bank.setdefault(word, []).append({"q": question, "a": answer})

    if not new_bank:
        raise ValueError("사용할 수 있는 문제가 없습니다.")

    return new_bank


# ---------------------------------------------------------
# 사이드바: 엑셀 문제은행 관리
# ---------------------------------------------------------
with st.sidebar:
    st.header("📚 문제은행 관리")
    st.caption("엑셀에서 문제를 수정한 뒤 한 번에 업로드할 수 있습니다.")

    template_path = Path(__file__).with_name("science_bingo_question_template.xlsx")

    if template_path.exists():
        st.download_button(
            "⬇️ 엑셀 양식 다운로드",
            data=template_path.read_bytes(),
            file_name="science_bingo_question_template.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True,
        )
    else:
        st.warning(
            "엑셀 양식 파일을 찾을 수 없습니다. "
            "GitHub 저장소에 science_bingo_question_template.xlsx 파일도 함께 올려주세요."
        )

    st.divider()

    uploaded_excel = st.file_uploader(
        "문제은행 엑셀 업로드",
        type=["xlsx"],
        help="제공된 양식의 '문제은행' 시트를 수정한 파일을 올려주세요.",
    )

    if uploaded_excel is not None:
        if st.button("✅ 업로드한 문제은행 적용", use_container_width=True):
            try:
                new_bank = load_question_bank_from_excel(uploaded_excel)
                st.session_state.question_bank = new_bank
                go_home()
                st.success(
                    f"적용 완료: {len(new_bank)}개 단어 / "
                    f"{sum(len(v) for v in new_bank.values())}개 문제"
                )
                st.rerun()
            except ValueError as e:
                st.error(str(e))

    st.divider()

    total_cards = len(st.session_state.question_bank)
    total_questions = sum(
        len(items) for items in st.session_state.question_bank.values()
    )
    st.info(f"현재 문제은행: **{total_cards}개 단어 · {total_questions}개 문제**")

    if st.button("↩️ 기본 문제은행으로 초기화", use_container_width=True):
        st.session_state.question_bank = copy.deepcopy(QUESTIONS)
        go_home()
        st.rerun()

    st.caption(
        "※ 업로드한 내용은 현재 앱 세션에 적용됩니다. "
        "앱이 완전히 재시작되거나 재배포되면 기본 문제은행으로 돌아갑니다."
    )


# 현재 문제은행의 단어 카드 목록
WORDS = list(st.session_state.question_bank.keys())


# ---------------------------------------------------------
# 스타일
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1500px;
            padding-top: 0.45rem;
            padding-bottom: 0.5rem;
        }

        /* 제목 */
        h1, .stApp h1 {
            text-align: center !important;
            font-size: 2.8rem !important;
            font-weight: 900 !important;
            line-height: 1.0 !important;
            letter-spacing: -0.04em !important;
            margin-bottom: 0.15rem !important;
        }

        /* 첫 화면 안내문 */
        .subtitle {
            text-align: center;
            font-size: 1.15rem !important;
            font-weight: 800 !important;
            color: #444;
            margin-bottom: 1.35rem;
            word-break: keep-all;
        }

        /* 안내문과 첫 번째 카드 줄 사이의 실제 여백 */
        .card-top-spacer {
            height: 22px;
        }

        /* Streamlit 버튼 자체 */
        div[data-testid="stButton"] > button,
        div.stButton > button {
            width: 100% !important;
            min-height: 52px !important;
            height: 52px !important;
            border-radius: 12px !important;
            padding: 0.2rem 0.55rem !important;
        }

        /* 버튼 안의 텍스트: Streamlit 버전 차이를 모두 커버 */
        div[data-testid="stButton"] > button *,
        div.stButton > button * {
            font-size: 1.35rem !important;
            font-weight: 900 !important;
            line-height: 1.15 !important;
            word-break: keep-all !important;
        }

        /* 5열 카드 행 사이의 세로 간격을 최소화 */
        [data-testid="stMain"] [data-testid="stHorizontalBlock"] {
            gap: 0.55rem !important;
            margin-bottom: -0.35rem !important;
        }

        .category {
            text-align: center;
            font-size: 1.9rem !important;
            font-weight: 900 !important;
            margin-top: 0.2rem;
            margin-bottom: 1rem;
        }

        .question-card {
            padding: 2.4rem 2.6rem;
            border: 2px solid #e5e7eb;
            border-radius: 22px;
            background: white;
            box-shadow: 0 8px 28px rgba(0,0,0,0.06);
            margin: 1rem 0 1.4rem 0;
        }

        .question-label {
            text-align: center;
            font-size: 1.55rem !important;
            font-weight: 900 !important;
            margin-bottom: 1rem;
        }

        .question-text {
            text-align: center;
            font-size: 3rem !important;
            line-height: 1.45 !important;
            font-weight: 900 !important;
            word-break: keep-all;
        }

        .answer-card {
            padding: 1.6rem 1.8rem;
            border-radius: 18px;
            background: #f3f4f6;
            margin: 1rem 0 1.4rem 0;
        }

        .answer-label {
            text-align: center;
            font-size: 1.4rem !important;
            font-weight: 900 !important;
            margin-bottom: 0.5rem;
        }

        .answer-text {
            text-align: center;
            font-size: 2.7rem !important;
            font-weight: 900 !important;
            word-break: keep-all;
        }

        /* 사이드바 버튼은 관리용이므로 작게 표시 */
        [data-testid="stSidebar"] div[data-testid="stButton"] > button,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button {
            min-height: 44px !important;
            padding: 0.4rem 0.6rem !important;
            border-radius: 10px !important;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button *,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button * {
            font-size: 1rem !important;
            font-weight: 800 !important;
            line-height: 1.2 !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# 메인 화면: 40개 단어
# ---------------------------------------------------------
if st.session_state.selected_word is None:
    st.title("🧪 과학 개념 빙고")
    st.markdown(
        '<div class="subtitle">학생이 고른 단어를 클릭하면 관련 문제가 무작위로 출제됩니다.</div>',
        unsafe_allow_html=True,
    )

    # 첫 번째 카드 줄이 안내문에 붙지 않도록 실제 공간 확보
    st.markdown('<div class="card-top-spacer"></div>', unsafe_allow_html=True)

    # 5열 × 8행
    for row_start in range(0, len(WORDS), 5):
        cols = st.columns(5)
        row_words = WORDS[row_start:row_start + 5]

        for col, word in zip(cols, row_words):
            with col:
                st.button(
                    word,
                    key=f"word_{word}",
                    on_click=select_word,
                    args=(word,),
                    use_container_width=True,
                )

# ---------------------------------------------------------
# 문제 화면
# ---------------------------------------------------------
else:
    word = st.session_state.selected_word
    question = st.session_state.current_question

    st.title("🧪 과학 개념 빙고")
    st.markdown(
        f'<div class="category">선택한 단어: {word}</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="question-card">
            <div class="question-label">문제</div>
            <div class="question-text">{question["q"]}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not st.session_state.answer_visible:
        left, center, right = st.columns([1, 2, 1])
        with center:
            st.button(
                "👀 정답 보기",
                key="show_answer_button",
                on_click=show_answer,
                type="primary",
                use_container_width=True,
            )
    else:
        st.markdown(
            f"""
            <div class="answer-card">
                <div class="answer-label">정답</div>
                <div class="answer-text">{question["a"]}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    left, center, right = st.columns([1, 2, 1])
    with center:
        st.button(
            "← 단어 목록으로",
            key="go_home",
            on_click=go_home,
            use_container_width=True,
        )

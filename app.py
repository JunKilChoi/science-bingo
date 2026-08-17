import copy
import json
import random

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

# 실제 게임에서 사용하는 문제 은행
# 사이드바에서 수정하면 이 데이터가 즉시 바뀝니다.
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


# ---------------------------------------------------------
# 사이드바: 카드 / 문제 / 정답 편집
# ---------------------------------------------------------
with st.sidebar:
    st.header("⚙️ 카드·문제 편집")
    st.caption("게임 중에도 수정할 수 있습니다. 저장하면 즉시 반영됩니다.")

    bank = st.session_state.question_bank
    edit_words = list(bank.keys())

    if edit_words:
        selected_edit_word = st.selectbox(
            "수정할 단어 카드",
            edit_words,
            key="editor_selected_word",
        )

        current_rows = pd.DataFrame(bank[selected_edit_word])
        if current_rows.empty:
            current_rows = pd.DataFrame([{"q": "", "a": ""}])

        current_rows = current_rows.rename(columns={"q": "문제", "a": "정답"})

        with st.form(key=f"edit_form_{selected_edit_word}"):
            new_word_name = st.text_input(
                "카드 이름",
                value=selected_edit_word,
            )

            st.markdown("**문제와 정답**")
            edited_rows = st.data_editor(
                current_rows,
                hide_index=True,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "문제": st.column_config.TextColumn(
                        "문제",
                        width="large",
                        help="학생에게 보여줄 문제",
                    ),
                    "정답": st.column_config.TextColumn(
                        "정답",
                        width="medium",
                        help="정답 보기에서 표시할 내용",
                    ),
                },
                key=f"question_editor_{selected_edit_word}",
            )

            save_changes = st.form_submit_button(
                "💾 이 카드 저장",
                use_container_width=True,
            )

        if save_changes:
            new_word_name = new_word_name.strip()

            cleaned_questions = []
            for _, row in edited_rows.iterrows():
                q = str(row.get("문제", "")).strip()
                a = str(row.get("정답", "")).strip()

                # 완전히 빈 행은 무시
                if not q and not a:
                    continue

                if q and a:
                    cleaned_questions.append({"q": q, "a": a})

            if not new_word_name:
                st.error("카드 이름을 입력해주세요.")
            elif new_word_name != selected_edit_word and new_word_name in bank:
                st.error("같은 이름의 카드가 이미 있습니다.")
            elif not cleaned_questions:
                st.error("문제와 정답을 최소 1개는 남겨주세요.")
            else:
                # 기존 카드의 위치를 유지한 채 이름과 내용을 교체
                new_bank = {}
                for word, questions in bank.items():
                    if word == selected_edit_word:
                        new_bank[new_word_name] = cleaned_questions
                    else:
                        new_bank[word] = questions

                st.session_state.question_bank = new_bank

                # 현재 문제 화면에서 이 카드를 열어 둔 경우 이름도 맞춰줌
                if st.session_state.selected_word == selected_edit_word:
                    st.session_state.selected_word = new_word_name

                st.success("저장했습니다. 게임 화면에 바로 반영됩니다.")

        st.divider()
        st.subheader("➕ 새 카드 추가")

        with st.form("add_card_form", clear_on_submit=True):
            add_word_name = st.text_input("새 카드 이름")
            add_question = st.text_input("첫 문제")
            add_answer = st.text_input("첫 정답")
            add_card = st.form_submit_button(
                "카드 추가",
                use_container_width=True,
            )

        if add_card:
            add_word_name = add_word_name.strip()
            add_question = add_question.strip()
            add_answer = add_answer.strip()

            if not add_word_name or not add_question or not add_answer:
                st.error("카드 이름, 문제, 정답을 모두 입력해주세요.")
            elif add_word_name in st.session_state.question_bank:
                st.error("같은 이름의 카드가 이미 있습니다.")
            else:
                st.session_state.question_bank[add_word_name] = [
                    {"q": add_question, "a": add_answer}
                ]
                st.success(f"'{add_word_name}' 카드를 추가했습니다.")
                st.rerun()

        st.divider()
        st.subheader("💾 편집 내용 백업")

        question_json = json.dumps(
            st.session_state.question_bank,
            ensure_ascii=False,
            indent=2,
        )

        st.download_button(
            "JSON으로 저장",
            data=question_json,
            file_name="science_bingo_questions.json",
            mime="application/json",
            use_container_width=True,
        )

        uploaded_json = st.file_uploader(
            "저장한 JSON 불러오기",
            type=["json"],
        )

        if uploaded_json is not None:
            if st.button("JSON 적용", use_container_width=True):
                try:
                    loaded = json.load(uploaded_json)

                    valid = (
                        isinstance(loaded, dict)
                        and all(
                            isinstance(word, str)
                            and isinstance(items, list)
                            and len(items) > 0
                            and all(
                                isinstance(item, dict)
                                and isinstance(item.get("q"), str)
                                and isinstance(item.get("a"), str)
                                for item in items
                            )
                            for word, items in loaded.items()
                        )
                    )

                    if not valid:
                        raise ValueError("올바른 문제 데이터 형식이 아닙니다.")

                    st.session_state.question_bank = loaded
                    go_home()
                    st.success("문제 데이터를 불러왔습니다.")
                    st.rerun()

                except Exception as e:
                    st.error(f"불러오기에 실패했습니다: {e}")

        if st.button("↩️ 처음 문제로 되돌리기", use_container_width=True):
            st.session_state.question_bank = copy.deepcopy(QUESTIONS)
            go_home()
            st.success("처음 문제로 되돌렸습니다.")
            st.rerun()

        st.caption(
            "※ Streamlit Cloud에서 앱을 다시 시작하거나 재배포하면 "
            "앱 안에서 수정한 내용이 사라질 수 있습니다. "
            "계속 사용할 수정본은 JSON으로 저장해 두는 것이 안전합니다."
        )

# 현재 문제 은행의 카드 목록
WORDS = list(st.session_state.question_bank.keys())


# ---------------------------------------------------------
# 스타일
# ---------------------------------------------------------
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1500px;
            padding-top: 1.2rem;
            padding-bottom: 2rem;
        }

        /* 제목 */
        h1, .stApp h1 {
            text-align: center !important;
            font-size: 4rem !important;
            font-weight: 900 !important;
            line-height: 1.1 !important;
            letter-spacing: -0.04em !important;
            margin-bottom: 0.5rem !important;
        }

        /* 첫 화면 안내문 */
        .subtitle {
            text-align: center;
            font-size: 1.8rem !important;
            font-weight: 800 !important;
            color: #444;
            margin-bottom: 2rem;
            word-break: keep-all;
        }

        /* Streamlit 버튼 자체 */
        div[data-testid="stButton"] > button,
        div.stButton > button {
            width: 100% !important;
            min-height: 88px !important;
            border-radius: 16px !important;
            padding: 0.65rem 0.8rem !important;
        }

        /* 버튼 안의 텍스트: Streamlit 버전 차이를 모두 커버 */
        div[data-testid="stButton"] > button *,
        div.stButton > button * {
            font-size: 1.8rem !important;
            font-weight: 900 !important;
            line-height: 1.15 !important;
            word-break: keep-all !important;
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

        /* 사이드바 편집 버튼은 작게 유지 */
        [data-testid="stSidebar"] div[data-testid="stButton"] > button,
        [data-testid="stSidebar"] div.stButton > button,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button {
            min-height: 42px !important;
            padding: 0.35rem 0.55rem !important;
            border-radius: 10px !important;
        }

        [data-testid="stSidebar"] div[data-testid="stButton"] > button *,
        [data-testid="stSidebar"] div.stButton > button *,
        [data-testid="stSidebar"] div[data-testid="stDownloadButton"] > button * {
            font-size: 0.95rem !important;
            font-weight: 700 !important;
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

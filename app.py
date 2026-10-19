import random
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="사람일까? AI일까?", layout="centered")

IMAGE_DIR = Path(__file__).parent / "images"

# ---------------------------------------------------------------------------
# 문항 데이터  (교사가 이 부분만 고치면 내용 교체 가능)
#   kind = "compare" : 두 개를 보고 'AI가 만든 쪽'을 고르기
#   kind = "judge"   : 하나를 보고 'AI인지 사람인지' 판단하기
# ---------------------------------------------------------------------------
QUESTIONS = [
    {
        "id": 1,
        "category": "문자 답장",
        "kind": "compare",
        "prompt": '친구에게 "나 오늘 수학 시험 완전 망쳤어 ㅠㅠ"라고 문자를 보냈습니다. '
                  "돌아온 답장 두 개 중에서 **AI가 쓴 답장**은 무엇일까요?",
        "hint": "친구는 보통 '내 이야기'를 먼저 합니다. 상담 선생님처럼 말하는 쪽을 의심해 보세요.",
        "options": [
            {"text": "그런 일이 있었군요. 시험 결과가 기대에 미치지 못해 속상하셨을 것 같아요. "
                     "하지만 한 번의 시험이 당신의 가치를 결정하지는 않습니다. "
                     "다음 시험을 위해 함께 계획을 세워 보는 것은 어떨까요?",
             "is_ai": True},
            {"text": "ㅋㅋㅋㅋ 나도 3번부터 다 찍었어 ㅠㅠ 야 그냥 떡볶이나 먹으러 가자",
             "is_ai": False},
        ],
        "note": "AI는 **감정 요약 → 위로 → 조언**의 순서로 정중하게 답하는 습관이 있습니다. "
                "친구 사이 문자에는 존댓말 대신 줄임말, 자기 이야기, 즉흥적인 제안이 들어갑니다.",
    },
    {
        "id": 2,
        "category": "독후감",
        "kind": "judge",
        "prompt": "다음 독후감의 마지막 문단을 읽어 보세요. 누가 썼을까요?",
        "hint": "글에 '그 사람만 쓸 수 있는 구체적인 장면'이 있는지 찾아보세요.",
        "content": "이 책을 읽고 나는 많은 것을 느꼈다. 주인공의 용기와 성장은 우리에게 깊은 감동을 준다. "
                   "또한 이 작품은 우정의 소중함과 가족의 의미를 다시 생각하게 해 준다. "
                   "이처럼 이 책은 시대를 넘어 많은 사람에게 사랑받는 작품이며, "
                   "나도 앞으로 이 책에서 배운 교훈을 잊지 않고 살아가고 싶다.",
        "is_ai": True,
        "note": "'많은 것을 느꼈다', '시대를 넘어 사랑받는' 처럼 **어느 책에 붙여도 맞는 문장**만 이어집니다. "
                "사람이 쓴 독후감에는 특정 장면, 솔직한 불만, 사소한 개인 경험이 끼어듭니다.",
    },
    {
        "id": 3,
        "category": "시 쓰기",
        "kind": "compare",
        "prompt": "'비'를 주제로 쓴 두 편의 시입니다. **AI가 쓴 시**는 무엇일까요?",
        "hint": "예쁜 비유가 많은 쪽과, 실제로 겪은 일이 적힌 쪽을 비교해 보세요.",
        "options": [
            {"text": "비가 온다\n우산이 없다\n가방을 머리에 얹고\n학원까지 뛰었다\n"
                     "양말이 질척질척\n선생님이 왜 늦었냐고 물었다\n비 때문이라고 말했다",
             "is_ai": False},
            {"text": "하늘이 울면\n대지는 노래한다\n투명한 눈물방울마다\n작은 희망이 피어나고\n"
                     "젖은 거리 위에\n새로운 꿈이 자란다",
             "is_ai": True},
        ],
        "note": "AI는 '하늘의 눈물', '희망이 피어난다'처럼 **많이 본 비유**를 즐겨 씁니다. "
                "사람의 글에는 양말, 학원, 선생님처럼 직접 겪지 않으면 나오지 않는 디테일이 남습니다.",
    },
    {
        "id": 4,
        "category": "사진",
        "kind": "judge",
        "prompt": "다음 사진은 카메라로 찍은 사진일까요, AI가 만든 이미지일까요?",
        "hint": "손가락 개수, 글자, 배경의 선, 귀걸이나 안경의 좌우 모양을 확대해서 보세요.",
        "image": "q4.png",
        "image_caption": "교실에 걸어 둘 사진 1장",
        "is_ai": True,
        "note": "AI 이미지 점검 포인트: ① 손가락·치아 개수 ② 간판이나 책의 **글자가 뭉개짐** "
                "③ 배경의 직선이 휘어짐 ④ 좌우 액세서리가 다름 ⑤ 피부와 조명이 비현실적으로 매끈함.",
    },
    {
        "id": 5,
        "category": "가게 후기",
        "kind": "compare",
        "prompt": "같은 분식집에 달린 후기 두 개입니다. **AI가 쓴 후기**는 무엇일까요?",
        "hint": "'직접 가 본 사람만 알 수 있는 정보'가 몇 개 있는지 세어 보세요.",
        "options": [
            {"text": "이 식당은 전반적으로 만족스러운 경험을 제공했습니다. 신선한 재료로 정성스럽게 조리된 음식과 "
                     "직원분들의 친절한 응대가 인상적이었습니다. 가족 단위 방문객에게 추천할 만한 곳입니다.",
             "is_ai": True},
            {"text": "웨이팅 40분;; 근데 계란찜 리필 되는 거 실화냐 ㅋㅋ 주차는 골목에 해야 해서 좀 불편함. "
                     "사장님이 콜라 서비스 주셨음",
             "is_ai": False},
        ],
        "note": "AI 후기는 장점을 골고루 나열하고 '추천합니다'로 끝맺습니다. "
                "사람 후기는 대기 시간, 주차, 리필처럼 **검증 가능한 구체적 사실**과 감정이 뒤섞입니다.",
    },
    {
        "id": 6,
        "category": "학급 공지",
        "kind": "judge",
        "prompt": "학급 단톡방에 올라온 공지입니다. 누가 썼을까요? (함정 주의!)",
        "hint": "'글이 깔끔하다'는 것만으로 AI라고 단정할 수 있을까요?",
        "content": "1학년 3반 공지입니다. 내일(5월 14일) 현장학습 때문에 8시 20분까지 학교 운동장으로 모여 주세요. "
                   "도시락과 물, 우산을 꼭 챙기고 멀미약이 필요한 사람은 미리 먹고 오면 좋겠습니다. "
                   "비가 많이 오면 체육관에서 모이니 아침에 단톡방을 꼭 확인해 주세요.  - 반장 서연",
        "is_ai": False,
        "note": "날짜, 시간, 장소, 비 올 때의 대안처럼 **틀리면 자신이 책임져야 하는 정보**가 촘촘합니다. "
                "AI는 이런 우리 반만의 사실을 알지 못합니다. '반듯하게 쓰면 AI'라는 생각은 위험한 편견입니다.",
    },
    {
        "id": 7,
        "category": "그림",
        "kind": "compare",
        "prompt": "두 그림 중 **AI가 만든 그림**은 무엇일까요?",
        "hint": "선의 떨림, 색칠이 삐져나간 부분, 지우개 흔적을 찾아보세요.",
        "options": [
            {"image": "q7_a.png", "caption": "A 그림", "is_ai": True},
            {"image": "q7_b.png", "caption": "B 그림", "is_ai": False},
        ],
        "note": "사람의 그림에는 떨린 선, 지운 자국, 번진 색처럼 **실수의 흔적**이 남습니다. "
                "AI 그림은 질감이 균일한 대신 손가락, 글자, 반복되는 무늬에서 어색함이 나타납니다.",
    },
    {
        "id": 8,
        "category": "고객센터 대화",
        "kname": "",
        "kind": "judge",
        "prompt": "쇼핑몰 채팅 상담에서 3초 만에 도착한 답변입니다. 상담원은 사람일까요, AI일까요?",
        "hint": "답변의 '구조'가 매번 똑같은지 생각해 보세요.",
        "content": "안녕하세요, 고객님. 문의해 주셔서 감사합니다. 말씀하신 배송 지연으로 불편을 드려 죄송합니다. "
                   "주문번호를 알려 주시면 더욱 정확하게 안내해 드리겠습니다. "
                   "다른 궁금한 점이 있으시면 언제든 말씀해 주세요.",
        "is_ai": True,
        "note": "**인사 → 사과 → 정보 요청 → 마무리** 구조가 항상 같고, 오타 없이 즉시 도착합니다. "
                "사람 상담원은 '잠시만요', 오타, 말줄임처럼 작업 중의 흔적을 남깁니다.",
    },
    {
        "id": 9,
        "category": "유머",
        "kind": "compare",
        "prompt": "친구들끼리 한 농담 두 개입니다. **AI가 만든 농담**은 무엇일까요?",
        "hint": "농담을 하고 나서 스스로 친절하게 설명해 주는 쪽이 있나요?",
        "options": [
            {"text": "왜 컴퓨터는 추위를 타지 않을까요? 창문(Windows)이 있기 때문입니다!",
             "is_ai": True},
            {"text": "야 급식에 탕수육 나왔는데 소스가 없었음. 이건 탕수육이 아니고 그냥 육임",
             "is_ai": False},
        ],
        "note": "AI 농담은 '왜 ~일까요? ~때문입니다' 형태로 정리되고 말장난을 괄호로 풀어 줍니다. "
                "사람의 농담은 **그 자리의 상황(오늘 급식)**에서 즉흥적으로 튀어나옵니다.",
    },
    {
        "id": 10,
        "category": "SNS 댓글",
        "kind": "judge",
        "prompt": "마지막 문제입니다. 이 댓글은 누가 썼을까요?",
        "hint": "AI에게 '중학생처럼 ㅋㅋ 섞어서 써 줘'라고 부탁하면 어떤 글이 나올까요?",
        "content": "헐 나도 어제 그거 봤는데 진짜 미쳤음 ㅋㅋㅋ 마지막 장면에서 나 소리 질렀잖아 ㅠㅠ "
                   "2편 언제 나와 ㅠㅠㅠ",
        "is_ai": True,
        "note": "AI는 요청만 하면 줄임말과 'ㅋㅋ'까지 흉내 냅니다. 즉 **말투만으로는 더 이상 구분할 수 없습니다.** "
                "앞으로는 '어떻게 말하는가'보다 **확인할 수 있는 사실과 맥락**을 봐야 합니다.",
    },
]

TOTAL = len(QUESTIONS)

DISCUSSION = [
    "내가 AI라고 판단할 때 사용한 단서는 무엇이었나요?",
    "사람이 쓴 글을 AI라고 오해한 문제가 있었나요? 왜 그렇게 생각했나요?",
    "AI가 쓴 글을 그대로 숙제로 내면 어떤 문제가 생길까요?",
    "말투까지 똑같이 흉내 내는 AI 시대에, 상대가 사람임을 확인하려면 무엇을 물어봐야 할까요?",
]

STATE_KEYS = ["stage", "order", "idx", "records", "checked", "nickname"]


def init_state():
    if "stage" not in st.session_state:
        st.session_state.stage = "intro"
        st.session_state.order = list(range(TOTAL))
        st.session_state.idx = 0
        st.session_state.records = []
        st.session_state.checked = False
        st.session_state.nickname = ""


def reset_all():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    init_state()


def show_media(filename, caption=None):
    path = IMAGE_DIR / filename
    if path.exists():
        st.image(str(path), caption=caption, use_container_width=True)
    else:
        st.warning(
            "이미지 준비 안내: `images/" + filename + "` 파일을 넣어 주세요.\n\n"
            "(교사용) 이 자리에 보여 줄 사진이나 그림을 images 폴더에 같은 이름으로 저장하면 됩니다."
        )
        if caption:
            st.caption(caption)


# ---------------------------------------------------------------------------
# 화면 1. 시작
# ---------------------------------------------------------------------------
def page_intro():
    st.title("사람일까? AI일까?")
    st.subheader("10문제로 해 보는 간이 튜링 테스트")
    st.markdown(
        "1950년, 앨런 튜링은 이런 질문을 했습니다.\n\n"
        "> 커튼 뒤에서 대화만 주고받았을 때, 상대가 **사람인지 기계인지** 알아낼 수 있을까?\n\n"
        "오늘은 문자 답장, 글, 사진, 그림을 보고 **사람이 만든 것과 AI가 만든 것**을 구분해 봅니다. "
        "총 10문제이고, 한 문제를 풀 때마다 바로 정답과 단서를 확인할 수 있습니다."
    )
    st.text_input("이름 또는 모둠 이름 (선택)", key="nickname", placeholder="예: 1모둠")
    shuffle = st.checkbox("문제 순서 섞기", value=False)
    if st.button("테스트 시작하기", type="primary", use_container_width=True):
        order = list(range(TOTAL))
        if shuffle:
            random.shuffle(order)
        st.session_state.order = order
        st.session_state.stage = "quiz"
        st.rerun()


# ---------------------------------------------------------------------------
# 화면 2. 문제 풀이
# ---------------------------------------------------------------------------
def render_compare(q, key):
    labels = ["A", "B"]
    cols = st.columns(2)
    for col, label, opt in zip(cols, labels, q["options"]):
        with col:
            st.markdown("**" + label + "**")
            if "image" in opt:
                show_media(opt["image"], opt.get("caption"))
            else:
                with st.container(border=True):
                    st.markdown(opt["text"].replace("\n", "  \n"))
    choice = st.radio(
        "AI가 만든 쪽은?",
        options=[0, 1],
        format_func=lambda i: labels[i] + " 가 AI",
        key=key,
        horizontal=True,
        index=None,
    )
    return choice


def render_judge(q, key):
    if "image" in q:
        show_media(q["image"], q.get("image_caption"))
    if "content" in q:
        with st.container(border=True):
            st.markdown(q["content"].replace("\n", "  \n"))
    choice = st.radio(
        "누가 만들었을까요?",
        options=[True, False],
        format_func=lambda v: "AI가 만들었다" if v else "사람이 만들었다",
        key=key,
        horizontal=True,
        index=None,
    )
    return choice


def page_quiz():
    pos = st.session_state.idx
    q = QUESTIONS[st.session_state.order[pos]]
    key = "choice_" + str(q["id"])

    st.progress(pos / TOTAL, text=str(pos + 1) + " / " + str(TOTAL) + " 번 문제")
    st.caption("유형: " + q["category"])
    st.markdown("### " + q["prompt"])

    with st.expander("힌트 보기"):
        st.write(q["hint"])

    if q["kind"] == "compare":
        choice = render_compare(q, key)
    else:
        choice = render_judge(q, key)

    st.divider()

    if not st.session_state.checked:
        if st.button("정답 확인", type="primary", use_container_width=True):
            if choice is None:
                st.warning("먼저 하나를 선택해 주세요.")
            else:
                if q["kind"] == "compare":
                    correct = q["options"][choice]["is_ai"]
                    my_answer = "A" if choice == 0 else "B"
                    answer = "A" if q["options"][0]["is_ai"] else "B"
                else:
                    correct = (choice == q["is_ai"])
                    my_answer = "AI" if choice else "사람"
                    answer = "AI" if q["is_ai"] else "사람"
                st.session_state.records.append(
                    {
                        "no": pos + 1,
                        "category": q["category"],
                        "mine": my_answer,
                        "answer": answer,
                        "correct": correct,
                        "note": q["note"],
                    }
                )
                st.session_state.checked = True
                st.rerun()
        return

    rec = st.session_state.records[-1]
    if rec["correct"]:
        st.success("정답입니다! (정답: " + rec["answer"] + ")")
    else:
        st.error("아쉽네요. 정답은 " + rec["answer"] + " 입니다.")
    st.info("**단서 정리** · " + q["note"])

    label = "결과 보기" if pos + 1 == TOTAL else "다음 문제"
    if st.button(label, type="primary", use_container_width=True):
        st.session_state.checked = False
        if pos + 1 == TOTAL:
            st.session_state.stage = "result"
        else:
            st.session_state.idx += 1
        st.rerun()


# ---------------------------------------------------------------------------
# 화면 3. 결과
# ---------------------------------------------------------------------------
def grade_message(score):
    if score >= 9:
        return "AI 탐정", "단서를 아주 정확하게 찾아냈습니다."
    if score >= 7:
        return "관찰력 우수", "대체로 잘 구분했습니다. 틀린 문제의 단서를 다시 확인해 보세요."
    if score >= 4:
        return "성장 중", "절반 정도 맞혔습니다. 요즘 AI는 정말 사람처럼 쓴다는 증거입니다."
    return "AI에게 속았다", "AI가 그만큼 정교해졌다는 뜻입니다. 단서 정리를 함께 읽어 봅시다."


def page_result():
    records = st.session_state.records
    score = sum(1 for r in records if r["correct"])
    title, message = grade_message(score)

    who = st.session_state.nickname.strip()
    st.title("결과" + (" · " + who if who else ""))
    c1, c2, c3 = st.columns(3)
    c1.metric("맞힌 개수", str(score) + " / " + str(TOTAL))
    c2.metric("정답률", str(int(score / TOTAL * 100)) + "%")
    c3.metric("평가", title)
    st.write(message)

    st.subheader("문제별 복습")
    header = "| 번호 | 유형 | 내 선택 | 정답 | 결과 |\n|---|---|---|---|---|\n"
    rows = ""
    for r in records:
        mark = "O" if r["correct"] else "X"
        rows += ("| " + str(r["no"]) + " | " + r["category"] + " | " + r["mine"]
                 + " | " + r["answer"] + " | " + mark + " |\n")
    st.markdown(header + rows)

    with st.expander("단서 정리 다시 보기"):
        for r in records:
            st.markdown("**" + str(r["no"]) + ". " + r["category"] + "** · " + r["note"])

    st.subheader("함께 이야기해 봅시다")
    for i, item in enumerate(DISCUSSION, start=1):
        st.markdown(str(i) + ". " + item)

    st.info(
        "오늘의 결론: AI는 **그럴듯한 평균적인 문장**을 잘 만들고, 사람은 **직접 겪은 구체적인 경험**을 씁니다. "
        "하지만 AI는 말투까지 흉내 낼 수 있으므로, 글의 느낌만으로 판단하지 말고 "
        "사실을 확인하는 습관이 필요합니다."
    )

    if st.button("다시 하기", use_container_width=True):
        reset_all()
        st.rerun()


# ---------------------------------------------------------------------------
# 사이드바 (교사용)
# ---------------------------------------------------------------------------
def sidebar():
    with st.sidebar:
        st.markdown("### 진행 상황")
        if st.session_state.stage == "quiz":
            st.write("문제 " + str(st.session_state.idx + 1) + " / " + str(TOTAL))
        else:
            st.write(st.session_state.stage)
        solved = len(st.session_state.records)
        correct = sum(1 for r in st.session_state.records if r["correct"])
        st.write("푼 문제: " + str(solved) + "개 / 맞힌 문제: " + str(correct) + "개")
        st.divider()
        if st.checkbox("교사용 정답지 보기"):
            for i, q in enumerate(QUESTIONS, start=1):
                if q["kind"] == "compare":
                    ans = "A" if q["options"][0]["is_ai"] else "B"
                else:
                    ans = "AI" if q["is_ai"] else "사람"
                st.write(str(i) + ". " + q["category"] + " → " + ans)
        st.divider()
        if st.button("처음으로 돌아가기"):
            reset_all()
            st.rerun()


def main():
    init_state()
    sidebar()
    if st.session_state.stage == "intro":
        page_intro()
    elif st.session_state.stage == "quiz":
        page_quiz()
    else:
        page_result()


if __name__ == "__main__":
    main()

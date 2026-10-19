# -*- coding: utf-8 -*-
# 사람 vs AI 구별 챌린지 - 중학교 1학년 인공지능 수업용 간이 튜링 테스트
# 실행: streamlit run app.py

import os
import random
import streamlit as st

# =====================================================================
# 1) 테마 - 색상/모양을 여기서만 바꾸면 앱 전체에 적용됩니다
#    PPT 색을 스포이드로 찍어서 아래 HEX 값만 교체하세요.
# =====================================================================
THEME = {
    "BG": "#F5F2FF",          # 배경
    "SURFACE": "#FFFFFF",     # 카드 배경
    "INK": "#1C1340",         # 진한 글자
    "INK_SOFT": "#6E679B",    # 흐린 글자
    "PRIMARY": "#6C4CF1",     # 포인트(보라)
    "PRIMARY_SOFT": "#EDE7FF",
    "ACCENT": "#00BFA6",      # 보조 포인트(민트)
    "ACCENT_SOFT": "#DEF7F3",
    "LINE": "#E4DDFB",        # 테두리
    "GOOD": "#17A673",        # 정답
    "BAD": "#F4567A",         # 오답
    "RADIUS": "22px",
}

TITLE = "사람 vs AI 구별 챌린지"
SUBTITLE = "문자부터 사진까지, 진짜를 찾아내는 10가지 문제!"
TAGS = ["#생성형AI", "#튜링테스트", "#사람인가AI인가"]

# =====================================================================
# 2) 문제 - QUESTIONS 리스트만 고치면 문항이 바뀝니다
#    kind "compare" : A/B 두 개 중 AI가 만든 것 고르기
#    kind "judge"   : 하나를 보고 AI인지 사람인지 판단하기
#    image 키를 쓰면 images 폴더의 그림 파일을 보여줍니다
# =====================================================================
QUESTIONS = [
    {
        "kind": "compare",
        "tag": "#문자답장",
        "title": "시험을 망친 친구에게 온 답장",
        "prompt": "친구에게 '나 수학 시험 완전 망했어'라고 보냈더니 이런 답장이 왔어요. 둘 중 AI가 쓴 답장은?",
        "hint": "위로하는 말에 '정리'와 '제안'이 들어 있는지 살펴보세요.",
        "options": [
            {"label": "A", "text": "ㅠㅠ 헐 나도 3번부터 다 틀린듯 걍 떡볶이 먹으러 가자", "is_ai": False},
            {"label": "B", "text": "속상한 마음이 충분히 이해돼. 하지만 이번 시험은 과정의 일부일 뿐이야. 틀린 문제를 정리해 보면 다음에는 분명 더 좋은 결과를 얻을 수 있을 거야. 힘내!", "is_ai": True},
        ],
        "note": "B는 '이해돼 → 위로 → 해결책 제안 → 응원'으로 순서가 너무 깔끔합니다. 친구끼리 급하게 보내는 문자에는 보통 오타, 줄임말, 자기 이야기가 섞입니다.",
    },
    {
        "kind": "judge",
        "tag": "#SNS후기",
        "title": "급식 후기 한 줄",
        "prompt": "이 글은 AI가 썼을까요, 사람이 썼을까요?",
        "content": "오늘 급식 탕수육 진짜 미쳤다 근데 소스가 부어져 나와서 좀 축축했음 그래도 두 번 받아먹음ㅋㅋ",
        "is_ai": False,
        "hint": "좋은 점만 말하는지, 아쉬운 점도 솔직하게 말하는지 보세요.",
        "note": "사람이 쓴 글입니다. '축축했음' 같은 구체적인 불만과 '두 번 받아먹음'처럼 겪은 사람만 아는 행동이 들어 있습니다. AI는 직접 먹어본 적이 없으니 이런 디테일을 만들기 어렵습니다.",
    },
    {
        "kind": "compare",
        "tag": "#자기소개",
        "title": "전학생의 자기소개",
        "prompt": "새 학기 첫날 자기소개입니다. AI가 쓴 쪽은 어디일까요?",
        "hint": "취미를 말할 때 '어느 정도로' 좋아하는지가 드러나는지 확인하세요.",
        "options": [
            {"label": "A", "text": "안녕하세요! 저는 밝고 긍정적인 성격을 가진 학생입니다. 취미는 독서와 운동이며, 새로운 친구들과 즐겁게 지내고 싶습니다. 앞으로 잘 부탁드립니다!", "is_ai": True},
            {"label": "B", "text": "안녕 난 김도윤. 농구 좋아하는데 키가 안 커서 슛만 연습해. 쉬는 시간에 체육관 가면 보통 나 있음. 같이 할 사람 말 걸어줘.", "is_ai": False},
        ],
        "note": "A의 '밝고 긍정적인 성격', '독서와 운동'은 누구에게나 붙일 수 있는 말입니다. B는 '키가 안 커서 슛만 연습해'처럼 그 사람만의 사정이 있어서 사람 글로 보입니다.",
    },
    {
        "kind": "judge",
        "tag": "#사진",
        "title": "이 사진, 진짜일까?",
        "prompt": "AI가 만든 사진일까요, 사람이 찍은 사진일까요?",
        "image": "images/q4.png",
        "is_ai": True,
        "hint": "손가락 개수, 글자, 귀걸이 짝, 배경의 선이 이어지는지 확인하세요.",
        "note": "AI 생성 이미지입니다. 생성 AI는 손가락 개수, 간판 글자, 액세서리 짝 맞추기, 배경 직선 연결에서 자주 실수합니다. 피부와 조명이 너무 매끈한 것도 단서입니다.",
    },
    {
        "kind": "compare",
        "tag": "#사과문",
        "title": "지각했을 때 선생님께 보낸 메시지",
        "prompt": "지각한 학생이 담임 선생님께 보낸 메시지입니다. AI의 도움을 받아 쓴 쪽은?",
        "hint": "이유가 구체적인지, 아니면 '불가피한 사정'처럼 뭉뚱그려져 있는지 보세요.",
        "options": [
            {"label": "A", "text": "선생님 죄송합니다. 부득이한 사정으로 인해 등교가 늦어지게 되었습니다. 앞으로는 보다 철저히 시간 관리를 하여 같은 일이 반복되지 않도록 노력하겠습니다.", "is_ai": True},
            {"label": "B", "text": "선생님 죄송해요 버스 놓쳐서 다음 거 기다리다가 늦었어요... 지금 교문 들어왔습니다 ㅠㅠ", "is_ai": False},
        ],
        "note": "A는 '부득이한 사정', '철저히 시간 관리'처럼 어떤 상황에도 쓸 수 있는 문장입니다. B처럼 '버스를 놓쳤다'는 진짜 이유가 들어가면 사람이 쓴 글일 가능성이 큽니다.",
    },
    {
        "kind": "judge",
        "tag": "#문제풀이",
        "title": "수학 문제 설명",
        "prompt": "친구에게 받은 설명입니다. AI가 썼을까요?",
        "content": "이 문제는 일차방정식의 활용 문제입니다. 먼저 구하고자 하는 값을 x로 놓습니다. 다음으로 문제의 조건을 식으로 표현합니다. 마지막으로 양변을 정리하여 x의 값을 구합니다. 따라서 답은 12입니다. 추가로 궁금한 점이 있으면 말씀해 주세요!",
        "is_ai": True,
        "hint": "마지막 문장을 소리 내어 읽어 보세요. 친구가 할 말투인가요?",
        "note": "AI가 쓴 글입니다. '먼저 / 다음으로 / 마지막으로'처럼 단계가 완벽하게 나뉘고, '궁금한 점이 있으면 말씀해 주세요'처럼 친구 사이에 안 쓰는 상담원 말투로 끝납니다.",
    },
    {
        "kind": "compare",
        "tag": "#그림",
        "title": "두 장의 그림",
        "prompt": "같은 주제로 그린 두 그림입니다. AI가 만든 그림은 어느 쪽일까요?",
        "hint": "선의 떨림, 지우개 흔적, 종이 질감이 보이는지 살펴보세요.",
        "options": [
            {"label": "A", "image": "images/q7_a.png", "is_ai": True},
            {"label": "B", "image": "images/q7_b.png", "is_ai": False},
        ],
        "note": "사람 그림에는 선이 흔들린 자리, 덧칠, 지우개 흔적 같은 '실수의 흔적'이 남습니다. AI 그림은 번쩍이는 완성도에 비해 디테일을 확대하면 구조가 어긋나 있는 경우가 많습니다.",
    },
    {
        "kind": "judge",
        "tag": "#역함정",
        "title": "어느 날의 일기",
        "prompt": "글이 어딘가 어색합니다. 그렇다면 AI가 쓴 걸까요?",
        "content": "오늘은 비가 왔다. 우산이 없어서 뛰었다. 신발이 젖었다. 기분이 나빴는데 집에 오니 엄마가 부침개를 했다. 그래서 괜찮아졌다. 비 오는 날은 부침개 냄새가 나는 날이다.",
        "is_ai": False,
        "hint": "어색한 글이라고 꼭 AI는 아닙니다. 마지막 문장이 왜 나왔는지 생각해 보세요.",
        "note": "사람이 쓴 글입니다. 문장이 짧고 투박하다고 AI는 아닙니다. 마지막 문장처럼 '내 경험에서 나온 나만의 결론'은 AI가 흉내내기 어려운 부분입니다. 글이 매끄러운지가 아니라 겪은 사람의 흔적이 있는지를 봐야 합니다.",
    },
    {
        "kind": "compare",
        "tag": "#댓글",
        "title": "유튜브 영상 댓글",
        "prompt": "같은 영상에 달린 댓글 두 개입니다. AI가 쓴 댓글은?",
        "hint": "영상을 실제로 본 사람만 쓸 수 있는 내용이 있는지 찾아보세요.",
        "options": [
            {"label": "A", "text": "정말 유익한 영상이네요! 설명이 체계적이고 이해하기 쉬워서 큰 도움이 되었습니다. 앞으로도 좋은 콘텐츠 기대하겠습니다.", "is_ai": True},
            {"label": "B", "text": "4분 12초에 나온 거 우리 학교 과학실에서 해봤는데 물이 안 올라갔음... 컵이 작아야 되는 건가요", "is_ai": False},
        ],
        "note": "A는 어떤 영상에도 복사해서 붙일 수 있는 칭찬입니다. B는 '4분 12초', '과학실', '실패한 결과'처럼 영상을 본 사람만 쓸 수 있는 내용입니다.",
    },
    {
        "kind": "judge",
        "tag": "#AI의변장",
        "title": "중학생 말투로 쓴 글",
        "prompt": "줄임말과 이모지가 가득합니다. 사람이 쓴 걸까요?",
        "content": "ㅇㅈ 이번 체육대회 진짜 꿀잼이었음 ㅋㅋ 우리 반 계주 1등하고 다들 완전 신나서 소리질렀는데 그 순간이 정말 소중한 추억으로 남을 것 같아 앞으로도 우리 반 파이팅!! 😊✨",
        "is_ai": True,
        "hint": "글의 앞부분 말투와 뒷부분 말투가 같은지 비교해 보세요.",
        "note": "AI가 중학생 말투를 흉내낸 글입니다. 앞은 'ㅇㅈ, 꿀잼, ㅋㅋ'인데 뒤는 '소중한 추억으로 남을 것 같아, 우리 반 파이팅'으로 갑자기 반성문 말투가 됩니다. 이런 말투 끊김과 과한 이모지가 AI의 변장을 들키게 하는 단서입니다.",
    },
]

# =====================================================================
# 3) 스타일
# =====================================================================
CSS = """
<style>
@import url("https://cdn.jsdelivr.net/gh/orioncactus/pretendard@v1.3.9/dist/web/static/pretendard.css");

#MainMenu, footer, header { visibility: hidden; }

html, body, [class*="css"], .stApp {
  font-family: Pretendard, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}
.stApp { background: __BG__; }
.block-container { padding-top: 2.0rem; padding-bottom: 3rem; max-width: 820px; }

/* 공통 카드 */
.tt-card {
  background: __SURFACE__;
  border: 1px solid __LINE__;
  border-radius: __RADIUS__;
  padding: 26px 28px;
  margin-bottom: 16px;
}

/* 표지 */
.tt-hero {
  background: __PRIMARY__;
  border-radius: __RADIUS__;
  padding: 34px 30px 30px 30px;
  margin-bottom: 18px;
  color: #FFFFFF;
}
.tt-bubble {
  display: inline-block;
  background: #FFFFFF;
  color: __PRIMARY__;
  font-weight: 700;
  font-size: 15px;
  padding: 9px 16px;
  border-radius: 16px 16px 16px 4px;
  margin-bottom: 14px;
}
.tt-hero h1 { color: #FFFFFF; font-size: 34px; font-weight: 800; margin: 0 0 8px 0; line-height: 1.25; }
.tt-hero p  { color: rgba(255,255,255,0.88); font-size: 15px; margin: 0; }
.tt-tags { margin-top: 18px; }
.tt-tag {
  display: inline-block;
  background: rgba(255,255,255,0.18);
  color: #FFFFFF;
  font-size: 13px; font-weight: 600;
  padding: 6px 12px; border-radius: 999px; margin-right: 6px;
}

/* 숫자 배지 */
.tt-badge {
  display: inline-flex; align-items: center; justify-content: center;
  width: 36px; height: 36px; border-radius: 50%;
  background: __PRIMARY__; color: #FFFFFF;
  font-weight: 800; font-size: 16px;
  margin-right: 12px;
}
.tt-qhead { display: flex; align-items: center; margin-bottom: 6px; }
.tt-chip {
  display: inline-block; background: __ACCENT_SOFT__; color: #0C7D6D;
  font-size: 12px; font-weight: 700; padding: 5px 11px; border-radius: 999px;
}
.tt-qtitle { color: __INK__; font-size: 23px; font-weight: 800; margin: 10px 0 6px 0; }
.tt-qprompt { color: __INK_SOFT__; font-size: 15px; line-height: 1.6; margin: 0; }

/* 말풍선 보기 */
.tt-opt {
  background: __BG__;
  border: 1px solid __LINE__;
  border-radius: 18px 18px 18px 6px;
  padding: 18px 18px;
  color: __INK__; font-size: 15px; line-height: 1.7;
  min-height: 150px;
}
.tt-optlabel {
  display: inline-block; background: __PRIMARY_SOFT__; color: __PRIMARY__;
  font-weight: 800; font-size: 13px; padding: 4px 11px;
  border-radius: 999px; margin-bottom: 10px;
}
.tt-single {
  background: __BG__; border: 1px solid __LINE__;
  border-left: 5px solid __ACCENT__;
  border-radius: 6px 18px 18px 18px;
  padding: 20px 22px; color: __INK__; font-size: 16px; line-height: 1.8;
}

/* 진행 표시 */
.tt-steps { margin: 0 0 14px 2px; }
.tt-dot {
  display: inline-block; width: 11px; height: 11px; border-radius: 50%;
  background: __LINE__; margin-right: 6px;
}
.tt-dot.done { background: __ACCENT__; }
.tt-dot.now  { background: __PRIMARY__; transform: scale(1.35); }
.tt-steptext { color: __INK_SOFT__; font-size: 13px; font-weight: 600; margin-left: 6px; }

/* 정답 피드백 */
.tt-feed { border-radius: __RADIUS__; padding: 22px 24px; margin-bottom: 14px; }
.tt-feed.ok { background: #E9F8F1; border: 1px solid #BCE8D5; }
.tt-feed.no { background: #FEEDF1; border: 1px solid #FACBD6; }
.tt-feed h4 { margin: 0 0 8px 0; font-size: 19px; font-weight: 800; }
.tt-feed.ok h4 { color: __GOOD__; }
.tt-feed.no h4 { color: __BAD__; }
.tt-feed p { margin: 0; color: __INK__; font-size: 15px; line-height: 1.7; }
.tt-answerline { font-size: 14px; font-weight: 700; color: __INK_SOFT__; margin-bottom: 10px; }

/* 결과 */
.tt-gauge-wrap { display: flex; align-items: center; gap: 24px; }
.tt-gauge {
  width: 130px; height: 130px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  flex: 0 0 auto;
}
.tt-gauge-in {
  width: 100px; height: 100px; border-radius: 50%;
  background: __SURFACE__;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.tt-gauge-num { font-size: 30px; font-weight: 800; color: __INK__; line-height: 1; }
.tt-gauge-lab { font-size: 12px; color: __INK_SOFT__; margin-top: 4px; }
.tt-grade { font-size: 25px; font-weight: 800; color: __INK__; margin: 0 0 6px 0; }
.tt-gradedesc { font-size: 15px; color: __INK_SOFT__; line-height: 1.6; margin: 0; }

.tt-row {
  display: flex; align-items: center; gap: 12px;
  padding: 12px 4px; border-bottom: 1px solid __LINE__;
}
.tt-row:last-child { border-bottom: none; }
.tt-mark { font-weight: 800; font-size: 15px; width: 22px; flex: 0 0 auto; }
.tt-mark.ok { color: __GOOD__; }
.tt-mark.no { color: __BAD__; }
.tt-rowtitle { color: __INK__; font-size: 15px; font-weight: 600; flex: 1 1 auto; }
.tt-rowtag { color: __INK_SOFT__; font-size: 12px; font-weight: 600; }

.tt-sectitle { color: __INK__; font-size: 19px; font-weight: 800; margin: 0 0 14px 0; }
.tt-note { color: __INK_SOFT__; font-size: 14px; line-height: 1.7; margin: 0 0 10px 0; }
.tt-note b { color: __INK__; }

/* 버튼 */
.stButton > button {
  border-radius: 14px;
  border: 1px solid __LINE__;
  background: __SURFACE__;
  color: __INK__;
  font-weight: 700;
  font-size: 15px;
  padding: 12px 16px;
  transition: none;
}
.stButton > button:hover {
  border-color: __PRIMARY__;
  color: __PRIMARY__;
  background: __PRIMARY_SOFT__;
}
div[data-testid="stVerticalBlock"] div.tt-primary + div .stButton > button,
.tt-primary-btn .stButton > button {
  background: __PRIMARY__; color: #FFFFFF; border-color: __PRIMARY__;
}
.stTextInput > div > div > input {
  border-radius: 12px; border: 1px solid __LINE__;
}
div[data-testid="stImage"] img { border-radius: 14px; border: 1px solid __LINE__; }
</style>
"""


def inject_css():
    css = CSS
    for key, value in THEME.items():
        css = css.replace("__" + key + "__", value)
    st.markdown(css, unsafe_allow_html=True)


def html(markup):
    st.markdown(markup, unsafe_allow_html=True)


# =====================================================================
# 4) 상태
# =====================================================================
def init_state():
    ss = st.session_state
    ss.setdefault("stage", "intro")
    ss.setdefault("order", list(range(len(QUESTIONS))))
    ss.setdefault("idx", 0)
    ss.setdefault("answers", {})
    ss.setdefault("checked", {})
    ss.setdefault("team", "")


def reset_all():
    for key in ["stage", "order", "idx", "answers", "checked"]:
        if key in st.session_state:
            del st.session_state[key]
    init_state()


def show_media(opt_or_q, caption=None):
    path = opt_or_q.get("image")
    if path and os.path.exists(path):
        st.image(path, use_container_width=True, caption=caption)
    else:
        html(
            "<div class='tt-opt' style='display:flex;align-items:center;"
            "justify-content:center;text-align:center;color:" + THEME["INK_SOFT"] + ";'>"
            "이미지 준비 안내<br><span style='font-size:13px'>" + str(path) + "</span></div>"
        )


# =====================================================================
# 5) 화면 - 시작
# =====================================================================
def screen_intro():
    tags = "".join(["<span class='tt-tag'>" + t + "</span>" for t in TAGS])
    html(
        "<div class='tt-hero'>"
        "<div class='tt-bubble'>내가 사람일까, AI일까?</div>"
        "<h1>" + TITLE + "</h1>"
        "<p>" + SUBTITLE + "</p>"
        "<div class='tt-tags'>" + tags + "</div>"
        "</div>"
    )

    html(
        "<div class='tt-card'>"
        "<div class='tt-qhead'><span class='tt-badge'>?</span>"
        "<span class='tt-chip'>#튜링테스트</span></div>"
        "<div class='tt-qtitle'>사람인지 AI인지, 구별할 수 있을까?</div>"
        "<p class='tt-qprompt'>1950년 수학자 앨런 튜링은 이런 질문을 했어요. "
        "<b>'대화만 해 보고 상대가 기계인지 사람인지 알 수 없다면, 그 기계는 생각한다고 말할 수 있을까?'</b><br><br>"
        "오늘은 그 질문을 우리가 직접 해 봅니다. 문자 답장, 글, 사진, 그림 "
        "총 " + str(len(QUESTIONS)) + "개를 보고 어느 쪽이 AI인지 골라 보세요. "
        "중요한 건 점수가 아니라 <b>'왜 그렇게 생각했는지'</b>예요.</p>"
        "</div>"
    )

    st.text_input("모둠 이름 또는 내 이름", key="team", placeholder="예) 1모둠 탐정단")
    shuffle = st.checkbox("문제 순서 섞기", value=False)

    html("<div class='tt-primary-btn'>")
    if st.button("도전 시작하기", use_container_width=True, key="start"):
        order = list(range(len(QUESTIONS)))
        if shuffle:
            random.shuffle(order)
        st.session_state.order = order
        st.session_state.idx = 0
        st.session_state.answers = {}
        st.session_state.checked = {}
        st.session_state.stage = "quiz"
        st.rerun()
    html("</div>")


# =====================================================================
# 6) 화면 - 문제
# =====================================================================
def steps_html(current, total):
    dots = ""
    for i in range(total):
        cls = "tt-dot"
        if i < current:
            cls += " done"
        elif i == current:
            cls += " now"
        dots += "<span class='" + cls + "'></span>"
    return (
        "<div class='tt-steps'>" + dots +
        "<span class='tt-steptext'>" + str(current + 1) + " / " + str(total) + "</span></div>"
    )


def screen_quiz():
    ss = st.session_state
    total = len(ss.order)
    pos = ss.idx
    qid = ss.order[pos]
    q = QUESTIONS[qid]
    answered = qid in ss.checked

    html(steps_html(pos, total))
    html(
        "<div class='tt-card'>"
        "<div class='tt-qhead'><span class='tt-badge'>" + str(pos + 1) + "</span>"
        "<span class='tt-chip'>" + q["tag"] + "</span></div>"
        "<div class='tt-qtitle'>" + q["title"] + "</div>"
        "<p class='tt-qprompt'>" + q["prompt"] + "</p>"
        "</div>"
    )

    if not answered:
        with st.expander("힌트 보기"):
            st.write(q["hint"])

    if q["kind"] == "compare":
        cols = st.columns(2, gap="medium")
        for i, opt in enumerate(q["options"]):
            with cols[i]:
                html("<span class='tt-optlabel'>" + opt["label"] + "</span>")
                if "image" in opt:
                    show_media(opt)
                else:
                    html("<div class='tt-opt'>" + opt["text"] + "</div>")
                st.write("")
                if st.button(
                    opt["label"] + "가 AI예요",
                    key="pick_" + str(qid) + "_" + str(i),
                    use_container_width=True,
                    disabled=answered,
                ):
                    ss.answers[qid] = i
                    ss.checked[qid] = (opt["is_ai"] is True)
                    st.rerun()
    else:
        if "image" in q:
            show_media(q)
        else:
            html("<div class='tt-single'>" + q["content"] + "</div>")
        st.write("")
        cols = st.columns(2, gap="medium")
        choices = [("ai", "AI가 만들었어요"), ("human", "사람이 만들었어요")]
        for i, (val, label) in enumerate(choices):
            with cols[i]:
                if st.button(
                    label,
                    key="judge_" + str(qid) + "_" + val,
                    use_container_width=True,
                    disabled=answered,
                ):
                    ss.answers[qid] = val
                    ss.checked[qid] = ((val == "ai") == bool(q["is_ai"]))
                    st.rerun()

    if answered:
        correct = ss.checked[qid]
        if q["kind"] == "compare":
            ai_label = [o["label"] for o in q["options"] if o["is_ai"]][0]
            answer_text = "정답: " + ai_label + "가 AI가 만든 것"
        else:
            answer_text = "정답: " + ("AI가 만든 것" if q["is_ai"] else "사람이 만든 것")

        cls = "ok" if correct else "no"
        head = "맞혔어요!" if correct else "아쉬워요!"
        html(
            "<div class='tt-feed " + cls + "'>"
            "<h4>" + head + "</h4>"
            "<div class='tt-answerline'>" + answer_text + "</div>"
            "<p>" + q["note"] + "</p>"
            "</div>"
        )
        html("<div class='tt-primary-btn'>")
        last = (pos == total - 1)
        if st.button("결과 보기" if last else "다음 문제", use_container_width=True, key="next_" + str(qid)):
            if last:
                ss.stage = "result"
            else:
                ss.idx += 1
            st.rerun()
        html("</div>")


# =====================================================================
# 7) 화면 - 결과
# =====================================================================
GRADES = [
    (90, "AI 탐정 1급", "사람과 AI의 차이를 아주 정확하게 잡아냈어요. 어떤 단서를 봤는지 친구들에게 설명해 주세요."),
    (70, "AI 탐정 2급", "꽤 잘 구별했어요. 틀린 문제의 단서를 다시 읽어 보면 거의 완벽해질 거예요."),
    (50, "관찰 중인 탐정", "절반 정도 맞혔어요. 글이 매끄러운지보다 '겪은 사람의 흔적'이 있는지 보세요."),
    (0, "AI에게 속은 탐정", "괜찮아요! 어려운 게 당연합니다. 이게 바로 튜링 테스트가 지금 중요한 이유예요."),
]


def screen_result():
    ss = st.session_state
    total = len(QUESTIONS)
    score = sum(1 for v in ss.checked.values() if v)
    pct = int(round(score / total * 100)) if total else 0
    grade, desc = next((g, d) for cut, g, d in GRADES if pct >= cut)

    who = ss.get("team") or "우리 모둠"
    html(
        "<div class='tt-hero'>"
        "<div class='tt-bubble'>" + who + "의 결과</div>"
        "<h1>" + str(score) + "문제 정답!</h1>"
        "<p>총 " + str(total) + "문제 중 " + str(score) + "개를 맞혔어요. 정답률 " + str(pct) + "%</p>"
        "</div>"
    )

    gauge_style = (
        "background: conic-gradient(" + THEME["PRIMARY"] + " 0% " + str(pct) + "%, "
        + THEME["LINE"] + " " + str(pct) + "% 100%);"
    )
    html(
        "<div class='tt-card'><div class='tt-gauge-wrap'>"
        "<div class='tt-gauge' style='" + gauge_style + "'>"
        "<div class='tt-gauge-in'>"
        "<div class='tt-gauge-num'>" + str(pct) + "%</div>"
        "<div class='tt-gauge-lab'>정답률</div>"
        "</div></div>"
        "<div><p class='tt-grade'>" + grade + "</p>"
        "<p class='tt-gradedesc'>" + desc + "</p></div>"
        "</div></div>"
    )

    rows = ""
    for pos, qid in enumerate(ss.order):
        q = QUESTIONS[qid]
        ok = ss.checked.get(qid)
        mark = "O" if ok else ("X" if qid in ss.checked else "-")
        cls = "ok" if ok else "no"
        rows += (
            "<div class='tt-row'>"
            "<span class='tt-mark " + cls + "'>" + mark + "</span>"
            "<span class='tt-rowtitle'>" + str(pos + 1) + ". " + q["title"] + "</span>"
            "<span class='tt-rowtag'>" + q["tag"] + "</span>"
            "</div>"
        )
    html("<div class='tt-card'><p class='tt-sectitle'>문제별 결과</p>" + rows + "</div>")

    clues = ""
    for pos, qid in enumerate(ss.order):
        q = QUESTIONS[qid]
        clues += "<p class='tt-note'><b>" + str(pos + 1) + ". " + q["title"] + "</b><br>" + q["note"] + "</p>"
    with st.expander("단서 모아보기 (복습용)"):
        html(clues)

    talks = [
        "AI가 쓴 글에서 가장 먼저 눈치챈 특징은 무엇이었나요?",
        "사람이 쓴 글인데 AI라고 착각한 문제가 있었나요? 왜 헷갈렸을까요?",
        "앞으로 AI가 더 발전하면 우리가 구별할 수 있을까요? 구별이 안 되면 어떤 문제가 생길까요?",
        "AI가 만든 것을 꼭 표시해야 하는 상황은 언제일까요? 반 친구들과 규칙을 정해 봅시다.",
    ]
    cards = ""
    for i, t in enumerate(talks, start=1):
        cards += (
            "<div class='tt-row'>"
            "<span class='tt-badge' style='width:28px;height:28px;font-size:13px;'>" + str(i) + "</span>"
            "<span class='tt-rowtitle'>" + t + "</span></div>"
        )
    html("<div class='tt-card'><p class='tt-sectitle'>이야기 나눠 봐요</p>" + cards + "</div>")

    col1, col2 = st.columns(2, gap="medium")
    with col1:
        if st.button("다시 도전하기", use_container_width=True, key="again"):
            reset_all()
            st.session_state.stage = "quiz"
            st.rerun()
    with col2:
        if st.button("처음 화면으로", use_container_width=True, key="home"):
            reset_all()
            st.rerun()


# =====================================================================
# 8) 사이드바 (교사용)
# =====================================================================
def sidebar():
    ss = st.session_state
    with st.sidebar:
        html("<p class='tt-sectitle'>수업 도구</p>")
        done = len(ss.get("checked", {}))
        score = sum(1 for v in ss.get("checked", {}).values() if v)
        st.write("풀어본 문제: " + str(done) + " / " + str(len(QUESTIONS)))
        st.write("현재 점수: " + str(score) + "점")
        st.divider()
        if st.checkbox("교사용 정답지 보기"):
            lines = []
            for i, q in enumerate(QUESTIONS, start=1):
                if q["kind"] == "compare":
                    ans = [o["label"] for o in q["options"] if o["is_ai"]][0] + " (AI)"
                else:
                    ans = "AI" if q["is_ai"] else "사람"
                lines.append(str(i) + ". " + q["title"] + " → " + ans)
            st.text("\n".join(lines))
        st.divider()
        if st.button("처음으로 돌아가기", use_container_width=True, key="sb_home"):
            reset_all()
            st.rerun()
        st.caption("이미지 문항은 app.py 옆 images 폴더에 q4.png, q7_a.png, q7_b.png를 넣어 주세요.")


# =====================================================================
# 9) 실행
# =====================================================================
def main():
    st.set_page_config(page_title=TITLE, page_icon="\U0001F50D", layout="centered")
    init_state()
    inject_css()
    sidebar()
    stage = st.session_state.stage
    if stage == "intro":
        screen_intro()
    elif stage == "quiz":
        screen_quiz()
    else:
        screen_result()


if __name__ == "__main__":
    main()

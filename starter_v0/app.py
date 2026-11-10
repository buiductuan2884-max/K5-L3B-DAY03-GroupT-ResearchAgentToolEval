"""Streamlit UI for the research agent.

Run from starter_v0/:  streamlit run app.py
Reuses chat.py's tool loop and transcript format, so UI chats are saved to
transcripts/*.transcript.json exactly like `python chat.py`.
"""
from __future__ import annotations

import sys
from datetime import datetime
from typing import Any

import streamlit as st

from chat import (
    ARTIFACTS_DIR,
    ROOT,
    json_text,
    now_iso,
    run_model_tool_loop,
    safe_slug,
    trim_history,
    write_transcript,
)
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

# chat.py prints emoji progress lines; Windows' cp1252 console would crash the turn.
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROVIDERS = ["openai", "openrouter", "anthropic", "gemini", "ollama"]
SYSTEM_PROMPT_PATH = ARTIFACTS_DIR / "system_prompt.md"
TOOLS_PATH = ARTIFACTS_DIR / "tools.yaml"
HISTORY_WINDOW = 5
MAX_TOOL_ROUNDS = 4

st.set_page_config(page_title="GroupT Research Agent", page_icon="🔎", layout="wide")

# One small style layer on top of .streamlit/config.toml: tight type, sharp corners, tool cards.
st.markdown("""
<style>
.block-container {max-width: 980px; padding-top: 2rem;}
h1 {font-size: 1.9rem !important; letter-spacing: -0.02em; margin-bottom: 0 !important;}
.gt-sub {color:#5F5D55; font-size:0.95rem; margin:.25rem 0 1rem;}
.gt-meta {display:flex; flex-wrap:wrap; gap:.5rem; margin-bottom:1.25rem;}
.gt-chip {font:500 0.78rem ui-monospace,SFMono-Regular,Consolas,monospace; padding:.2rem .55rem;
  border:1px solid #D9D7CE; border-radius:4px; background:#fff; color:#3A3934;}
.gt-tool {font:600 0.8rem ui-monospace,SFMono-Regular,Consolas,monospace; color:#0F766E;}
.gt-tool.err {color:#B42318;}
[data-testid="stExpander"] details {border-radius:6px; border-color:#E3E1D8; background:#fff;}
[data-testid="stExpander"] summary:hover {color:#0F766E;}
.stButton button {border-radius:6px; transition:transform .12s ease, border-color .12s ease;}
.stButton button:hover {transform:translateY(-1px); border-color:#0F766E;}
.stButton button:active {transform:translateY(0);}
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("Cấu hình")
    provider_name = st.selectbox("Provider", PROVIDERS, index=0)
    version = st.text_input("Version label", value="v2")
    model = st.text_input("Model (để trống = mặc định)", value="").strip() or None
    if st.button("Cuộc chat mới"):
        st.session_state.clear()
        st.rerun()


def new_session() -> None:
    provider = make_provider(provider_name)
    av = build_artifact_version(version, SYSTEM_PROMPT_PATH, TOOLS_PATH)
    transcript_id = "_".join([safe_slug(version), safe_slug(provider_name), "ui",
                              datetime.now().strftime("%Y%m%dT%H%M%S%f")])
    st.session_state.update(
        provider=provider,
        system_prompt=SYSTEM_PROMPT_PATH.read_text(encoding="utf-8"),
        tools=to_openai_tools(load_tool_declarations(TOOLS_PATH)),
        history=[],
        turns_view=[],
        transcript_path=ROOT / "transcripts" / f"{transcript_id}.transcript.json",
        transcript={
            "transcript_id": transcript_id,
            **artifact_version_dict(av),
            "provider": provider_name,
            "model": model or getattr(provider, "default_model", None),
            "system_prompt": str(SYSTEM_PROMPT_PATH),
            "tools": str(TOOLS_PATH),
            "history_window": HISTORY_WINDOW,
            "max_tool_rounds": MAX_TOOL_ROUNDS,
            "source": "streamlit_ui",
            "created_at": now_iso(),
            "updated_at": now_iso(),
            "turns": [],
        },
    )


def is_tool_error(result: Any) -> bool:
    return isinstance(result, dict) and bool(result.get("error"))


def show_tool_events(rounds: list[dict[str, Any]]) -> None:
    for rnd in rounds:
        for event in rnd.get("tool_results", []):
            failed = is_tool_error(event.get("result"))
            mark = "✗" if failed else "✓"
            with st.expander(f"{mark} {event['tool']} · round {rnd['round']}", expanded=failed):
                st.caption("Arguments")
                st.code(json_text(event.get("args", {})), language="json")
                st.caption("Kết quả")
                st.code(json_text(event.get("result", {}), max_chars=6000), language="json")


if "transcript" not in st.session_state:
    try:
        new_session()
    except Exception as exc:  # missing key / SDK: show it instead of a blank page
        st.error(f"Không khởi tạo được provider: {type(exc).__name__}: {exc}")
        st.stop()

st.title("Research Agent của GroupT")
st.markdown(f'<p class="gt-sub">Hỏi về tweet, tin web, bài báo arXiv hay policy công ty. Agent tự chọn trong '
            f'{len(st.session_state.tools)} tool, và mọi lần gọi tool hiện ngay dưới câu trả lời.</p>',
            unsafe_allow_html=True)
t = st.session_state.transcript
st.markdown('<div class="gt-meta">' + "".join(
    f'<span class="gt-chip">{label}</span>' for label in (
        t["artifact_version"], f"{t['provider']} · {t['model'] or 'default'}",
        st.session_state.transcript_path.name)) + "</div>", unsafe_allow_html=True)

EXAMPLES = ["Tin AI mới nhất hôm nay", "Tóm tắt 5 tweet mới nhất của một tài khoản",
            "Đọc giúp mình bài báo này"]
if not st.session_state.turns_view:
    cols = st.columns(len(EXAMPLES))
    for col, ex in zip(cols, EXAMPLES):
        if col.button(ex, use_container_width=True):
            st.session_state.pending = ex
            st.rerun()

for turn in st.session_state.turns_view:
    with st.chat_message("user"):
        st.markdown(turn["user"])
    with st.chat_message("assistant"):
        show_tool_events(turn["rounds"])
        if turn["status"] == "provider_error":
            st.error(turn["text"])
        else:
            st.markdown(turn["text"])

user_text = st.chat_input("Hỏi agent: tweet, tin web, đọc link, paper, policy…") or st.session_state.pop("pending", None)
if user_text:
    s = st.session_state
    turn_record: dict[str, Any] = {
        "turn_index": len(s.transcript["turns"]) + 1,
        "started_at": now_iso(),
        "user": user_text,
        "status": "started",
        "assistant_text": None,
        "rounds": [],
        "tool_events": [],
    }
    messages = [{"role": "system", "content": s.system_prompt},
                *trim_history(s.history, HISTORY_WINDOW),
                {"role": "user", "content": user_text}]
    with st.spinner("Agent đang chọn tool và chạy…"):
        try:
            result = run_model_tool_loop(provider=s.provider, messages=messages, tools=s.tools,
                                         model=model, max_tool_rounds=MAX_TOOL_ROUNDS)
            turn_record.update(result)
            s.history += [{"role": "user", "content": user_text},
                          {"role": "assistant", "content": result["assistant_text"]}]
            view_text = result["assistant_text"]
        except Exception as exc:
            # Keep tool/provider errors visible (rubric: UI must not hide tool errors).
            turn_record.update(status="provider_error", error=f"{type(exc).__name__}: {exc}")
            view_text = turn_record["error"]
    turn_record["ended_at"] = now_iso()
    s.transcript["turns"].append(turn_record)
    write_transcript(s.transcript_path, s.transcript)
    s.turns_view.append({"user": user_text, "text": view_text,
                         "status": turn_record["status"], "rounds": turn_record.get("rounds", [])})
    st.rerun()

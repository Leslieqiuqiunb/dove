import streamlit as st

# ── 核心加解密函数 ──
def caesar(text: str, key: int) -> str:
    """每个字符的 Unicode 码位 + key（模整个 Unicode 范围）"""
    result = ""
    for char in text:
        code = (ord(char) + key) % 1114112
        result += chr(code)
    return result


# ── 页面配置 ──
st.set_page_config(
    page_title="Caesar 加解密工具",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="expanded",
)


# ── 标题与说明 ──
st.title("Caesar 加解密工具")
st.caption("支持中文、表情、任意字符｜加密与解密使用**相同**的正整数密钥即可")

with st.expander("使用说明", expanded=True):
    st.markdown("""
    - 加密：原文每个字符的码位 + 密钥  
    - 解密：密文每个字符的码位 - 密钥  
    - 密钥建议：3～13 之间比较常用（太大太小都容易猜到）  
    - 支持：中文、英文、Emoji、符号、空格、换行等
    """)


# ── 输入区域 ──
col1, col2 = st.columns([5, 2])

with col1:
    input_text = st.text_area(
        "要处理的文本",
        height=180,
        placeholder="在这里粘贴或输入文字...\n例如：Hello 世界！ 你好呀😊",
        key="input_text"
    )

with col2:
    key = st.number_input(
        "密钥（正整数）",
        min_value=0,
        max_value=1000,
        value=3,
        step=1,
        help="解密时使用相同的数字，程序会自动减去"
    )


# ── 操作按钮 ──
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("加密 →", type="primary", use_container_width=True):
        if input_text.strip():
            result = caesar(input_text, int(key))
            st.session_state["result"] = result
            st.session_state["mode"] = "加密"
        else:
            st.warning("请输入文本内容")

with c2:
    if st.button("← 解密", type="primary", use_container_width=True):
        if input_text.strip():
            result = caesar(input_text, -int(key))
            st.session_state["result"] = result
            st.session_state["mode"] = "解密"
        else:
            st.warning("请输入文本内容")

with c3:
    if st.button("清空", use_container_width=True):
        st.session_state.pop("result", None)
        st.session_state.pop("mode", None)
        st.rerun()


# ── 结果显示区 ──
if "result" in st.session_state:
    st.divider()
    mode = st.session_state.get("mode", "处理")
    st.subheader(f"**{mode}结果**")

    st.code(st.session_state["result"], language=None)

    # 复制与下载按钮
    col_copy, col_down = st.columns(2)

    with col_copy:
        st.button(
            "📋 一键复制",
            on_click=lambda: st.session_state.update({"copied": True}),
            use_container_width=True
        )

    with col_down:
        st.download_button(
            label="⬇️ 下载为 txt",
            data=st.session_state["result"],
            file_name=f"caesar_{mode.lower()}_result.txt",
            mime="text/plain",
            use_container_width=True
        )

    if st.session_state.get("copied", False):
        st.success("已复制到剪贴板！")
        st.session_state["copied"] = False

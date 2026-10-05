import streamlit as st

from agentic_rag.graph import graph

st.set_page_config(page_title="Diabetes Health Info Assistant", page_icon="🩺")

st.title("🩺 Diabetes & Prediabetes Info Assistant")
st.caption("An agentic RAG system answering questions from real CDC content, with built-in safety guardrails.")

question = st.text_input("Ask a question about diabetes or prediabetes:")

if st.button("Ask") and question:
    with st.spinner("Thinking..."):
        result = graph.invoke({"question": question})

    verdict = result.get("safety_verdict")

    if verdict == "allow":
        st.success("✅ Question allowed")
    else:
        st.warning(f"⚠️ Declined: {verdict}")

    col1, col2 = st.columns(2)
    col1.metric("Audience", result.get("audience", "n/a"))
    col2.metric("Topic mode", result.get("topic_mode", "n/a"))

    st.markdown("### Answer")
    st.markdown(result.get("answer"))

    chunks = result.get("retrieved_chunks", [])
    if chunks:
        with st.expander(f"📄 Retrieved {len(chunks)} source chunks"):
            for c in chunks:
                st.markdown(f"**{c.metadata.get('doc_id')}** — {c.metadata.get('Header 2')}")
                st.caption(c.page_content[:200] + "...")
                st.divider()
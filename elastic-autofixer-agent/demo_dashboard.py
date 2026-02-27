import streamlit as st
import requests
import pandas as pd
import time
import json

# Configuration
API_URL = "http://127.0.0.1:8000/api/v1"

st.set_page_config(page_title="Elastic Auto-Fixer Agent", page_icon="🛠️", layout="wide")

# Header
st.title("🛠️ Elastic Auto-Fixer Agent")
st.markdown("### Autonomous SRE for Elastic Cloud Serverless")

# Sidebar
st.sidebar.header("Agent Controls")
if st.sidebar.button("🔍 Scan Cluster"):
    with st.spinner("Scanning cluster for inefficiencies..."):
        try:
            resp = requests.get(f"{API_URL}/diagnose")
            st.session_state['issues'] = resp.json()
            st.sidebar.success(f"Found {len(st.session_state['issues'])} issues.")
        except Exception as e:
            st.sidebar.error(f"Connection Failed: {e}")

# Main Area
if 'issues' not in st.session_state:
    st.info("👈 Click 'Scan Cluster' to begin diagnostics.")
else:
    issues = st.session_state['issues']
    
    if not issues:
        st.success("✅ Cluster is healthy! No issues found.")
    
    for i, issue in enumerate(issues):
        with st.expander(f"⚠️ {issue['severity'].upper()}: {issue['issue_id']} ({issue['category']})", expanded=True):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {issue['description']}")
                st.markdown(f"**Resource:** `{issue['affected_resource']}`")
                st.json(issue['metrics'])
            
            with col2:
                st.markdown("### Actions")
                if st.button(f"🪄 Fix with AI", key=f"btn_{i}"):
                    st.session_state[f'fix_{i}'] = True

            # If Fix button clicked
            if st.session_state.get(f'fix_{i}'):
                with st.spinner("Consulting LLM & ESRE..."):
                    try:
                        # Call Generate Fix API
                        fix_resp = requests.post(f"{API_URL}/generate-fix", json=issue)
                        proposal = fix_resp.json()
                        
                        st.markdown("---")
                        st.subheader("💡 AI Fix Proposal")
                        st.info(proposal['explanation'])
                        
                        # Diff View
                        c1, c2 = st.columns(2)
                        with c1:
                            st.caption("🔴 Original Config")
                            st.code(json.dumps(proposal['original_code'], indent=2), language='json')
                        with c2:
                            st.caption("🟢 Optimized Config")
                            st.code(json.dumps(proposal['fixed_code'], indent=2), language='json')
                        
                        # Apply Button
                        if st.button(f"🚀 Apply Fix to Cluster", key=f"apply_{i}"):
                            with st.spinner("Applying & Benchmarking..."):
                                apply_resp = requests.post(f"{API_URL}/apply-fix", json=proposal)
                                if apply_resp.status_code == 200:
                                    st.success(f"✅ Success: {apply_resp.json()['message']}")
                                    time.sleep(2)
                                    st.rerun()
                                else:
                                    st.error("Failed to apply fix.")
                                    
                    except Exception as e:
                        st.error(f"Error: {e}")
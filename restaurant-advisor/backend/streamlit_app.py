import streamlit as st
from decision_tree import Node, root

def init_session_state():
    if 'current_node' not in st.session_state:
        st.session_state.current_node = root
        st.session_state.path = []
        st.session_state.level = 1

def main():
    st.set_page_config(
        page_title="Restaurant Decision Helper",
        layout="centered"
    )
    
    init_session_state()
    
    # Header
    st.title("Restaurant Decision Assisstant")
    st.write("Let's help you decide whether to wait or leave!")
    
    # Progress bar
    progress = st.progress(st.session_state.level / 6)  # 6 is max depth
    
    # Show decision path
    if st.session_state.path:
        with st.expander("Your choices so far"):
            for choice in st.session_state.path:
                st.write(f"-> {choice}")
    
    current = st.session_state.current_node
    
    # Display result or question
    if current.result:
        if "Wait" in current.result:
            st.success(f"🕒 {current.result}")
        else:
            st.warning(f"🚶‍♂️ {current.result}")
            
        if st.button("Start Over", type="primary"):
            st.session_state.current_node = root
            st.session_state.path = []
            st.session_state.level = 1
            st.rerun()
            
    else:
        st.write("### " + current.question)
        
        # Create columns for options
        cols = st.columns(len(current.options))
        
        # Display options as buttons
        for idx, option in enumerate(current.options):
            with cols[idx]:
                if st.button(option, key=f"btn_{option}", use_container_width=True):
                    # Update path
                    st.session_state.path.append(f"{current.question}: {option}")
                    # Move to next node
                    st.session_state.current_node = current.children[option]
                    # Update level
                    st.session_state.level += 1
                    # Rerun to update UI
                    st.rerun()

if __name__ == "__main__":
    main()
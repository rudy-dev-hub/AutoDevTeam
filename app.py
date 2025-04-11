import streamlit as st
from crew.crew_setup import AutoDevCrew
import time
import json
from pathlib import Path
import os

st.set_page_config(
    page_title="AutoDev Team",
    page_icon="🤖",
    layout="wide"
)

def init_session_state():
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'current_task' not in st.session_state:
        st.session_state.current_task = None
    if 'generated_files' not in st.session_state:
        st.session_state.generated_files = []
    if 'current_agent' not in st.session_state:
        st.session_state.current_agent = None
    if 'task_in_progress' not in st.session_state:
        st.session_state.task_in_progress = False

def save_generated_file(content: str, filename: str, language: str = None, section: str = None):
    """Save a generated file and return its path"""
    # Create outputs directory if it doesn't exist
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)
    
    # Create the file path
    file_path = output_dir / filename
    
    # Save the content
    with open(file_path, "w") as f:
        f.write(content)
    
    return str(file_path)

def extract_code_blocks(text: str) -> list:
    """Extract code blocks from text"""
    code_blocks = []
    lines = text.split('\n')
    current_block = []
    in_code_block = False
    current_language = None
    current_section = None
    
    for line in lines:
        # Check for section headers
        if line.strip().endswith(':'):
            section = line.strip()[:-1].upper()
            if section in ['IMPLEMENTATION', 'TESTS', 'SUGGESTED IMPROVEMENTS']:
                current_section = section
                continue
        
        if line.strip().startswith('```'):
            if in_code_block:
                if current_block:
                    code_blocks.append({
                        'language': current_language or 'python',
                        'code': '\n'.join(current_block),
                        'section': current_section
                    })
                current_block = []
                current_language = None
            else:
                # Extract language from ```python or similar
                lang = line.strip()[3:].strip()
                if lang:
                    current_language = lang
            in_code_block = not in_code_block
        elif in_code_block:
            current_block.append(line)
    
    if current_block:
        code_blocks.append({
            'language': current_language or 'python',
            'code': '\n'.join(current_block),
            'section': current_section
        })
    
    return code_blocks

def display_chat():
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown("👤 **You:**")
        elif message["role"] == "agent":
            st.markdown(f"🤖 **{message['agent']}:**")
        else:
            st.markdown("🤖 **Assistant:**")
        st.markdown(message["content"])
        st.markdown("---")

def handle_task_submission():
    if st.session_state.current_task and not st.session_state.task_in_progress:
        st.session_state.task_in_progress = True
        
        def progress_callback(agent_name: str, message: str):
            # Add message to the chat
            st.session_state.messages.append({
                "role": "agent",
                "agent": agent_name,
                "content": message
            })
            # Update current agent
            st.session_state.current_agent = agent_name
            # Force a rerun to show the update
            st.rerun()

        # Create progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Add user task to chat
        st.session_state.messages.append({
            "role": "user",
            "content": st.session_state.current_task
        })
        
        try:
            # Update progress bar for each agent
            agents = ["Software Architect", "Senior Python Developer", "Code Reviewer", "Test Engineer"]
            for i, agent in enumerate(agents):
                status_text.text(f"🔄 {agent} is working...")
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.5)  # Small delay to show progress
            
            # Execute the task
            crew = AutoDevCrew(progress_callback=progress_callback)
            result = crew.run(st.session_state.current_task)
            
            # Complete the progress
            progress_bar.progress(100)
            status_text.text("✅ Task completed!")
            
            # Add final result to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Task completed! Here's the final result:\n\n{result}"
            })
            
            # Extract and save code blocks
            code_blocks = extract_code_blocks(result)
            for i, block in enumerate(code_blocks):
                if block['code'].strip():
                    # Determine file extension based on content and language
                    ext = ".py"  # default to Python
                    if "import pytest" in block['code']:
                        ext = "_test.py"
                    elif "import streamlit" in block['code']:
                        ext = "_app.py"
                    elif block['language'] and block['language'] != 'python':
                        ext = f".{block['language']}"
                    
                    # Determine filename based on section
                    section = block.get('section', '')
                    if section == 'IMPLEMENTATION':
                        filename = f"implementation_{i+1}{ext}"
                    elif section == 'TESTS':
                        filename = f"tests_{i+1}{ext}"
                    elif section == 'SUGGESTED IMPROVEMENTS':
                        filename = f"improvements_{i+1}{ext}"
                    else:
                        filename = f"generated_code_{i+1}{ext}"
                    
                    file_path = save_generated_file(block['code'], filename, block['language'], section)
                    if file_path not in st.session_state.generated_files:
                        st.session_state.generated_files.append(file_path)
            
            # Save the full result
            full_result_path = save_generated_file(result, "full_result.txt")
            if full_result_path not in st.session_state.generated_files:
                st.session_state.generated_files.append(full_result_path)
            
        except Exception as e:
            progress_bar.progress(100)
            status_text.text("❌ Error occurred!")
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"❌ Error: {str(e)}"
            })
        finally:
            st.session_state.task_in_progress = False
            st.session_state.current_agent = None

def main():
    st.title("🤖 AutoDev Team")
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.header("Generated Files")
        if not st.session_state.generated_files:
            st.info("No files generated yet. Submit a task to generate files.")
        else:
            for file_path in st.session_state.generated_files:
                try:
                    with open(file_path, 'r') as f:
                        content = f.read()
                        filename = Path(file_path).name
                        st.download_button(
                            f"📥 Download {filename}",
                            content,
                            file_name=filename,
                            key=f"download_{filename}"
                        )
                        # Show file preview
                        with st.expander(f"Preview {filename}"):
                            st.code(content, language="python" if filename.endswith('.py') else "text")
                except Exception as e:
                    st.error(f"Error loading {file_path}: {str(e)}")
        
        if st.session_state.current_agent:
            st.header("Current Status")
            st.info(f"🔄 {st.session_state.current_agent} is working...")
    
    # Main chat interface
    st.header("Task Input")
    
    task_input = st.text_area("Enter your task here:", key="task_input")
    if st.button("Submit Task", disabled=st.session_state.task_in_progress):
        st.session_state.current_task = task_input
        handle_task_submission()
    
    # Display chat history
    st.header("Task Progress")
    display_chat()

if __name__ == "__main__":
    main() 
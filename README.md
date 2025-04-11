# Auto Dev Team

An AI-powered development team using CrewAI to automate software development tasks. The system uses a team of AI agents working together to plan, implement, review, and test code based on user requirements.

## Features

- 🤖 AI-powered development team with specialized agents:
  - Software Architect: Plans and breaks down tasks
  - Senior Python Developer: Implements code
  - Code Reviewer: Reviews and suggests improvements
  - Test Engineer: Creates comprehensive test suites

- 🎯 Task Processing:
  - Automatic task breakdown and planning
  - Clean, documented code implementation
  - Code review with improvement suggestions
  - Comprehensive test suite generation

- 🖥️ User Interface:
  - Streamlit-based web interface
  - Real-time progress tracking
  - Code block extraction and display
  - File saving capabilities

## Setup

1. Clone the repository:
```bash
git clone <your-repo-url>
cd auto-dev-team
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the root directory with:
```
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. Open your browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter your task in the text input field and click "Submit Task"

4. The AI team will:
   - Break down the task into steps
   - Implement the solution
   - Review the code
   - Generate tests

5. The results will be displayed in the UI and saved to the `outputs` directory

## Project Structure

```
auto-dev-team/
├── app.py              # Streamlit application
├── main.py            # Entry point
├── requirements.txt   # Dependencies
├── crew/
│   └── crew_setup.py  # CrewAI implementation
└── engine/
    └── llm_wrapper.py # LLM configuration
```

## Dependencies

- crewai==0.1.32
- streamlit
- python-dotenv
- openai

## Contributing

Feel free to submit issues and enhancement requests!

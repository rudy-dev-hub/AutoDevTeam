from crewai import Agent, Task, Crew
from typing import List, Callable, Optional
from engine.llm_wrapper import llm

class AutoDevCrew:
    def __init__(self, progress_callback: Optional[Callable[[str, str], None]] = None):
        self.progress_callback = progress_callback
        
        # Initialize agents with specific roles and goals
        self.planner = Agent(
            role='Software Architect',
            goal='Break down complex tasks into clear, actionable steps',
            backstory="""You are an experienced software architect with a track record of 
            breaking down complex projects into manageable tasks. You excel at identifying 
            dependencies and potential challenges.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        self.coder = Agent(
            role='Senior Python Developer',
            goal='Write clean, efficient, and well-documented Python code',
            backstory="""You are a senior Python developer with expertise in writing 
            production-ready code. You follow best practices and ensure code quality.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        self.reviewer = Agent(
            role='Code Reviewer',
            goal='Ensure code quality and identify potential issues',
            backstory="""You are a meticulous code reviewer with years of experience in 
            Python development. You have a keen eye for detail and best practices.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

        self.tester = Agent(
            role='Test Engineer',
            goal='Create comprehensive test suites for Python code',
            backstory="""You are an expert in Python testing, specializing in pytest. 
            You ensure code reliability through thorough testing.""",
            verbose=True,
            allow_delegation=False,
            llm=llm
        )

    def _update_progress(self, agent_name: str, message: str):
        """Update progress through callback if available"""
        if self.progress_callback:
            self.progress_callback(agent_name, message)

    def create_tasks(self, user_task: str) -> List[Task]:
        # Create tasks for each agent
        planning_task = Task(
            description=f"""Analyze the following task and break it down into clear, 
            actionable steps: {user_task}
            
            Provide a detailed plan with 5-7 steps, focusing on technical implementation details.
            Each step should be complete and actionable.
            
            Format your response as:
            PLAN:
            [Your detailed plan here]
            
            IMPLEMENTATION:
            ```python
            [Your implementation code here]
            ```
            
            TESTS:
            ```python
            [Your test code here]
            ```""",
            agent=self.planner,
            callback=lambda task_output: self._update_progress("Software Architect", task_output)
        )

        coding_task = Task(
            description=f"""Based on the plan provided, write Python code to accomplish 
            the following task: {user_task}
            
            Include:
            - All necessary imports
            - Error handling
            - Documentation
            - Type hints where appropriate
            
            Format your response as:
            IMPLEMENTATION:
            ```python
            [Your implementation code here]
            ```
            
            EXPLANATION:
            [Your explanation of the code here]""",
            agent=self.coder,
            callback=lambda task_output: self._update_progress("Senior Python Developer", task_output)
        )

        review_task = Task(
            description="""Review the generated code and provide feedback on:
            - Code quality
            - Best practices
            - Potential improvements
            - Security concerns
            
            Be thorough and specific in your review.
            
            Format your response as:
            REVIEW:
            [Your detailed review here]
            
            SUGGESTED IMPROVEMENTS:
            ```python
            [Your improved code here if any]
            ```""",
            agent=self.reviewer,
            callback=lambda task_output: self._update_progress("Code Reviewer", task_output)
        )

        testing_task = Task(
            description="""Create comprehensive unit tests for the generated code using pytest.
            Include:
            - Edge cases
            - Error scenarios
            - Input validation
            - Expected outputs
            
            Ensure high test coverage.
            
            Format your response as:
            TESTS:
            ```python
            [Your test code here]
            ```
            
            TEST EXPLANATION:
            [Your explanation of the tests here]""",
            agent=self.tester,
            callback=lambda task_output: self._update_progress("Test Engineer", task_output)
        )

        return [planning_task, coding_task, review_task, testing_task]

    def run(self, user_task: str):
        # Create tasks
        tasks = self.create_tasks(user_task)

        # Create and run the crew
        crew = Crew(
            agents=[self.planner, self.coder, self.reviewer, self.tester],
            tasks=tasks,
            verbose=2
        )

        # Execute the crew's tasks
        results = []
        for task in tasks:
            result = task.execute()
            results.append(result)

        # Combine all results
        combined_result = "\n\n".join(results)
        return combined_result 
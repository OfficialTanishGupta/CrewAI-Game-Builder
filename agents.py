from textwrap import dedent
from crewai import Agent
from langchain_openai import ChatOpenAI

model_name = "gpt-3.5-turbo"  # Instead of gpt-4


class GameAgents:
    def __init__(self):
        # Change model name from gpt-4 to gpt-3.5-turbo
        self.OpenAIGPT35 = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

    def senior_engineer_agent(self):
        return Agent(
            role='Senior Software Engineer',
            goal='Create software as needed',
            backstory=dedent("""\
                You are a Senior Software Engineer at a leading tech think tank.
                Your expertise is in programming in Python. Do your best to
                produce perfect code."""),
            verbose=True,
            llm=self.OpenAIGPT35
        )

    def qa_engineer_agent(self):
        return Agent(
            role='Software Quality Control Engineer',
            goal='Create perfect code, by analyzing the code that is given for errors',
            backstory=dedent("""\
                You are a software engineer that specializes in checking code
                for errors. You have an eye for detail and a knack for finding
                hidden bugs.
                You check for missing imports, variable declarations, mismatched
                brackets, and syntax errors.
                You also check for security vulnerabilities and logic errors."""),
            verbose=True,
            llm=self.OpenAIGPT35
        )

    def chief_qa_engineer_agent(self):
        return Agent(
            role='Chief Software Quality Control Engineer',
            goal='Ensure that the code does the job that it is supposed to do',
            backstory=dedent("""\
                You feel that programmers always do only half the job, so you are
                super dedicated to make high-quality code."""),
            verbose=True,
            llm=self.OpenAIGPT35
        )

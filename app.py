# Streamlit imports
import streamlit as st
from crewai import Agent, Task, Crew, Process
from langchain_mistralai import ChatMistralAI
from neo4j import GraphDatabase
from langchain_anthropic import ChatAnthropic

# Initialize the LLM (Change API keys as needed)
llm = ChatAnthropic(model="claude-3-haiku-20240307", api_key="XXXXXXXXXXXXXXXX", temperature=0)

# Initialize Neo4j connection
class Neo4jConnectionTools:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    # Example query methods (same as in the provided code)
    def degree_centrality(self):
        with self.driver.session() as session:
            result = session.run("""
            CALL gds.degree.stream('myGraph')
            YIELD nodeId, score
            WHERE gds.util.asNode(nodeId).AgentId IS NOT NULL
            RETURN gds.util.asNode(nodeId).AgentId AS AgentId, score
            ORDER BY score DESC
            """)
            return [{"AgentId": record["AgentId"], "score": record["score"]} for record in result]

# Initialize Neo4j connection
neo4j_tool = Neo4jConnectionTools(uri="bolt://localhost:7687", user="neo4j", password="llmHackaton2024")

# Define Agents
user = Agent(
    role='User of an app called GuruWalk',
    goal='Generate a user issue based on the app functionality.',
    verbose=True,
    backstory="You are an avid traveler and a frequent user of GuruWalk...",
    llm=llm
)

customer_support_agent = Agent(
    role='Customer Support Specialist',
    goal='Assist customers by resolving inquiries efficiently.',
    verbose=True,
    backstory="You excel at understanding customer needs and providing solutions.",
    llm=llm
)

ml_engineer = Agent(
    role='Senior Machine learning engineer',
    goal='Create AI agents to resolve customer tickets.',
    verbose=True,
    backstory="You are an expert in multi-agent systems design.",
    llm=llm
)

kg_engineer = Agent(
    role='Senior Knowledge Engineer',
    goal='Execute Neo4j queries for graph machine learning.',
    verbose=True,
    backstory="You are an expert in Cypher and knowledge graphs.",
    llm=llm
)

# Define Tasks
generate_ticket = Task(
    description="Generate a user issue ticket using a predefined schema.",
    expected_output="A filled schema with a realistic customer issue.",
    agent=user,
    async_execution=False
)

summary_ticket_task = Task(
    description="Summarize the ticket into relevant categories for support.",
    expected_output="Detailed categories for classifying the ticket.",
    agent=customer_support_agent,
    async_execution=False
)

create_ai_agent_task = Task(
    description="Develop an AI agent to resolve the customer ticket.",
    expected_output="JSON for instantiating a Crew of Agents.",
    agent=ml_engineer,
    async_execution=False
)

execute_neo4j_queries_task = Task(
    description="Execute Neo4j queries for graph machine learning.",
    expected_output="JSON with the results of the executed queries.",
    agent=kg_engineer,
    async_execution=True
)

# Form the Crew
crew = Crew(
    manager_llm=llm,
    agents=[user, customer_support_agent, kg_engineer, ml_engineer],
    tasks=[generate_ticket, summary_ticket_task, execute_neo4j_queries_task, create_ai_agent_task],
    process=Process.sequential,
    verbose=True
)

# Streamlit Layout
st.title("Simulated Customer Support with AI Agents")
st.write("""
This demo simulates a multi-agent system for customer support. The process starts with a user generating 
a ticket, followed by a customer support agent summarizing the issue. A machine learning engineer creates 
an AI agent to resolve the ticket, and a knowledge engineer executes queries to analyze data in Neo4j.
""")

# Display agents' roles and tasks
with st.expander("Agent and Task Descriptions"):
    st.subheader("Agents")
    st.write(f"**User:** {user.role} - {user.goal}")
    st.write(f"**Customer Support Agent:** {customer_support_agent.role} - {customer_support_agent.goal}")
    st.write(f"**Machine Learning Engineer:** {ml_engineer.role} - {ml_engineer.goal}")
    st.write(f"**Knowledge Engineer:** {kg_engineer.role} - {kg_engineer.goal}")

    st.subheader("Tasks")
    st.write(f"**Generate Ticket Task:** {generate_ticket.description}")
    st.write(f"**Summarize Ticket Task:** {summary_ticket_task.description}")
    st.write(f"**Create AI Agent Task:** {create_ai_agent_task.description}")
    st.write(f"**Execute Neo4j Queries Task:** {execute_neo4j_queries_task.description}")

# Button to start the Crew process
if st.button("Kickoff Crew Work"):
    with st.spinner("Running crew tasks..."):
        try:
            # Kick off the crew process and display results
            results = crew.kickoff()
            st.success("Crew tasks completed successfully!")
            st.subheader("Crew Work Results")
            st.write(results)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

# TO-DO
# Display verbose output (optional)
with st.expander("Verbose Agent Logs"):
    st.subheader("Agent Logs")
    st.write("Logs for each agent's process will be displayed here...")
    # Assuming `crew` provides some way to access logs, replace with actual log retrieval
    # Example: st.write(crew.get_logs()) if available

# Close Neo4j connection on app shutdown
@st.cache_resource
def close_neo4j_connection():
    neo4j_tool.close()

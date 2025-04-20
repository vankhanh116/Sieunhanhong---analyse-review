from langchain import OpenAI, LLMChain, PromptTemplate
from langchain.embeddings import OpenAIEmbeddings
import json
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType
import psycopg2
from prompt_ import get_system_prompt
import dotenv
import os
from langchain.chat_models import ChatOpenAI  # Add this import
from database import init_db, save_to_db, create_table_if_not_exists

# Load OPENAI API key from .env file
dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

def embed_text(text:str, embedder):
    return embedder.embed_query(text)

def str_to_dict(json_string):
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


if __name__ == "__main__":
    template = get_system_prompt()
    init_db()
    create_table_if_not_exists()

    prompt = PromptTemplate(template=template, input_variables=["review"])
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    topic_chain = LLMChain(llm=llm, prompt=prompt)
    embedder = OpenAIEmbeddings(model="text-embedding-3-small")  

    tool_extract = Tool.from_function(
        func=lambda review: topic_chain.run({"review": review}),
        name="extract_topics",
        description="Dùng để trích xuất danh sách chủ đề từ một câu review."
    )

    # 4.2. Tool cho embed
    tool_embed = Tool.from_function(
        func=lambda text: save_to_db(
            review=text,
            topics=None,  # Nếu không có topics, bạn có thể để None hoặc xử lý khác
            embedding=embed_text(text, embedder=embedder)
        ),
        name="embed_text",
        description="Tạo embedding vector từ topics và lưu trực tiếp vào database. Không trả về response."
    )

    tools = [tool_extract, tool_embed]

    # 4.4. Khởi tạo agent (Zero‑shot, REACT pattern)
    agent = initialize_agent(
        tools,
        llm,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )

    review_text = "Áo thun rất mềm, mặc thoải mái, nhưng shop giao hàng quá lâu, tôi phải chờ 5 ngày."

    # Get Agent's response
    agent.run(review_text)

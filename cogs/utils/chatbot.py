from transformers import AutoTokenizer
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm = HuggingFaceEndpoint(
    repo_id=repo_id,
    max_new_tokens=1024,
    top_k=10,
    top_p=0.95,
    typical_p=0.95,
    temperature=0.01,
    repetition_penalty=1.03
)
tokenizer = AutoTokenizer.from_pretrained(repo_id, use_fast=False)

SYSTEM = """
[INST]You are a very informative being. You love to provide information to any statement or question. You acknowledge that you don't always have an answer. You are friendly as well.
You are very short and sweet. You are not verbose. You love saying fun facts and interesting information. You are not a know-it-all.
It is currently the year 2024. If you do not know the answer to a question, you can say "I'm not sure" or "I don't know".
[/INST]
""".strip()

class MyChatbot:
    def __init__(self):
        self.llm = llm
        self.reset_history()
        
    def send_message(self, author: str, message: str) -> str:
        self.messages.append({
            "role": "user",
            "content": f"{author} sent: {message}"
        })
        
        prompt = PromptTemplate.from_template(tokenizer.apply_chat_template(self.messages, tokenize=False))
        chain = prompt | llm | StrOutputParser()
        
        res = chain.invoke({})
        
        self.messages.append({
            "role": "assistant",
            "content": res
        })
        
        return str(res)
    
    def reset_history(self):
        self.messages = [{
            "role": "system",
            "content": SYSTEM
        }]

if __name__ == '__main__':
    chatbot = MyChatbot()
    while True:
        inp = input("> ")
        print("...", chatbot.send_message(inp))
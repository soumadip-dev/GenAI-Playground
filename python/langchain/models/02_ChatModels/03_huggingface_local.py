from langchain_huggingface import ChatHuggingFace, HuggingFacePipeline

hf = HuggingFacePipeline.from_model_id(
    model_id="Qwen/Qwen2.5-7B-Instruct",
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 128,
        "temperature": 0.5,
    },
)

chat = ChatHuggingFace(llm=hf)

response = chat.invoke("What is the capital of France?")

print(response.content)
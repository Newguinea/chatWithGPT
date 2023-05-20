from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain import OpenAI
from langchain import PromptTemplate
from langchain.chains.summarize import load_summarize_chain

openai_api_key = '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'
llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
llm3 = ChatOpenAI(temperature=0,
                  openai_api_key=openai_api_key,
                  max_tokens=1000,
                  )

def getReplay(text, final_prompt="what is this story? do you think it is a good story?", compress_prompt="please compress the text and output key information"):
    text = compressText(text, compress_prompt, final_prompt)
    return finalPrompt(final_prompt, text)


def compressText(text, compress_prompt, final_prompt):
    condition = True
    while condition:
        # TODO 如果大于3000 token，拆解成10000字符长度，3000重合长度的段落
        text_splitter = RecursiveCharacterTextSplitter(separators=["\n\n", "\n", "\t"], chunk_size=10000,
                                                       chunk_overlap=3000)
        docs = text_splitter.create_documents([text])
        num_documents = len(docs)
        print(f"Now our book is split up into {num_documents} documents")
        selected_docs = docs

        map_prompt = compress_prompt + "\n" + "```{text}```"

        map_prompt_template = PromptTemplate(template=map_prompt, input_variables=["text"])
        map_chain = load_summarize_chain(llm=llm3,
                                         chain_type="stuff",
                                         prompt=map_prompt_template)
        selected_docs = [doc for doc in selected_docs]
        # Make an empty list to hold your summaries
        summary_list = []

        # Loop through a range of the lenght of your selected docs
        for i, doc in enumerate(selected_docs):
            # Go get a summary of the chunk
            chunk_summary = map_chain.run([doc])
            # Append that summary to your list
            summary_list.append(chunk_summary)

        summaries = "\n".join(summary_list)
        text = summaries
        if (llm.get_num_tokens(summaries + final_prompt) < 3800):
            condition = False
    print("its a for loop to reduce the text size")
    return text

def finalPrompt(final_prompt, text):
    llm = OpenAI(temperature=0, openai_api_key=openai_api_key)
    prompt = f"{final_prompt}\n```{{text}}```\ntext = {text}"
    output = llm(prompt)
    return output

# # 打开文件
# with open('The Little Prince.txt', 'r', encoding='utf-8') as file:
#     file_content = file.read()
#
# # 将文件内容传递给变量
# text = file_content
#
# compress_prompt = "there was a very long text ,Your goal is to give a summary of this section so that a\
# reader will have a full understanding of what happened.
# Your response should be at least three paragraphs and fully encompass what was said in the passage."
# final_prompt = "You will be given a series of summaries,
# Your goal is to give a verbose summary of what happened in the story.
# The reader should be able to grasp what happened in the text.
# "
#
# print(getReplay(text, final_prompt, compress_prompt))
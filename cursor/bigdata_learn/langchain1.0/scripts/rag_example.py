"""
LangChain 1.0 RAG 示例代码
"""
import os
from dotenv import load_dotenv

load_dotenv()


def create_rag_system():
    """
    创建完整的 RAG 系统
    """
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    
    # ==========================================
    # 1. 加载文档
    # ==========================================
    print("1. 加载文档...")
    
    # 获取数据文件路径
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "sample_docs.txt")
    
    loader = TextLoader(data_path, encoding="utf-8")
    documents = loader.load()
    print(f"   加载了 {len(documents)} 个文档")
    
    # ==========================================
    # 2. 分割文档
    # ==========================================
    print("2. 分割文档...")
    
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", ".", " ", ""]
    )
    chunks = splitter.split_documents(documents)
    print(f"   分割成 {len(chunks)} 个块")
    
    # ==========================================
    # 3. 创建向量库
    # ==========================================
    print("3. 创建向量库...")
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    print("   向量库创建完成")
    
    # 可选：保存向量库
    # vectorstore.save_local("faiss_index")
    
    # ==========================================
    # 4. 创建检索器
    # ==========================================
    print("4. 创建检索器...")
    
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 3}
    )
    
    # ==========================================
    # 5. 创建 RAG Chain
    # ==========================================
    print("5. 创建 RAG Chain...")
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
你是一个知识库问答助手。根据提供的上下文回答问题。
如果上下文中没有相关信息，请诚实地说"根据现有知识库，我无法回答这个问题"。

上下文：
{context}

问题：{question}

回答：
""")
    
    def format_docs(docs):
        """格式化检索到的文档"""
        return "\n\n---\n\n".join(doc.page_content for doc in docs)
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    print("   RAG Chain 创建完成")
    
    return rag_chain, retriever


def test_retrieval(retriever):
    """测试检索功能"""
    print("\n" + "=" * 50)
    print("检索测试")
    print("=" * 50)
    
    query = "什么是 LCEL？"
    print(f"\n查询: {query}")
    
    docs = retriever.invoke(query)
    print(f"检索到 {len(docs)} 个相关文档:")
    for i, doc in enumerate(docs, 1):
        print(f"\n--- 文档 {i} ---")
        print(doc.page_content[:200] + "...")


def test_rag_qa(rag_chain):
    """测试 RAG 问答"""
    print("\n" + "=" * 50)
    print("RAG 问答测试")
    print("=" * 50)
    
    questions = [
        "什么是 LangChain？",
        "LCEL 有什么优势？",
        "LangChain 支持哪些应用场景？",
        "如何学习 LangChain？",
        "量子计算的原理是什么？"  # 知识库中没有的问题
    ]
    
    for q in questions:
        print(f"\n问题: {q}")
        answer = rag_chain.invoke(q)
        print(f"回答: {answer}")


def test_streaming_rag(rag_chain):
    """测试流式 RAG"""
    print("\n" + "=" * 50)
    print("流式 RAG 测试")
    print("=" * 50)
    
    question = "详细介绍 LangChain 的 RAG 功能"
    print(f"\n问题: {question}")
    print("回答: ", end="")
    
    for chunk in rag_chain.stream(question):
        print(chunk, end="", flush=True)
    print()


def create_rag_with_source():
    """
    创建带来源引用的 RAG 系统
    """
    from langchain_openai import ChatOpenAI, OpenAIEmbeddings
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.vectorstores import FAISS
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    
    print("\n" + "=" * 50)
    print("带来源引用的 RAG")
    print("=" * 50)
    
    # 加载和处理文档
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, "..", "data", "sample_docs.txt")
    
    loader = TextLoader(data_path, encoding="utf-8")
    documents = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)
    
    # 添加元数据
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_id"] = i
        chunk.metadata["source"] = "sample_docs.txt"
    
    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
    
    prompt = ChatPromptTemplate.from_template("""
根据以下上下文回答问题：

{context}

问题：{question}
回答：
""")
    
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    def get_answer_with_source(question):
        """获取答案和来源"""
        docs = retriever.invoke(question)
        context = format_docs(docs)
        
        chain = prompt | llm | StrOutputParser()
        answer = chain.invoke({"context": context, "question": question})
        
        sources = [
            {
                "chunk_id": doc.metadata.get("chunk_id"),
                "source": doc.metadata.get("source"),
                "content_preview": doc.page_content[:100] + "..."
            }
            for doc in docs
        ]
        
        return {
            "answer": answer,
            "sources": sources
        }
    
    # 测试
    question = "LangChain 1.0 有哪些主要特性？"
    result = get_answer_with_source(question)
    
    print(f"\n问题: {question}")
    print(f"\n回答: {result['answer']}")
    print(f"\n来源 ({len(result['sources'])} 个文档):")
    for src in result["sources"]:
        print(f"  - Chunk {src['chunk_id']} from {src['source']}")


# ============================================
# 主函数
# ============================================
if __name__ == "__main__":
    print("=" * 50)
    print("LangChain 1.0 RAG 示例")
    print("=" * 50)
    
    # 检查 API Key
    if not os.getenv("OPENAI_API_KEY"):
        print("请设置 OPENAI_API_KEY 环境变量")
        exit(1)
    
    # 创建 RAG 系统
    rag_chain, retriever = create_rag_system()
    
    # 测试检索
    test_retrieval(retriever)
    
    # 测试问答
    test_rag_qa(rag_chain)
    
    # 测试流式输出
    test_streaming_rag(rag_chain)
    
    # 带来源的 RAG
    create_rag_with_source()
    
    print("\n" + "=" * 50)
    print("RAG 示例执行完成！")

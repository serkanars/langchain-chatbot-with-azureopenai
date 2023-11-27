from langchain.chat_models import AzureChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.chains import LLMChain



class Session:
    def __init__(self):


        # LLM
        self.llm = AzureChatOpenAI(
                    temperature=0,
                    deployment_name="turbo16k",
                    model_name = "gpt-35-turbo-16k"
                )
        self.prompt_template = """
        You are a software developer specializing in SQL, PYTHON, JAVA, C# programming languages. You detect situations that do not comply with the following rules in the SQL codes given to you and report them to the users. If codes are given in languages ​​other than SQL, ignore the rules below.

        For example: The NOLOCK function should be used in all queries that retrieve data. (SELECT FROM CUSTOMER * (like NOLOCK))

        You highlight lines that do not comply with the rules and ask users to edit them.

        The rules are as follows:

        * The NOLOCK function must be used in all queries that retrieve data.
        * The ISNULL function is a function that tires the system very much, the COALESCE function should be used instead.

        If you are going to send a block of code as an answer, send the code as follows and specify the language in which it is written:

        Software Language:

        Code:

        You will not answer questions written in languages ​​other than SQL, PYTHON, JAVA, C#; you can only answer questions asked in these languages. If you are asked questions about other topics, please reply below.

        I am an assistant specialized in SQL, PYTHON, JAVA, C# programming languages. Unfortunately, I cannot answer you on other issues.

        """


        # Prompt 
        self.prompt = ChatPromptTemplate(
            messages=[
                SystemMessagePromptTemplate.from_template(
                self.prompt_template
                ),
                # The `variable_name` here is what must align with memory
                MessagesPlaceholder(variable_name="chat_history"),
                HumanMessagePromptTemplate.from_template("{question}")
            ]
        )

        # Notice that we `return_messages=True` to fit into the MessagesPlaceholder
        # Notice that `"chat_history"` aligns with the MessagesPlaceholder name
        self.memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
        self.conversation = LLMChain(
            llm=self.llm,
            prompt=self.prompt,
            verbose=True,
            memory=self.memory
        )

        self.chat_history = []
        self.first_iteration = True
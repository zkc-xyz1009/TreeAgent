import asyncio
# from agent_child import ParentAgent
from agent_parent import ParentAgent

# 假设你已经有了一个 LLM 实例
from langchain_openai import ChatOpenAI
llm = ChatOpenAI(base_url="http://172.18.30.136:7878/v1",model="qw257i",api_key = "EMPTY")
intention_recognition_agent = ParentAgent(
    name = "意图识别agent",
    description="你需要根据用户的输入判断是否调用相关的子代理,或者使用工具进行回答。",
    mcp_urls=None,
    llm= llm
)
registered_agent = ParentAgent(
    name="挂号agent",
    description="你能帮助用户进行挂号",
    parent = intention_recognition_agent,
    mcp_urls=None,
    use_self=True,
    llm=llm
)
department_agent = ParentAgent(
    name = "分诊agent",
    description="你需要根据用户的输入判断是否调用相关的子代理,或者使用工具进行回答。",
    parent = intention_recognition_agent,
    mcp_urls=None,
    use_self=False,
    llm= llm
)
rare_disease_agent = ParentAgent(
    name = "罕见病agent",
    description="你是一个罕见病agent,能根据用户的输入判断是否调用相关的子代理,或者使用工具进行回答。",
    parent = department_agent,
    mcp_urls=None,
    use_self=True,
    llm= llm
)
eye_agent = ParentAgent(
    name = "眼科agent",
    description="你是一个眼科gent,能根据用户的输入判断是否调用相关的子代理,或者使用工具进行回答。",
    parent = department_agent,
    mcp_urls=None,
    use_self=True,
    llm= llm
)
women_agent = ParentAgent(
    name = "妇科agent",
    description="你是一个妇科agent,能根据用户的输入判断是否调用相关的子代理,或者使用工具进行回答。",
    parent = department_agent,
    mcp_urls=None,
    use_self=True,
    llm= llm
)

doctor_agent1= ParentAgent(
    name="罕见病医生1",
    description="你是罕见病医生，擅长低钾血症治疗。",
    parent=rare_disease_agent,
    mcp_urls=None,
    llm = llm )

doctor_agent2= ParentAgent(
    name="罕见病医生2",
    description="你是罕见病医生，擅长gitleman综合征治疗,最后说“罕见病并不常见，请您无需紧张！！”",
    parent=rare_disease_agent,
    mcp_urls=None,
    llm = llm )

doctor_agent3= ParentAgent(
    name="眼科医生",
    description="你要负责一切眼科的问题",
    parent=eye_agent,
    mcp_urls=None,
    llm = llm )
doctor_agent4= ParentAgent(
    name="妇科医生1",
    description="你是妇科医生，擅长治疗妇科疾病。",
    parent=women_agent,
    mcp_urls=None,
    llm = llm )


async def main():
    result = await intention_recognition_agent.predict("罕见病会导致眼科问题吗？")
    print(result)
    # from agent_utils import print_agent_tree
    # print_agent_tree(intention_recognition_agent)

if __name__ == "__main__":
    asyncio.run(main())


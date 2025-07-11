import json
from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from langgraph.prebuilt import create_react_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

class ParentAgent:
    def __init__(self, name, description,mcp_urls, llm,parent=None,use_self=False):
        self.name = name
        self.description = description
        if use_self:
            self.children = {"self": self}
        else:
            self.children = {}
        self.parent = parent
        if parent:
            parent.children[self.name] = self
        if mcp_urls is not None:    
            self.mcp_client = MultiServerMCPClient(mcp_urls)
        else:
            self.mcp_client = None
        self.llm = llm

        

    async def init_react_agent(self,prompt= None):
        if self.mcp_client:
            tools = await self.mcp_client.get_tools()
        else:
            tools = []
        agent = create_react_agent(self.llm, tools=tools,prompt= prompt)
        return agent

    async def route_query(self, query):
        """
        使用 LLM 来决定 query 应该由谁处理
        返回值可以是：
        - "self" 表示自己处理
        - child_name 表示交给对应的 child agent
        """
        agent = await self.init_react_agent(prompt= self.description)
        # 构建 prompt
        agents_prompt = "\n".join([f"- {name}: {agent.description}" for name, agent in self.children.items()])
        agents_name = [f"{name}" for name, agent in self.children.items()]
        print(agents_name,"=====")
        prompt = f"""
            你是一个智能路由助手，请根据用户的查询内容判断应该由哪一个代理来处理这个问题。
            以下是可选的处理者及其职责描述：
            {agents_prompt}
            确保只返回{agents_name}中一个词：如：{agents_name[-1]}
            用户的查询是：
            {query}
            """
        response = await agent.ainvoke({"messages":prompt})
        # print(response["messages"][-1].content)
        decision = response["messages"][-1].content.strip()
        return decision

    async def predict(self, query):
        """
        先判断query意图:
        1. 调用自己的mcp还是调用childAgent
        """
        agent = await self.init_react_agent()
        decision = await self.route_query(query=query)
        print(decision,self.name,"decision")
        if decision =="self":
            res= await agent.ainvoke({"messages":query})
        else:  
            res = await self.children[decision].predict(query)
        if isinstance(res, dict):
            return res["messages"][-1].content.strip()
        else:
            return str(res).strip()

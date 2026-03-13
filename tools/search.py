from langchain_community.tools import tool, DuckDuckGoSearchRun

ddg = DuckDuckGoSearchRun()

class Search:
    @tool
    def search_result(query: str):
        """Search the web for information"""
        return ddg.invoke(query)
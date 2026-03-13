from langchain_classic.agents import create_react_agent, AgentExecutor
from langchain_classic import hub
from services.llm_service import LLM
from tools.weather import Weather
from tools.trains import Trains
from tools.hotels import Hotels
from tools.flights import Flights


class Agent:

    def __init__(self):
        self.prompt = hub.pull("hwchase17/react")
        self.trains = Trains()
        self.flights = Flights()
        self.weather = Weather()
        self.hotels = Hotels()

        self.tools = [
            self.flights.get_flights,
            self.weather.weather,
            self.hotels.get_hotels,
            self.trains.get_trains,
        ]

    def agent_create(self):
        llm = LLM().get_llm()

        agent = create_react_agent(
            llm=llm,
            tools=self.tools,
            prompt=self.prompt
        )

        return agent

    def agent_execute(self):
        agent = self.agent_create()

        agent_executor = AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True
        )

        return agent_executor

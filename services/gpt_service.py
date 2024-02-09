from langchain_openai import ChatOpenAI
from langchain.output_parsers import PydanticOutputParser
from contract_manager.models import Contract
from langchain.prompts import ChatPromptTemplate, HumanMessagePromptTemplate
from contract_manager.secrets import openai_api_key


class GPTService:
    def __init__(self):
        self._init_model()
        self.parser = PydanticOutputParser(pydantic_object=Contract)
        self._init_prompt()

    def _init_model(self):
        self.model = ChatOpenAI(
            model="gpt-4",
            openai_api_key=openai_api_key,
            max_tokens=1000
        )

    def _init_prompt(self):
        self.prompt = ChatPromptTemplate(
            messages=[
                HumanMessagePromptTemplate.from_template(self._get_task_prompt())
            ],
            input_variables=["contract_data"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions(),
            },
        )

    @staticmethod
    def _get_task_prompt():
        return "Analyze the provided contracts data and extract key features in JSON format. Please, only in JSON format. \n{format_instructions}\n{contract_data}"

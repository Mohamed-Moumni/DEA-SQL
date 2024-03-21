from typing import List,Dict

class InfoIdentifier:
    def __init__(self, _model, _prompt_template:str) -> None:
        self.model = _model
        self.prompt_template = _prompt_template
    
    def start(self, questions:List[str]):
        entities:Dict[str, str] = {}
        for quest in questions:
            entities[quest] = self.model.generate_response(quest)
        return entities

from abc import ABC, abstractmethod
from typing import Any
from .types import BaseInputs, BaseOutputs



class BaseInfer(ABC):
    
    @abstractmethod
    def setup(self, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def infer(self, inputs: BaseInputs) -> BaseOutputs:
        pass

    def run_inference(self, inputs: BaseInputs) -> BaseOutputs:
        inputs.check()
        outputs = self.infer(inputs)
        outputs.check()
        return outputs

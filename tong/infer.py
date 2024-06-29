from abc import ABC, abstractmethod
from typing import Any
from .types import BaseInputs, BaseOutputs



class BaseInfer(ABC):
    def __init__(self) -> None:
        self.setup()
    
    @abstractmethod
    def setup(self) -> None:
        pass

    @abstractmethod
    def infer(self, inputs: BaseInputs) -> BaseOutputs:
        pass

    def run_inference(self, inputs: BaseInputs) -> BaseOutputs:
        inputs.check()
        outputs = self.infer(inputs)
        outputs.check()

        print("Inference complete!")
        return outputs

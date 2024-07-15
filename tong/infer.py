import psutil
import os
import signal

from abc import ABC, abstractmethod
from typing import Any
from .types import BaseInputs, BaseOutputs

def kill_children(parent_pid, sig=signal.SIGTERM):
    try:
        parent = psutil.Process(parent_pid)
    except psutil.NoSuchProcess:
        return
    children = parent.children(recursive=True)
    for child in children:
        child.send_signal(sig)

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
        kill_children(os.getpid())
        print("Inference complete!")

        return outputs

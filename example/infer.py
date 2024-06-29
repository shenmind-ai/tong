from tong import BaseInfer, BaseInputs, BaseOutputs, FileInput, StringInput, FloatInput, IntegerInput, FloatOutput, IntegerOutput, FloatOutputList, IntegerOutputList

import torch
from torchvision import models, transforms
from PIL import Image


class Inputs(BaseInputs):

    def __init__(self):
        self.image_path = FileInput(
                value = "image.jpg",
                description = "Path to the image file",
                min_size = 1 * 1024, # 1KB
                max_size = 10 * 1024 * 1024, # 10MB
                suffix = ["jpg", "jpeg", "png"],
                )

        self.threshold = FloatInput(
                value = 0.5,
                description = "Threshold for the model",
                min_value = 0.0,
                max_value = 1.0,
            )

class Outputs(BaseOutputs):
    def __init__(self):
        self.top3_labels = IntegerOutputList(
                description="Top 3 predicted class labels"
        )

        self.top3_class_confidences = FloatOutputList(
                description="Top 3 predicted class confidences"
            )

        self.label = IntegerOutput(
                description="Predicted class label"
            )

        self.confidence = FloatOutput(
                description="Predicted class confidence"
            )


class Infer(BaseInfer):
    def setup(self):
        """
        The code here will be executed when the inference service starts. 
        Typically, you can load the model here so that it can be used during inference.
        """

        self.model = models.resnet50(pretrained=True)



    def infer(self, inputs: Inputs) -> Outputs:

        img = Image.open(inputs.image_path.value)
        img = img.resize((224, 224))

        transform = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        img = transform(img)
        img = img.unsqueeze(0)

        outputs = self.model(img)

        # Get the class label and confidence
        class_label = torch.argmax(outputs).item()
        class_confidence = torch.max(outputs).item()

        if class_confidence < inputs.threshold.value:
            class_label = -1
            class_confidence = -1


        # Get the top 3 class labels and confidences
        top3_labels = torch.argsort(outputs, descending=True)[0].squeeze()[:3].tolist()
        top3_class_confidences = torch.sort(outputs, descending=True)[0].squeeze()[:3].tolist()


        return Outputs().set_values(
            top3_labels = top3_labels,
            top3_class_confidences = top3_class_confidences,
            label = class_label,
            confidence = class_confidence
        )

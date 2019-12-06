import torch
import torchvision
from torch import nn
from typing import Optional


class Flatten(nn.Module):
    "Flatten `x` to a single dimension, often used at the end of a model. `full` for rank-1 tensor"

    def __init__(self, full: bool = False):
        super().__init__()
        self.full = full

    def forward(self, x):
        return x.view(-1) if self.full else x.view(x.size(0), -1)


class AdaptiveConcatPool2d(nn.Module):
    "Layer that concats `AdaptiveAvgPool2d` and `AdaptiveMaxPool2d`."  # from pytorch

    def __init__(self, sz: Optional[int] = None):
        "Output will be 2*sz or 2 if sz is None"
        super().__init__()
        self.output_size = sz or 1
        self.ap = nn.AdaptiveAvgPool2d(self.output_size)
        self.mp = nn.AdaptiveMaxPool2d(self.output_size)

    def forward(self, x): return torch.cat([self.mp(x), self.ap(x)], 1)


def myhead(nf, nc):
    return \
        nn.Sequential(  # the dropout is needed otherwise you cannot load the weights
            AdaptiveConcatPool2d(),
            Flatten(),
            nn.BatchNorm1d(nf),
            nn.Dropout(p=0.25),
            nn.Linear(nf, 512),
            nn.ReLU(True),
            nn.BatchNorm1d(512),
            nn.Dropout(p=0.5),
            nn.Linear(512, nc),
        )


def init_model():
    my_model = torchvision.models.resnet34()
    modules = list(my_model.children())
    modules.pop(-1)
    modules.pop(-1)
    temp = nn.Sequential(nn.Sequential(*modules))
    tempchildren = list(temp.children())
    tempchildren.append(myhead(1024, 6))
    my_r101 = nn.Sequential(*tempchildren)

    model = my_r101
    weighties = torch.load('modelBefore.pth')
    model.load_state_dict(weighties['state_dict'])
    return model

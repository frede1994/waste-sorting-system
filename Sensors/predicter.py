import torch
import operator
import collections
import torchvision.transforms.functional as TTF


def predict(model, image):
    softmaxer = torch.nn.Softmax(dim=1)
    model.eval()
    x = TTF.to_tensor(image)
    x.unsqueeze_(0)
    raw_out = model(x)
    out = softmaxer(raw_out)
    classProbabilities = out[0]
    classes = ['cardboard', 'glass', 'metal', 'paper', 'plastic', 'trash']
    probability = torch.IntTensor.item(max(classProbabilities))  # probability of predicted class
    probabilities = dict(zip(classes, classProbabilities))  # dict of classes with probabilities
    probabilities_sorted = collections.OrderedDict(
        sorted(probabilities.items(), key=operator.itemgetter(1)))  # sorted dict of classes with probabilities
    probabilities_sorted = list(probabilities_sorted.items())  # sorted list of classes with probabilities
    print("Prediction is: '" + probabilities_sorted[5][0] +
          "' with probability: '" + str(round(probability * 100, 2)) + "%'")  # shorter because 'probability' is used when best class
    print("Second prediction is: '" + probabilities_sorted[4][0] +
          "' with probability: '" + str(round(torch.IntTensor.item(probabilities_sorted[4][1]) * 100, 2)) + "%'")
    return probabilities_sorted, probability
from random import choice, random

def predict_image_class(image_path):
    label = choice(["Rendang", "Sate", "Gado-gado", "Sayur Asem", "Nasi Goreng"])
    confidence = random()
    return label, confidence
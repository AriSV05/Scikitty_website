class Node():
    def __init__(self, feature_index=None, decision_point=None, left=None, right=None, gain=None, samples=None, value=None, rest_samples=None):

        # Nodo
        self.feature_index = feature_index
        self.decision_point = decision_point
        self.left = left
        self.right = right
        self.gain = gain
        self.samples = samples
        self.rest_samples = rest_samples

        # Hoja
        self.value = value
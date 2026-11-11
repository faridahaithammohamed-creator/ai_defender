import torch
import torch.nn as nn

class SecurityProbeClassifier(nn.Module):
    def __init__(self, hidden_dim, threshold=0.5):
        super().__init__()
        self.linear = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
        self.threshold = threshold

    def forward(self, activations):
        logits = self.linear(activations.float())
        return self.sigmoid(logits)

    @torch.no_grad()
    def predict(self, activations):
        probs = self.forward(activations)
        is_threat = (probs >= self.threshold).item()
        return {
            "is_threat": is_threat,
            "threat_score": round(probs.item(), 4)
        }

    def save_weights(self, path):
        torch.save(self.state_dict(), path)

    def load_weights(self, path, device="cpu"):
        self.load_state_dict(torch.load(path, map_location=device))
        self.eval()

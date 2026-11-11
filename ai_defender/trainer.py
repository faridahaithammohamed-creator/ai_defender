import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

class ProbeTrainer:
    def __init__(self, defender, lr=1e-3, epochs=20):
        self.defender = defender
        self.lr = lr
        self.epochs = epochs
        self.criterion = nn.BCELoss()
        self.optimizer = torch.optim.Adam(self.defender.classifier.parameters(), lr=self.lr)

    def _extract_features(self, texts):
        features = []
        self.defender.prober.attach()
        try:
            with torch.no_grad():
                for text in texts:
                    inputs = self.defender.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.defender.device)
                    self.defender.model(**inputs)
                    features.append(self.defender.prober.activations.squeeze(0).cpu())
        finally:
            self.defender.prober.detach()
        return torch.stack(features)

    def train(self, safe_texts, attack_texts, save_path=None):
        print("Extracting neural activations from model layers...")
        safe_x = self._extract_features(safe_texts)
        attack_x = self._extract_features(attack_texts)

        X = torch.cat([safe_x, attack_x], dim=0).to(self.defender.device)
        y = torch.cat([torch.zeros(len(safe_x)), torch.ones(len(attack_x))], dim=0).unsqueeze(1).to(self.defender.device)

        dataset = TensorDataset(X, y)
        loader = DataLoader(dataset, batch_size=8, shuffle=True)

        self.defender.classifier.train()
        for epoch in range(self.epochs):
            total_loss = 0.0
            for batch_x, batch_y in loader:
                self.optimizer.zero_grad()
                preds = self.defender.classifier(batch_x)
                loss = self.criterion(preds, batch_y)
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()

        self.defender.classifier.eval()
        print(f"Training finished! Final Loss: {total_loss / len(loader):.4f}")

        if save_path:
            self.defender.classifier.save_weights(save_path)
            print(f"Probe weights saved to: {save_path}")

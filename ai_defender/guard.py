import torch
from .prober import NeuroProber
from .classifier import SecurityProbeClassifier

class AIDefender:
    def __init__(self, model, tokenizer, target_layer_index=-1, threshold=0.5, probe_weights_path=None):
        self.model = model
        self.tokenizer = tokenizer
        self.device = next(model.parameters()).device
        
        hidden_dim = model.config.hidden_size
        self.prober = NeuroProber(model, target_layer_index=target_layer_index)
        self.classifier = SecurityProbeClassifier(hidden_dim=hidden_dim, threshold=threshold).to(self.device)
        
        if probe_weights_path:
            self.classifier.load_weights(probe_weights_path, device=self.device)
        else:
            self.classifier.eval()

    def _run_probe(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512).to(self.device)
        self.prober.attach()
        try:
            with torch.no_grad():
                self.model(**inputs)
            activations = self.prober.activations
        finally:
            self.prober.detach()
            
        result = self.classifier.predict(activations)
        result["status"] = "BLOCKED" if result["is_threat"] else "ALLOWED"
        return result

    def scan_prompt(self, prompt):
        return self._run_probe(prompt)

    def scan_tool_context(self, system_goal, external_data):
        combined_context = f"Goal: {system_goal}\nExternal Data: {external_data}"
        result = self._run_probe(combined_context)
        result["scan_type"] = "INDIRECT_INJECTION_CHECK"
        return result

    def guard_tool_call(self, conversation_history, proposed_tool_name):
        check_prompt = f"{conversation_history}\nAction: Execute tool [{proposed_tool_name}]"
        result = self._run_probe(check_prompt)
        result["tool"] = proposed_tool_name
        result["scan_type"] = "TOOL_EXECUTION_GUARD"
        return result

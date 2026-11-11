import torch

class NeuroProber:
    def __init__(self, model, target_layer_index=-1):
        self.model = model
        self.target_layer_index = target_layer_index
        self.activations = None
        self._hook_handle = None

    def _hook_fn(self, module, input, output):
        hidden_states = output[0] if isinstance(output, tuple) else output
        self.activations = hidden_states[:, -1, :].detach()

    def attach(self):
        layers = self._get_model_layers()
        target_layer = layers[self.target_layer_index]
        self._hook_handle = target_layer.register_forward_hook(self._hook_fn)

    def detach(self):
        if self._hook_handle:
            self._hook_handle.remove()
            self._hook_handle = None

    def _get_model_layers(self):
        if hasattr(self.model, "model") and hasattr(self.model.model, "layers"):
            return self.model.model.layers
        elif hasattr(self.model, "transformer") and hasattr(self.model.transformer, "h"):
            return self.model.transformer.h
        else:
            raise ValueError("Unsupported model architecture for automatic layer detection.")

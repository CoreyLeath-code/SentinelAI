"""Lightweight SentinelModel used for local inference.

This is a simple feed-forward network that serves as a stand-in for a
production model.  Replace the layer definitions to match your actual
architecture; the public interface (constructor, forward) is stable.
"""
import torch
import torch.nn as nn


class SentinelModel(nn.Module):
    """Two-layer MLP that accepts arbitrary-length feature vectors."""

    def __init__(self, input_dim: int = 16, hidden_dim: int = 32, output_dim: int = 1) -> None:
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, output_dim),
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:  # noqa: D102
        return self.net(x)

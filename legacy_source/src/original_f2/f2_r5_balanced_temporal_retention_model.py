from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Dict, Tuple

import torch
import torch.nn as nn
import torch.nn.functional as F


@dataclass(frozen=True)
class FrozenTrainingSpec:
    learning_rate: float = 3.0e-4
    weight_decay: float = 1.0e-4
    batch_size: int = 32
    grad_clip_max_norm: float = 1.0
    adam_beta1: float = 0.9
    adam_beta2: float = 0.999
    adam_eps: float = 1.0e-8
    warmup_epochs: int = 5
    warmup_start_factor: float = 0.1
    minimum_lr: float = 3.0e-6
    max_epochs: int = 100
    huber_delta: float = 1.0


SPEC = FrozenTrainingSpec()


def _groups(channels: int) -> int:
    return 8 if channels % 8 == 0 else 1


class ResDown1d(nn.Module):
    def __init__(self, c_in: int, c_out: int, stride: int = 2):
        super().__init__()
        self.norm1 = nn.GroupNorm(_groups(c_in), c_in)
        self.conv1 = nn.Conv1d(c_in, c_out, kernel_size=9, stride=stride, padding=4, bias=False)
        self.norm2 = nn.GroupNorm(_groups(c_out), c_out)
        self.conv2 = nn.Conv1d(c_out, c_out, kernel_size=9, stride=1, padding=4, bias=False)
        self.skip = (
            nn.Conv1d(c_in, c_out, kernel_size=1, stride=stride, bias=False)
            if c_in != c_out or stride != 1 else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.conv1(F.gelu(self.norm1(x)))
        y = self.conv2(F.gelu(self.norm2(y)))
        return y + self.skip(x)


class TemporalEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        self.stem = nn.Sequential(
            nn.Conv1d(1, 32, kernel_size=15, stride=4, padding=7, bias=False),
            nn.GroupNorm(8, 32),
            nn.GELU(),
        )
        self.stage2 = ResDown1d(32, 64, stride=2)
        self.stage3 = ResDown1d(64, 128, stride=2)
        self.stage4 = ResDown1d(128, 256, stride=2)
        self.pool = nn.AdaptiveAvgPool1d(1)

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.ndim != 2:
            raise ValueError(f"temporal input must be [B,N], got {tuple(x.shape)}")
        y = self.stem(x.unsqueeze(1))
        y = self.stage2(y)
        y = self.stage3(y)
        y = self.stage4(y)
        pooled = self.pool(y).squeeze(-1)
        return pooled, y


class ResDown2d(nn.Module):
    def __init__(self, c_in: int, c_out: int, stride=(2, 2)):
        super().__init__()
        self.norm1 = nn.GroupNorm(_groups(c_in), c_in)
        self.conv1 = nn.Conv2d(c_in, c_out, kernel_size=3, stride=stride, padding=1, bias=False)
        self.norm2 = nn.GroupNorm(_groups(c_out), c_out)
        self.conv2 = nn.Conv2d(c_out, c_out, kernel_size=3, stride=1, padding=1, bias=False)
        self.skip = (
            nn.Conv2d(c_in, c_out, kernel_size=1, stride=stride, bias=False)
            if c_in != c_out or stride != (1, 1) else nn.Identity()
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        y = self.conv1(F.gelu(self.norm1(x)))
        y = self.conv2(F.gelu(self.norm2(y)))
        return y + self.skip(x)


class TFEncoder(nn.Module):
    def __init__(self):
        super().__init__()
        # Preserve more temporal resolution in the 30-frame STFT axis at the stem.
        self.stem = nn.Sequential(
            nn.Conv2d(1, 16, kernel_size=5, stride=(2, 1), padding=2, bias=False),
            nn.GroupNorm(8, 16),
            nn.GELU(),
        )
        self.stage2 = ResDown2d(16, 32, stride=(2, 2))
        self.stage3 = ResDown2d(32, 64, stride=(2, 2))
        self.stage4 = ResDown2d(64, 128, stride=(2, 2))
        self.pool = nn.AdaptiveAvgPool2d((1, 1))

    def forward(self, x: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        if x.ndim != 3:
            raise ValueError(f"TF input must be [B,F,T], got {tuple(x.shape)}")
        y = self.stem(x.unsqueeze(1))
        y = self.stage2(y)
        y = self.stage3(y)
        y = self.stage4(y)
        pooled = self.pool(y).flatten(1)
        return pooled, y


class F2RepresentationModel(nn.Module):
    """
    Single-detector dual-view representation model.

    IMPORTANT:
      * no detector/network identity enters this model,
      * no CW status enters this model,
      * no technosignature/warp/exotic labels enter this model,
      * amplitude_log10_rms is retained externally as metadata and is not fused here.
    """
    def __init__(self):
        super().__init__()
        self.temporal = TemporalEncoder()
        self.tf = TFEncoder()
        self.fusion_main = nn.Linear(640, 64)
        self.temporal_retention = nn.Linear(256, 64)
        self.projector = nn.Sequential(
            nn.Linear(128, 256),
            nn.GELU(),
            nn.Linear(256, 128),
        )

        # Auxiliary masked-reconstruction heads.
        self.temporal_decoder = nn.Sequential(
            nn.Conv1d(256, 128, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv1d(128, 1, kernel_size=1),
        )
        self.tf_decoder = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.GELU(),
            nn.Conv2d(64, 1, kernel_size=1),
        )

        self.apply(self._init_module)

    @staticmethod
    def _init_module(module: nn.Module) -> None:
        if isinstance(module, (nn.Conv1d, nn.Conv2d, nn.Linear)):
            nn.init.kaiming_normal_(module.weight, mode="fan_out", nonlinearity="relu")
            if module.bias is not None:
                nn.init.zeros_(module.bias)
        elif isinstance(module, nn.GroupNorm):
            nn.init.ones_(module.weight)
            nn.init.zeros_(module.bias)

    def forward(self, temporal: torch.Tensor, tf_view: torch.Tensor) -> Dict[str, torch.Tensor]:
        t_pool, t_local = self.temporal(temporal)
        f_pool, f_local = self.tf(tf_view)

        # R3 prospective order-sensitive temporal summary.
        # Preserve the original mean-pooled temporal representation and add one
        # fixed signed half-time contrast from the existing local feature map.
        n_time = t_local.shape[-1]
        half = n_time // 2
        t_direction = (
            t_local[..., n_time - half:].mean(dim=-1)
            - t_local[..., :half].mean(dim=-1)
        )

        z_main = self.fusion_main(torch.cat([t_pool, t_direction, f_pool], dim=1))
        z_temporal = self.temporal_retention(t_pool)
        embedding = torch.cat([z_main, z_temporal], dim=1)
        projected = self.projector(embedding)

        t_recon = self.temporal_decoder(t_local)
        t_recon = F.interpolate(
            t_recon, size=temporal.shape[-1], mode="linear", align_corners=False
        ).squeeze(1)

        tf_recon = self.tf_decoder(f_local)
        tf_recon = F.interpolate(
            tf_recon, size=tf_view.shape[-2:], mode="bilinear", align_corners=False
        ).squeeze(1)

        return {
            "embedding": embedding,
            "embedding_l2": F.normalize(embedding, dim=1),
            "projected": projected,
            "temporal_reconstruction": t_recon,
            "tf_reconstruction": tf_recon,
        }


def off_diagonal(x: torch.Tensor) -> torch.Tensor:
    n, m = x.shape
    if n != m:
        raise ValueError("covariance matrix must be square")
    return x.flatten()[:-1].view(n - 1, n + 1)[:, 1:].flatten()


def vicreg_components(z1: torch.Tensor, z2: torch.Tensor, eps: float = 1.0e-4) -> Dict[str, torch.Tensor]:
    if z1.shape != z2.shape or z1.ndim != 2:
        raise ValueError("z1 and z2 must be [B,D] and have identical shape")
    b, d = z1.shape
    if b < 2:
        raise ValueError("VICReg requires batch size >= 2")

    invariance = F.mse_loss(z1, z2)

    std1 = torch.sqrt(z1.var(dim=0, unbiased=False) + eps)
    std2 = torch.sqrt(z2.var(dim=0, unbiased=False) + eps)
    variance = 0.5 * (
        torch.mean(F.relu(1.0 - std1)) +
        torch.mean(F.relu(1.0 - std2))
    )

    c1 = z1 - z1.mean(dim=0)
    c2 = z2 - z2.mean(dim=0)
    cov1 = (c1.T @ c1) / float(b - 1)
    cov2 = (c2.T @ c2) / float(b - 1)
    covariance = (
        off_diagonal(cov1).pow(2).sum() / d +
        off_diagonal(cov2).pow(2).sum() / d
    )

    return {
        "invariance": invariance,
        "variance": variance,
        "covariance": covariance,
    }


def masked_huber(
    prediction: torch.Tensor,
    target: torch.Tensor,
    mask: torch.Tensor,
    delta: float = SPEC.huber_delta,
) -> torch.Tensor:
    if prediction.shape != target.shape or prediction.shape != mask.shape:
        raise ValueError("prediction, target, and mask must have identical shapes")
    selected = mask.to(dtype=torch.bool)
    if selected.sum().item() == 0:
        # Explicit zero connected to prediction graph semantics without inventing unmasked loss.
        return prediction.sum() * 0.0
    return F.huber_loss(
        prediction[selected],
        target[selected],
        reduction="mean",
        delta=delta,
    )


def total_ssl_loss(
    out1: Dict[str, torch.Tensor],
    out2: Dict[str, torch.Tensor],
    temporal_target1: torch.Tensor,
    temporal_target2: torch.Tensor,
    temporal_mask1: torch.Tensor,
    temporal_mask2: torch.Tensor,
    tf_target1: torch.Tensor,
    tf_target2: torch.Tensor,
    tf_mask1: torch.Tensor,
    tf_mask2: torch.Tensor,
) -> Dict[str, torch.Tensor]:
    comp = vicreg_components(out1["projected"], out2["projected"])

    rec_t = 0.5 * (
        masked_huber(out1["temporal_reconstruction"], temporal_target1, temporal_mask1) +
        masked_huber(out2["temporal_reconstruction"], temporal_target2, temporal_mask2)
    )
    rec_f = 0.5 * (
        masked_huber(out1["tf_reconstruction"], tf_target1, tf_mask1) +
        masked_huber(out2["tf_reconstruction"], tf_target2, tf_mask2)
    )
    reconstruction = 0.5 * (rec_t + rec_f)

    total = (
        25.0 * comp["invariance"] +
        25.0 * comp["variance"] +
        1.0 * comp["covariance"] +
        1.0 * reconstruction
    )
    return {
        **comp,
        "masked_reconstruction": reconstruction,
        "total": total,
    }


def build_optimizer(model: nn.Module) -> torch.optim.Optimizer:
    # R2A freezes one uniform AdamW parameter group; no hidden exceptions.
    return torch.optim.AdamW(
        model.parameters(),
        lr=SPEC.learning_rate,
        betas=(SPEC.adam_beta1, SPEC.adam_beta2),
        eps=SPEC.adam_eps,
        weight_decay=SPEC.weight_decay,
    )


def scheduled_lr(epoch_index: int) -> float:
    """
    Zero-based epoch index.
    Epochs 0..4: linear warmup from 0.1*base to base.
    Epochs 5..99: cosine decay from base to minimum_lr.
    """
    if epoch_index < 0 or epoch_index >= SPEC.max_epochs:
        raise ValueError("epoch_index outside frozen [0, max_epochs) interval")

    if epoch_index < SPEC.warmup_epochs:
        if SPEC.warmup_epochs == 1:
            factor = 1.0
        else:
            frac = epoch_index / float(SPEC.warmup_epochs - 1)
            factor = SPEC.warmup_start_factor + (1.0 - SPEC.warmup_start_factor) * frac
        return SPEC.learning_rate * factor

    denom = max(1, SPEC.max_epochs - SPEC.warmup_epochs - 1)
    progress = (epoch_index - SPEC.warmup_epochs) / float(denom)
    cosine = 0.5 * (1.0 + math.cos(math.pi * progress))
    return SPEC.minimum_lr + (SPEC.learning_rate - SPEC.minimum_lr) * cosine


def frozen_parameter_count(model: nn.Module) -> Dict[str, int]:
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total = sum(p.numel() for p in model.parameters())
    return {"total": int(total), "trainable": int(trainable)}
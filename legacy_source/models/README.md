# Frozen fitted models

The three `SEED_<seed>/best.pt` files are the original fitted checkpoints,
received from the original workstation and verified against the pre-existing
SHA256 identities in the frozen evaluator. They were not newly trained.
Each checkpoint includes the model tensors, optimizer state and a best-epoch
training snapshot. The full byte identities are in
`evidence/INDEPENDENT_WEIGHT_VERIFICATION.json` and the release manifest.

The exact 960-item branch-specific training/development schedule is supplied
at `training/COMPUTE_BOUNDED_SCHEDULE.json`. This schedule does not include
the 20 compact input NPZ files or the production cache ledger. Its 640/320
branch-item counts are not counts of independent physical observations.

File integrity, static tensor inspection, strict framework loading, synthetic
inference and original raw-input replay are separate checks. No new training,
real-strain inference or 4096 scientific trial follows from including these
artifacts. The optional validation tool uses an existing PyTorch environment;
it must never fall back to unrestricted pickle loading or install packages.

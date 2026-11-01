# Neural methods specification

Each of three fixed seeds defines one detector-local, dual-view convolutional network, with weights shared across detector/run cells and frequency branches. The inputs are a whitened four-second temporal vector and its log-power spectrogram. The 4096-Hz branch covers 20–1600 Hz and has shapes 16384 and 404 × 30; the 16384-Hz branch covers 1600–5000 Hz and has shapes 65536 and 870 × 30. These are the learned-model bands, distinct from the later 64–768-Hz correlation comparison. A 1D residual encoder supplies a 256-dimensional pooled vector and signed half-time contrast; a 2D residual encoder supplies a 128-dimensional pooled vector. Their 640-dimensional concatenation maps to 64 coordinates, joined with a separate 64-coordinate temporal projection to form the exported 128-dimensional embedding.

The actual bounded fit restarted from initialization using 640 training and 320 internal-development branch-specific items across ten detector/run/branch cells. Within each cell, target starts and the training/development boundary were separated by at least 68 s; whole-source independence is not implied. The external validation panel was excluded from fitting. Training used logical batches of 32, AdamW (Loshchilov and Hutter 2019), and six epochs. The objective was $25L_{\mathrm{inv}}+25L_{\mathrm{var}}+L_{\mathrm{cov}}+L_{\mathrm{rec}}$, combining VICReg terms (Bardes, Ponce, and LeCun 2022) with masked Huber reconstruction. Fixed two-view augmentations and the complete layer, optimizer and schedule specifications are given in the supplement. The smallest internal-development loss selected each checkpoint; ties retained the earlier epoch.

Exact source code and checkpoint hashes specify the implementation. The three original trained checkpoints and the exact bounded-training item schedule have been recovered and match their previously frozen SHA256 identities. A new replay from strain through the learned embeddings has not been executed; it additionally requires matching raw or preprocessed inputs and numerical-runtime checks. A newly trained network would be a separate replication.

The implementation uses PyTorch (Paszke et al. 2019). The architecture and learning recipe specify how a model was constructed; trained checkpoint tensors specify the particular fitted model. PCA, nearest-neighbor ranking and cached-score transformations are subsequent non-neural operations with neural-derived inputs. The later direct correlation, energy, physical-source and broad-lag calculations perform no new neural inference. A runtime import of the tensor library is not counted as model evaluation.

# Detailed implementation and dependency specification

The specifications below come from the exact model and preprocessing modules, the recovered bounded trainer and its original base trainer, and the recovered final checkpoints. Code, serialized tensor structure and training metadata were inspected without retraining or neural inference. A nominal 100-epoch scheduler in the model module must not be confused with the six epochs actually executed by the bounded experiment. Likewise, the generic full-schedule JIT trainer's patience rule was not the bounded trainer's stopping criterion.

| Component | Exact specification |
|:--|:--|
| Temporal input | Four seconds, 16384 or 65536 float32 samples, depending on frequency branch. |
| Temporal stem | Conv1d 1→32, kernel 15, stride 4, padding 7, no bias; GroupNorm with eight groups; GELU. |
| Temporal residual stages | Channels 32→64→128→256. Each stage uses GroupNorm/GELU/Conv1d(kernel 9, stride 2, padding 4), then GroupNorm/GELU/Conv1d(kernel 9, stride 1, padding 4); a kernel-1, stride-2 convolution supplies the skip. Convolutions have no bias. |
| Temporal summaries | Global mean over the 256-channel final map; a second 256-dimensional vector is the last-half mean minus first-half mean. |
| Time–frequency stem | Conv2d 1→16, kernel 5, stride (2,1), padding 2, no bias; GroupNorm eight groups; GELU. |
| Time–frequency residual stages | Channels 16→32→64→128. Each stage uses two 3×3 convolutions with padding 1, the first with stride (2,2); pre-convolution GroupNorm/GELU; a 1×1, stride-(2,2) skip; no convolution bias. |
| Embedding | Linear 640→64 applied to the pooled temporal, signed temporal and pooled TF concatenation; separate Linear 256→64 applied to pooled temporal features; concatenate the two 64-dimensional outputs. No embedding normalization is implied by the raw output. An additional L2-normalized output is available separately. |
| Projector | Linear 128→256, GELU, Linear 256→128. The self-supervised agreement objective acts on this projected representation, not directly on the exported raw embedding. |
| Temporal reconstruction head | Conv1d 256→128, kernel 3, padding 1, bias; GELU; Conv1d 128→1, kernel 1, bias. Linear interpolation returns the original temporal length, with `align_corners=False`. |
| TF reconstruction head | Conv2d 128→64, kernel 3, padding 1, bias; GELU; Conv2d 64→1, kernel 1, bias. Bilinear interpolation returns the original TF shape, with `align_corners=False`. |
| Parameter count | 1,804,082 float32 parameters in 64 model tensors per recovered checkpoint, matching the released layer declarations including projector and reconstruction heads. |
| Initialization | Kaiming-normal Conv/Linear weights, `fan_out`, initialization argument `nonlinearity=relu`; zero biases. GroupNorm scales start at one and offsets at zero. The forward activation is GELU. |
| Excluded inputs | Detector identity, CW status and technological-source labels do not enter the network. Unwhitened log-RMS amplitude is retained externally and is not fused into the network. |
| Training cells | O4a/H1, O4a/L1, O4b/H1, O4b/L1 and O4b/V1, each with low/mid and high-frequency branches: ten cells. |
| Bounded data selection | From already `cache_verified` production-TRAIN slots, choose the latest 32 greedily 68-s-spaced items per cell for internal development, and the earliest 64 spaced items ending at least 68 s before the development minimum. These are branch-specific counts, not a count of statistically independent physical observations. |
| Training extent | Six epochs, 20 logical training batches and ten development batches per epoch; up to 120 optimizer updates per seed. Branches are not mixed within a logical batch. The 20 training batches receive a deterministic seed/epoch permutation. |
| Optimizer | AdamW, one uniform parameter group, initial base learning rate $3\times10^{-4}$, weight decay $10^{-4}$, betas (0.9,0.999), epsilon $10^{-8}$; gradient L2 norm clipped to 1. |
| Actual learning rates | Epoch indices 0–5: $3\times10^{-5}$, $9.75\times10^{-5}$, $1.65\times10^{-4}$, $2.325\times10^{-4}$, $3\times10^{-4}$, $3\times10^{-4}$. Five-epoch linear warmup is followed by the first point of the inherited cosine schedule; the nominal minimum rate $3\times10^{-6}$ is not reached by this bounded fit. |
| Checkpoint rule | Strictly smallest mean internal-development composite loss; ties retain the earlier epoch. The actual bounded trainer stops at six epochs, without the generic JIT trainer's patience rule. |
| Low-memory implementation | A logical 32-item batch first evaluates projected features without parameter gradients, obtains the batch VICReg feature gradients, then replays per-item forwards/backwards with reconstruction contributions divided by 32 before one optimizer step. It is not batch-size-one training. |
| Precision and CPU controls | Float64 preprocessing followed by float32 model inputs and parameters; no mixed-precision training. Four intra-operation threads, one inter-operation thread, and `torch.use_deterministic_algorithms(True)` are requested by the actual trainer. Exact original training library/build metadata has not been independently recovered; later inference-runtime checks must not be substituted silently. |

## Preprocessing and augmentations

The preceding 64-second reference and four-second target are linearly detrended separately. Reference PSD estimation uses four-second Hann Welch segments with 50% overlap, median averaging and density scaling. A positive floor is the maximum of float64 tiny and $10^{-12}$ times the median positive in-band PSD, falling back to all positive PSD bins if required. The target Fourier coefficients are divided by the square root of the interpolated PSD. The inverse-transformed target is hard-bandlimited at inclusive branch edges, then centered by its median and divided by $1.4826\operatorname{MAD}$. Missing positive PSD or zero/nonfinite MAD is rejected. The STFT uses periodic Hann windows, FFT divided by window sum, log10 power with a float64-tiny floor, integer starts, 50% overlap and no zero padding. Window/hop/FFT lengths are (1048,524,1048) and (4192,2096,4192), yielding 30 time frames and 404 or 870 frequency bins.

Each item produces two fixed-rule stochastic views. The temporal view receives an integer, zero-padded shift uniformly within ±0.125 s, a random sign with probability 0.5, log-uniform gain in [0.9,1.1], and Gaussian noise with RMS 0.005 times the transformed signal RMS. A contiguous mask of `floor(0.02*N)` samples is zeroed; its pre-mask augmented waveform is the reconstruction target. The TF view masks one uniformly selected time column across frequencies and reconstructs the original base TF array. The TF array is not recomputed after the temporal perturbations. Random generators are seeded from a SHA256-derived tuple containing the model seed, epoch, batch sequence, item index, view index and branch. Development views always use seed 20260919 and epoch zero, for all three models.

Invariance is MSE between projected views. The variance term averages the two mean hinge penalties on $1-\sqrt{\operatorname{var}(z)+10^{-4}}$, using population variance. For each view, the centered covariance is divided by $B-1$; off-diagonal squared entries are summed and divided by feature dimension, and the two view terms are added. Reconstruction averages temporal and TF masked Huber losses with delta 1, each first averaged over the two views. Only masked entries contribute. The loss weights are exactly (25,25,1,1).

## Checkpoint and source provenance

| Seed | Recovered `best.pt` SHA256 |
|:--|:--|
| 20260919 | `9602C9B73A4A7967249AC871ED23086805547F1C1B23C3DEF9535F02318652E8` |
| 20260920 | `DDB0A8BD263572DD32CD285812F34014F3FE4EF0117A312E02C5C811EECEC075` |
| 20260921 | `B0FB3AEA2A3657E88F9F79D6CB069BD1806030E50054CB7F2D8D1F862BEC533C` |

All three recovered checkpoint files match the previously frozen digests in the table. Their static tensor inventories each contain 64 float32 model tensors with 1,804,082 parameters; all tensor keys and shapes agree with the released architecture, and no nonfinite stored values were found. The saved optimizer states record 120 updates per parameter. Best epoch index 5 (the sixth epoch) and development losses 22.44843092896044, 21.1369436269626 and 21.111260562669486 agree exactly with the retained terminal ledger. The best-checkpoint snapshot precedes the trainer's terminal completion bookkeeping; its saved `complete=false` field is not evidence that the separate training campaign failed to close. These are file, tensor-structure and metadata checks, not a strict framework load or a neural-output replay.

The recovered bounded schedule has SHA256 `E13A09EF421E9F8C396EB3AFC3CAE34C2FDA1E0C3A13AA321ABCDB96EAA2220E`. Its ten cells contain 640 training and 320 internal-development branch-specific items, with 960 unique slot keys and 958 distinct detector/run/GPS target triples. Two exact target starts repeat across frequency branches, and other cross-branch 68-second supports overlap within partitions. The declared 68-second spacing within each branch cell and the training/development separation across branches were verified from the schedule. These checks do not establish whole-source independence. Exact item identities and recorded input hashes are now available; the referenced compact training arrays and production ledger remain unavailable, so their numerical contents and selection from the full eligible pool have not been replayed.

The exact model source has SHA256 `E5DFA40E229F6B58E008FDDA45800C9BF570936265FA36300C4B06A21E9A423E`. The recovered actual bounded trainer has SHA256 `141D2D4C648B6A660A07BD1AB08E33B366F487E606A69602600B92977A3AC049`; its original base trainer has SHA256 `0C03FA9A0C7ACF27F91BC52DFCC3C943DC20FE521E6FB03F0BCE85CFE07D0DF5`. Both were reconstructed byte-exactly from archived PowerShell text without executing historical launchers. Full module names, all source digests and retrieval provenance are in `NN_METHODS_AUDIT.json` and `RECOVERED_TRAINING_SOURCE_PROVENANCE.json`.

The recovered weights supply the particular fitted parameters needed to replay the original raw-input learned embeddings and dependent learned rankings. Matching inputs and numerical-runtime validation remain necessary. Cached embedding/scorer arithmetic can be checked without running the network; direct correlation/energy, source-only physical calculations and the later P2/P3/P4 correlation diagnostics have their own non-neural inputs and requirements. Retraining from the declared recipe produces a new replication whose agreement must be assessed, not assumed identical to the original fit.

## Neural dependence and the distinct completion units

The following mapping distinguishes learned inputs from the statistic evaluated on them. The code-and-result audit covers the available archived evidence; it is not a live examination of the workstation or a new raw-data experiment.

| Calculation | Role of the neural models | Reproduction boundary |
|:--|:--|:--|
| Learned single-detector representation and its diagnostic gates | Three seeded neural fits and frozen inference | The original fitted checkpoints are recovered; raw-input replay still requires matching inputs and numerical-runtime checks. |
| Source catalog and declared quality/finite checks | Metadata and numerical validation | No neural architecture is required for these checks themselves. |
| Fusion, learned ranking and representation consistency | Neural embeddings followed by standardization/PCA, nearest-neighbor distances or pair formulas | These downstream operations can use the valid retained banks; raw-to-bank replay needs the models. |
| Calibration/foreground embedding production and learned strain pilot | Frozen neural inference, with an independent non-neural energy comparator in the pilot | Stored results remain inspectable; regenerating learned responses needs matching weights and inputs. |
| Correlation development | New correlation and energy calculations; the learned-score comparison reuses matched pilot outputs | No new F2 calls in the correlation development run. The reused learned comparator retains its upstream dependence. |
| Six-source-block, structured-packet, physical-source and broad-lag studies | Raw correlation/energy, analytic source histories and timing diagnostics | Their archived native summaries report zero new F2 calls. Matching raw inputs, numerical definitions and source parameters remain necessary. |
| Observational timeline review | Statistical reuse of retained neural-derived scores | No new model inference or new observed exposure is created. |
| Executed CPU record survey |19fixed Fourier, autocorrelation and local-reference features; no neural calls |4096selected supports actually audited; valid-feature and quality/input-rejection counts are separate. Synthetic tests retain their engineering evidence class. |

| Experiment or computation | Retained completed count | Meaning |
|:--|:--|:--|
| Original full-search background campaign | 3/4096 | The original full-search trial unit. |
| H1 conditional-noise assay | 10/4096 | Conditional donor units with fixed other-detector observations. |
| Registered transformations of the existing observations | 4096/4096 | Transformations of the retained observation set; no new independent observing exposure. |
| Executed CPU detector-record survey |4096/4096audited |4020valid feature records;76quality rejections;0input rejections. |

The software engineering suite for the new CPU component has 13 synthetic tests. A separate completed synthetic scheduler fixture is also a software check, not 4096 detector observations. The companion `BASLAT.cmd` invokes saved-result and figure reproduction; it does not repeat the separately executed4096record survey. The new experiment has its own raw-source runner and saved-feature replay under `experiments/random4096_20261030/`. The recorded count of finite checks, cached tensors, metadata targets or synthetic jobs is not substituted for a completed scientific trial.

The three recovered checkpoints are the final frozen models used by the current learned branch. They do not recover every earlier failed training variant, its original inputs or its numerical environment. Historical failures retain their stated evidence level. The original item schedule is now available; exact training replay additionally requires its referenced input arrays and numerical environment. Retraining with new tensors must be labeled a new replication and its numerical and scientific agreement evaluated explicitly.

# Timing specificity and conditional amplitude limits for structured transients in public gravitational-wave data

Murat Metehan Türkoğlu

## Abstract

Searches for structured gravitational-wave transients must distinguish a response to injected signals from physical timing consistency and calibrated inference. We examine these distinctions in public O4a and O4b strain using fixed learned, correlation and energy statistics. On six source-disjoint blocks, a restricted-delay correlation definition exceeded its cut for 96/96 original injections versus 43/96 for energy, but failed its prespecified O4a noise guard. In an exploratory structured-packet panel it accepted 48/48 originals and 38/48 deliberately over-delayed copies. Saved broad-lag curves place stronger raw and envelope maxima outside the physical cap for every delayed copy in its score-driving pair. However, broad raw maxima also lie outside for four originals, demonstrating a cost of a simple peak-location veto. Paired input conditions and calibration counts are audited separately from held-out noise response; no equal-false-alarm superiority follows. A source-grouped H1 survey completed 4096 selected-record audits, retaining 4020 finite feature vectors and 76 quality rejections. A separate fixed linear projection on twelve retained H1 contexts yields a 90% phase-ensemble upper endpoint of $2.3393\times10^{-23}\,\mathrm{Hz}^{-1/2}$ for one prescribed four-Gaussian, 256-Hz coded packet. Its coverage assumes a uniform carrier phase independent of additive nuisance, model choice and interval selection. The application quantifies its conservative amplitude multiplier and common-context envelope penalty, rather than introducing quadrature filtering or distribution-robust limits as new principles. The measurements show why a light-travel-limited correlation maximum is insufficient evidence of physical envelope timing, and quantify the signal loss of a simple broad-peak veto. They also provide a reproducible conditional strain constraint when the stipulated source-phase model is appropriate. These results guide validation and interpretation of this structured-transient statistic, without assigning technological origin or discovery significance.

# Introduction

Public gravitational-wave strain permits searches for unusual temporal and inter-detector structure without specifying a complete astrophysical waveform. Such searches are relevant to signals outside existing template families and to conditional tests of proposed technological sources. Their interpretation nevertheless requires several distinctions. A large anomaly score may reflect instrumental behaviour, environmental coupling, an astrophysical signal or a limitation of the analysis. Structure that resembles a coded waveform does not by itself identify communication or controlled dynamics. Here technological sources motivate testable signal families; they are not the default explanation for an unusual observation.

Correlation and network consistency already provide established tools for unmodelled burst searches. The $r$-statistic tests conditioned detector data over allowed delays (Cadonati 2004). X-Pipeline and coherent WaveBurst use a common network response to gravitational-wave polarizations, rather than only the largest pairwise correlation (Sutton et al. 2010; Klimenko et al. 2016). Learning-based approaches also combine anomaly information with detector agreement: GWAK includes reconstruction and correlation features, CoAD learns cross-detector coincidence, and the MADGRAV preprint describes staged anomaly, glitch, coherence and ranking operations (Raikman et al. 2024; Ratner 2026; Inguglia et al. 2026). These antecedents preclude treating correlation, learned ranking or their arrangement in stages as a new general detection principle. The question addressed here concerns the measured behaviour of one fixed implementation.

The relevant discovery standard is set by searches that evaluate their full background and signal-dependent sensitivity. Published O3 and O4a burst analyses report recovery and inference at specified false-alarm operating points (Abbott et al. 2021a; Abac et al. 2025). An AUROC on constructed examples or a fixed-cut acceptance fraction on a finite noise panel answers a different question. In particular, favorable discrimination can coexist with excessive noise responses after transfer, or with acceptance of signals whose detector delays violate a common-source geometry. These endpoints must be measured separately before a signal family can support a calibrated observational claim.

Physical interpretation adds a source-to-detector requirement. A waveform must specify dynamics, amplitude, duration, polarizations and propagation, followed by the actual processing applied to the detector data. Accelerated-mass calculations already include trajectory assumptions and exhaust bookkeeping (Sellers et al. 2022); numerical warp-fluid collapse illustrates a different, model-specific waveform and frequency scale (Clough, Dietrich, and Khan 2024). Neither is represented faithfully by assigning a physical label to a generic short chirp. For a signal extending into a reference interval, retaining that history is also essential: truncation or forcing an unchanged reference can alter the measured response.

The specific question is whether the tested restricted-delay, maximum-pair correlation definition can respond strongly to a structured transient while failing to distinguish its physical envelope timing, and what conditional amplitude information can still be obtained with an explicitly different linear statistic. The empirical increment is a source-linked counterexample for this implementation, including the measured cost of rejecting broad-lag peaks outside the light-travel cap. Its practical consequence is that original-signal injections alone are an incomplete validation of a structured-transient screen: deliberately displaced envelopes and matched unmodified noise reveal distinct failure modes, while testing only the displaced controls would conceal the loss imposed on physically projected signals by a proposed veto. It is not the first recognition that pair correlation differs from coherent network reconstruction, nor a demonstrated failure of X-Pipeline, coherent WaveBurst or GWAK. A separate contribution applies phase-ensemble confidence geometry to one specified coded transient, with continuous-arrival response certification and raw-input replay. Quadrature likelihoods, loudest-event inference and distribution-robust upper limits already exist (Jaranowski, Królak, and Schutz 1998; Biswas et al. 2009; Dergachev 2013).

Comparisons are organized by shared strain inputs, attained finite calibration counts and held-out noise response. These are distinct requirements. Positive responses, failed criteria, challenging controls and historical numerical results are retained together; repeated variants are not independent observations. The study establishes neither a generally superior search method nor an identification of technological sources.

# Data and analysis methods

The analysis uses public interferometric strain and source metadata associated with O4a and O4b. The current two-detector configuration uses H1 and L1; the three-detector configuration adds V1. Historical public-data access and quality interpretation follow the releases and metadata represented in their archived source-selection records (Abbott et al. 2021b; Gravitational Wave Open Science Center 2025, 2026). The subsequent randomized CPU survey acquired the exact pinned public HDF5 sources anew, verifying publisher checksums before measurement; it is reported separately below. These current release references establish the public data context; exact input versions remain those of the prespecified source selections. Target and reference intervals are kept distinct.

The principal local processing unit is a four-second target with a preceding 64-second context. The learned representation chain includes 4096 and 16384 Hz branches. An earlier physical-reference reconstruction also examined a 1700–5000 Hz extension on paired 16 kHz H1/L1 inputs. The 64–768 Hz band described below belongs to the later raw-correlation and energy comparison; it must not be assigned retrospectively to every earlier project component. The official O4 documentation calls for the 16384 Hz branch around 1700 Hz and above, and cautions that data quality is less well studied above 2 kHz (Gravitational Wave Open Science Center n.d.); the historical high-frequency products do not establish a calibrated search in that band.

Two collections both have 192 network cases but serve different roles. The earlier collection is a controlled injection/contamination benchmark with labels and nominal protocol amplitudes. The later observational collection contains 192 selected foreground target windows. These are not interchangeable cohorts. Three model seeds applied to one collection also do not create three times as many independent observations.

Training, development, validation, calibration/reference, observation and exploratory-reuse roles are recorded explicitly. Full 68-second quality checks for the later source-disjoint panel include the declared valid-strain and burst-category quality conditions and the applicable hardware-injection exclusions. These criteria are not a complete investigation of every instrumental or environmental alternative. Physical source intervals, including detector and sample-rate aliases, are the units used for source-exclusion accounting. Disjointness of intervals does not establish statistical independence.

The six-block test selected its source blocks before evaluating their new scores. The subsequent structured-packet and physical-source studies reuse that already-open noise; neither is presented as a new held-out confirmation. The selected source times, numerical inputs and evidence limits accompany the reproducibility materials.

# fixed representations, ranking and comparison statistics

## Neural encoder and actual bounded training

Each of three fixed seeds defines one detector-local, dual-view convolutional network, with weights shared across detector/run cells and frequency branches. The inputs are a whitened four-second temporal vector and its log-power spectrogram. The 4096-Hz branch covers 20–1600 Hz and has shapes 16384 and 404 × 30; the 16384-Hz branch covers 1600–5000 Hz and has shapes 65536 and 870 × 30. These are the learned-model bands, distinct from the later 64–768-Hz correlation comparison. A 1D residual encoder supplies a 256-dimensional pooled vector and signed half-time contrast; a 2D residual encoder supplies a 128-dimensional pooled vector. Their 640-dimensional concatenation maps to 64 coordinates, joined with a separate 64-coordinate temporal projection to form the exported 128-dimensional embedding.

The actual bounded fit restarted from initialization using 640 training and 320 internal-development branch-specific items across ten detector/run/branch cells. Within each cell, target starts and the training/development boundary were separated by at least 68 s; whole-source independence is not implied. The external validation panel was excluded from fitting. Training used logical batches of 32, AdamW (Loshchilov and Hutter 2019), and six epochs. The objective was $25L_{\mathrm{inv}}+25L_{\mathrm{var}}+L_{\mathrm{cov}}+L_{\mathrm{rec}}$, combining VICReg terms (Bardes, Ponce, and LeCun 2022) with masked Huber reconstruction. Fixed two-view augmentations and the complete layer, optimizer and schedule specifications are given in the supplement. The smallest internal-development loss selected each checkpoint; ties retained the earlier epoch.

Exact source code and fitted-model identities specify the implementation. The three original trained checkpoints and the exact bounded-training item schedule have been recovered and match their archived identities. A new replay from strain through the learned embeddings has not been executed; it additionally requires matching raw or preprocessed inputs and numerical-runtime checks. A newly trained network would be a separate replication.

The implementation uses PyTorch (Paszke et al. 2019). The architecture and learning definition specify how a model was constructed; trained checkpoint tensors specify the particular fitted model. PCA, nearest-neighbor ranking and cached-score transformations are subsequent non-neural operations with neural-derived inputs. The later direct correlation, energy, physical-source and broad-lag calculations perform no new neural inference. A runtime import of the tensor library is not counted as model evaluation.

## Learned representation, fusion and learned ranking

For each of the three fixed seeds, the two detector-local branches produce 128-dimensional embeddings. The declared branch average is used by the network fusion. Concatenating three masked detector embeddings, a three-element detector mask and six pair features gives 393 inputs: three cosine agreements and three Euclidean disagreements normalized by $\sqrt{128}$. A shared, pooled-training-set standardization and 128-dimensional principal-component transformation define the later fixed fusion. Earlier fusion and probe failures remain part of the development record.

For each seed and topology, the learned ranking applies the archived featurewise robust scaling to the background reference representations. If $d_5(x)$ is the mean normalized Euclidean distance to the five nearest reference points, the scalar ranking is standardized using the training leave-one-out median and interquartile range, $$S_{\rm L}(x)=\frac{d_5(x)-m_{\mathrm{LOO}}}
 {q_{0.75,\mathrm{LOO}}-q_{0.25,\mathrm{LOO}}}.$$ Training self-comparisons are excluded. Featurewise scaling and final scalar standardization are different operations; their constants and degenerate-scale handling are fixed by the archived implementation. The percentile-calibration failure and subsequent raw-score control are reported below.

The learned pair statistic uses standardized embedding agreement minus disagreement for each active pair, followed by the minimum over pairs. This learned-feature statistic is distinct from the later raw-strain correlation ratio comparison: $$C_{ij}=\frac{c_{ij}-m_c}{s_c}-\frac{\ell_{ij}-m_\ell}{s_\ell},\qquad
 S_{\rm N}=\min_{(i,j)\in\mathcal P} C_{ij}.$$ The fixed interquartile convention is $s=\mathrm{IQR}/1.349$ with its archived fallbacks. No high value is interpreted as a probability of astrophysical or technological origin.

## Raw-strain correlation and energy

The normalized pairwise-correlation statistic (correlation ratio) and energy comparison use only the 4096 Hz branch. A 68-second record is partitioned into 17 four-second segments. Each segment is demeaned and multiplied by the symmetric 16384-sample Hann window. Bins from 64 through 768 Hz inclusive are retained. For correlation ratio, each detector spectrum is whitened by the square root of the binwise median power across the 16 preceding segments. The selected powers must be positive; no new numerical floor is introduced.

For a pair of whitened segment arrays, the numerator is a linear cross-correlation computed with a $2N$ zero-padded FFT. Its denominator is the product of the full-segment $L^2$ norms. The maximum absolute value is searched over the fixed integer light-travel lags; the H1–L1, H1–V1 and L1–V1 caps are respectively 41, 111 and 108 samples. There is no fractional lag interpolation. The network segment value is the maximum over active pairs, and $$S_{\mathrm{corr}}=\frac{\rho_{\mathrm{network,target}}}
 {\operatorname{median}_{j=1}^{16}\rho_{\mathrm{network},j}}.$$ The corresponding energy statistic uses unwhitened selected-band FFT power divided by the Hann-square sum. For each detector its target power is divided by the median of its 16 past powers; these ratios are averaged across active detectors. It is not an estimated matched-filter network SNR.

The cuts are transported unchanged, with a strict $>$ comparison:

<div class="center">

| Method |                O4a |                O4b |
|:-------|-------------------:|-------------------:|
| correlation ratio    | 1.2127042400481731 | 1.2033275141068391 |
| energy ratio | 1.1835502945794922 | 1.0797567256278390 |

</div>

These finite calibration cuts are not equal-FAR operating points. Maximizing within a physical lag window ensures that the selected lag lies there by construction; it does not prove that the true wave-envelope arrival time is physical. The maximum over pairs also does not solve a common-sky, all-detector polarization fit.

## Injection amplitudes, controls and dependence

The original controlled benchmark nominal amplitude levels belong to that benchmark’s contract. Later strain pilots use explicitly normalized source $h_{\rm rss}$ levels and a fixed detector projection. The structured-packet study uses two short 256 Hz structured families: a smoothly phase-coded packet and a phase-related packet train. Its source $h_{\rm rss}$ values are $10^{-21}$ and $10^{-20}\,\mathrm{Hz}^{-1/2}$. Time-reversed polarizations and detector-index extra delays of $0$, $0.15$ and $0.30$ seconds supply the declared controls. The delayed controls retain the same underlying waveforms; they are not independent samples from a population of instrumental glitches.

Variants share noise, geometry and source blocks. We therefore report counts, source-balanced summaries where declared, and each injection’s change from its own unmodified-noise baseline. Binomial independence intervals or new population significances are not inferred from the variant counts.

## Comparable inputs, calibration counts and held-out noise

Equivalence was audited at three levels: paired strain inputs, attained calibration exceedances and held-out noise response. The legacy method-specific cuts each exceeded one of the same twelve calibration contexts per run. The later H1 cuts each exceeded zero of the same twenty-five calibration source-group maxima, because each cut was its method's largest calibration group score. Equality on these finite panels did not transfer to equal held-out counts. The following table uses the original cuts and the same noise units within each cohort; it does not pool cohorts or convert counts to time-based FARs.

| Cohort and run | Method | calibration above cut | Held-out noise above cut | Original injection endpoint |
|:---|:---|---:|---:|:---|
| Six-block O4a | Correlation | 1/12 contexts | 3/12 contexts | Original six-block result retained |
| Six-block O4a | Energy | 1/12 contexts | 1/12 contexts | Original six-block result retained |
| Six-block O4b | Correlation | 1/12 contexts | 1/12 contexts | Original six-block result retained |
| Six-block O4b | Energy | 1/12 contexts | 4/12 contexts | Original six-block result retained |
| H1 survey O4a | Robust feature ranking | 0/25 groups | 2/27 test groups | 54/72 new context crossings |
| H1 survey O4a | Energy | 0/25 groups | 1/27 test groups | 36/72 new context crossings |
| H1 survey O4b | Robust feature ranking | 0/25 groups | 0/27 test groups | 42/72 new context crossings |
| H1 survey O4b | Energy | 0/25 groups | 2/27 test groups | 33/72 new context crossings |

calibration and held-out counts use unmodified noise. Contexts in the six-block panel and source-group maxima in the H1 survey are different statistical units. Zero calibration exceedances do not establish a zero false-alarm probability. Source-disjoint roles alone establish neither independence nor exchangeability. At the H1 cuts the aggregate 96/144 versus 69/144 context response is therefore a paired fixed-cut contrast, with different held-out noise behavior. The legacy 96/96 versus 43/96 comparison retains its failed epoch-wise screen. The cohort inventory and source identities accompany the numerical audit.

# Representation and ranking validation

The historical measurements distinguish numerical stability, constructed-signal discrimination and physical consistency. Several early values are retained terminal summaries, not newly reopened per-case arrays; their evidence levels and failed decisions remain in the scientific supplement.

Three reported training seeds used 640 training and 320 internal-development branch-specific items. These counts are not numbers of independent physical GPS supports. The non-collapse fraction was $0.9921875$, median cross-seed linear CKA $0.97555235$, and augmentation-pair cosine $0.99253152$. Nevertheless, the initial feature probe passed only three of six requirements; a later panel passed four, while the ten-panel stability assessment failed. A subsequent prospectively fixed five-panel assessment passed all five panels, with median repetition correlation $0.74852925$. Time–frequency excess passed none of those panels. The final methodological assessment is available only as a historical report; its separate numerical amendment was not recovered.

The aligned fusion partitions contained 128 training, 64 development and 64 validation network cases. Cross-seed CKA reached $0.99631325$ while validation AUROC was $0.501953125$; the pooled controlled-positive amendment also failed, with validation AUROC $0.763916015625$. High representation agreement therefore did not imply useful discrimination.

The original percentile mapping saturated: validation AUROCs were $0.578125$ for the two-detector epoch and $0.5$ for the three-detector epoch, despite raw-distance AUROCs of $1.0$. Removing that mapping retained the declared five-neighbour ranking; reported cross-seed rank correlations were $0.92628205$ and $0.91547619$. A separate learned pair-consistency statistic remained insufficient, with coherent-versus-background validation AUROCs $0.6201171875$ and $0.83984375$.

The later 192-case controlled benchmark reported ranking AUROC $1.0$ and pair-consistency medians $0.974826$ and $0.955729$. Its evidence is a transcribed terminal handoff; the pair-consistency statistic was first evaluated on this benchmark after label release. Seeds share the same cases and do not multiply independent sample size.

The completed calibration bank contains 1,066 detector records from 12 physical intervals, 27 streams and 54 files. A within-stream conditional diagnostic returned $p=3081/4097$; non-rejection did not establish stationarity or a physical-search null. Exact cached replay and dependent recombinations establish computational properties, not independent search exposure. The original full-search campaign remains at three of 4096 trials. Complete historical source-reference calculations, including the analytic accelerated- source reconstruction and partial Galactic-centre Messenger reproduction, are retained separately in the supplement.

# Completed observational and injection results

The completed experiments form a sequential development record, rather than replications on a common test population. We retain the observational non-rejection, the unsuccessful learned-score pilot, the favorable development comparison, the failed prespecified noise-control criterion, and the subsequent exploratory extension. The experiment summary below distinguishes their cohorts and primary denominators. The numerical sources and their archived identities are recorded in the accompanying result ledger.

<div id="tab:experiment_sequence">

| Experiment                      | Evaluation scope                                                                                                    | Binding outcome                                                                                                                  |
|:--------------------------------|:--------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| Historical controlled benchmark | 192 cases; per epoch: 24 background, 48 coherent injections, 24 single-detector contaminants                        | Reported learned ranking AUROC $1.000000$ for all seeds; median learned pair statistic AUROC $0.974826$ (O4a), $0.955729$ (O4b). |
| Conditional observation         | 192 four-second targets; 480 detector records                                                                       | Conditional $p=1712/4097=0.4178667$; no rejection at $\alpha=0.05$.                                                              |
| Learned-ranking strain pilot    | 24 calibration contexts; 12 injection contexts; 240 variants; primary evaluation subset: 64 originals in six blocks | Equal-block recovery $0.125$ for learned ranking and $0.625$ for energy; no automatic expansion.                                 |
| Correlation development         | 24 calibration contexts; four development contexts in two physical blocks; 80 variants, including 32 originals      | correlation ratio $32/32$, energy $24/32$, learned ranking $0/32$; favorable development screen, requiring fresh confirmation.                 |
| Source-disjoint validation      | Six new source blocks; 24 noise contexts; 240 variants, including 96 originals                                      | correlation ratio $96/96$ and energy $43/96$; paired gain $15/32$; O4a noise guard failed.                                                     |
| Structured-packet extension     | Same previously examined noise; 12 injection contexts; 144 variants, including 48 originals                         | correlation ratio $48/48$ and energy $21/48$; extra-delay controls $38/48$ for correlation ratio; descriptive extension only.                                |

Completed experiments, in analysis order. Counts in different rows must not be pooled into a matched-method comparison. “Original” denotes injections before the time-reversal and extra-delay controls.

</div>

## Historical controlled benchmark

The historical benchmark is available as results transcribed from supplied terminal summaries. This evidence level is distinct from the later complete-return record audits: the historical per-case score bank was not independently reprocessed for this manuscript integration. The bank contained 192 cases, comprising 24 background cases, 48 coherent network injections, and 24 synthetic single-detector contamination cases in each of O4a and O4b. The same cases were scored with seeds 20260919, 20260920, and 20260921; this does not create 576 independent cases.

The reported learned ranking AUROC for coherent injections versus background was $1.000000$ for every seed in both epochs. For the embedding-based network-consistency comparison against single-detector contamination, the seed-wise AUROCs were $0.974826$, $0.984375$, and $0.964410$ in O4a, and $0.942708$, $0.970486$, and $0.955729$ in O4b. The corresponding medians were $0.974826$ and $0.955729$. Both reported medians exceeded the declared $0.80$ criterion. We retain the reported six-decimal precision and do not infer population confidence intervals from these rounded summaries.

The evaluation chronology is asymmetric. Learned ranking scores were fixed before the benchmark label release. The learned pair statistic was first evaluated on the controlled benchmark bank after label release, following a historical numerical-convention binding check whose compared summary differences were zero. This is not a claim that both learned ranking and learned pair statistic score banks were fixed before unblinding. The complete family/amplitude summary is preserved in the scientific supplement. The nominal amplitude levels in that benchmark are not source strain, physical SNR, or distance, and its score medians are not detection efficiencies.

These positive discrimination results are retained alongside the subsequent negative strain-level pilot. The experiments differ in cohorts, signal families, amplitude definitions, and endpoints; a favorable finite-bank AUROC does not imply adequate sensitivity at the later transported cuts.

## Conditional observational result

The observational execution completed all 192 network targets, with 96 from O4a and 96 from O4b. Their four-second target intervals give 768 s of target exposure. The 68 s raw context around a target is not additional search exposure, and the 192 separated targets do not constitute one continuous 768 s recording. The fixed joint statistic was the maximum over targets of the median of the three standardized, seed-specific learned ranking values. Its observed value was $116.63425977697752$.

Of 4096 registered within-source-block transformations, 1711 produced a statistic at least as large as the observation, with ties included. Applying the registered finite-sample correction gave $$p_{\mathrm{cond}}=\frac{1711+1}{4096+1}
 =\frac{1712}{4097}=0.41786673175494266.$$ The declared conditional working null was therefore not rejected at $\alpha=0.05$. Its exchangeability/invariance condition remains an explicit working assumption; score-blind source selection does not prove that condition. This result neither establishes an absence of technosignatures nor establishes adequate sensitivity to all relevant signals.

The conditional draws are not independent repetitions of the entire physical search and add no independent noise livetime. They did not increase the legacy full-search null count, which remained three completed trials out of the original target of 4096. The registered recurrence structure also imposes a limitation on significance resolution: the most favorable recurrence bound for an O4a winner is at least $1/14>0.05$, and the actual winning structure has a $1/13$ floor. Increasing only the number of Monte Carlo draws cannot remove that structural bound. Finally, this observation used learned ranking; it is not an observational search with the subsequently developed correlation ratio statistic.

## Learned-ranking strain pilot

The strain-level pilot completed 24 calibration contexts, 12 unmodified injection-context baselines, and 240 variants. The primary evaluation subset contained eight contexts in six physical source blocks and 64 original injections. At the fixed cuts, the ordinary exceedance counts were $12/64$ for learned ranking and $40/64$ for energy. The prespecified equal-source-block recovery fractions were $1/8$ and $5/8$, respectively, giving a difference of $-1/2$. The ordinary fraction $12/64$ is not interchangeable with the primary learned ranking value $1/8$, because the source blocks contained different numbers of contexts.

All learned ranking exceedances occurred in one O4b source block. Eight of the 12 exceedances belonged to injection contexts whose unmodified baselines already exceeded their cut. Thus an ordinary exceedance count alone overstates the number of changes attributable to the added signals. The declared expansion criteria were not met, and the binding no-go decision for automatic expansion was retained. This is a negative result for the tested fixed representation-plus-ranking pipeline and finite signal panel; it is not evidence that machine learning or anomaly detection is generally ineffective.

## Correlation development and the prospective six-block test

The subsequent correlation comparison was initially a development analysis on two already available physical source blocks. Its four development contexts provided 32 original injections. correlation ratio, energy, and the fixed learned ranking comparator exceeded their cuts in 32, 24, and zero cases, respectively. The equal-block net threshold responses were $1$, $1/4$, and zero. Consequently, the correlation ratio-minus-energy lift was $3/4$, but the development decision explicitly required fresh confirmation. This is a paired, same-strain three-method comparison at the respective fixed cuts. It does not match held-out false-alarm rates or establish the same ranking on the later source-disjoint validation strains.

The source-disjoint validation used six prospectively selected source blocks, three per observing epoch, with four unmodified noise contexts in each block. Two contexts per block received the declared injections, giving 12 injection contexts and 96 originals across four waveform families and two source $h_{\mathrm{rss}}$ levels. Time-reversed and extra-delay controls brought the complete variant count to 240. All source blocks and all declared records were retained.

For an injected output $s^{\mathrm{inj}}_{ik}$ and its own unchanged-noise baseline $s^0_i$, define the paired net threshold response within block $b$ as $$J_{m,b}=\frac{1}{N_b}\sum_{(i,k)\in b}
 \left[\mathbf{1}\{s^{\mathrm{inj}}_{m,ik}>c_{m,e(i)}\}
 -\mathbf{1}\{s^0_{m,i}>c_{m,e(i)}\}\right],
 \label{eq:paired_lift}$$ where $m$ identifies the method and $e(i)$ its epoch. The original cuts, including the strict inequality, were transported without refitting. The source-disjoint validation has 16 original variants per block, so its overall variant average also equals the mean of the six block values. This paired quantity is a descriptive threshold statistic, not a physical false-alarm probability.

The correlation ratio exceeded the fixed cut in all $96/96$ originals, whereas the energy ratio did so in $43/96$. Sixteen of the correlation ratio exceedances and eight of the energy exceedances already had positive own-noise baselines. There were 80 upward crossings for correlation ratio and 35 for energy, with no downward crossings. Hence $$J_{\mathrm{corr}}=\frac{80}{96}=\frac56,\qquad
 J_{\mathrm{energy}}=\frac{35}{96},\qquad
 \Delta J=\frac{45}{96}=\frac{15}{32}.$$ Five of the six source blocks had positive $\Delta J$. The O4a and O4b mean gains were $2/3$ and $13/48$, respectively. The negative block, O4b B03, had $\Delta J=-7/16$ and remains in the aggregate.

The full prospective success screen nevertheless failed. Among all 12 unmodified O4a noise contexts, correlation ratio exceeded its cut three times and energy once. This violated the fixed requirement that correlation ratio produce no more noise exceedances than energy in each epoch. O4b satisfied that condition with one versus four exceedances. Pooling the epochs into four versus five would change the declared criterion and cannot convert the outcome into a pass. The binding result is failure of the prespecified validation screen. The observed screen failure does not, by itself, statistically establish a population false-alarm-rate increase or distribution shift.

<div id="tab:fresh6_epoch">

| Epoch | Noise contexts | correlation ratio noise | Energy noise | $\Delta J$ |  Guard |
|:------|---------------:|----------:|-------------:|-----------:|-------:|
| O4a   |             12 |         3 |            1 |      $2/3$ | Failed |
| O4b   |             12 |         1 |            4 |    $13/48$ | Passed |

Source-disjoint validation fixed-cut outcomes. The noise guard uses all 24 unmodified noise contexts; $J$ uses the 12 injection contexts and their matched baselines. These are different denominators.

</div>

The transported cuts define a valid finite fixed-definition comparison, but they do not establish equal false-alarm operating points in the new cohort. Accordingly, the larger injected exceedance count is not a claim of superiority at equal FAR. Variants reuse contexts and source blocks; we do not assign binomial independent-trial confidence intervals or discovery significance to the 96 originals or 240 variants.

## Control behavior and the structured-packet extension

All 96 source-disjoint validation time-reversed examples exceeded the correlation ratio cut, as did their original counterparts; energy exceeded in 43 cases for each orientation. Among 48 extra-delay controls, correlation ratio exceeded in 12 and energy in 32. All 12 correlation ratio exceedances occurred in the modulation family; none occurred in the other 36 extra-delay examples. These controls use delayed copies of the same waveform rather than independent instrumental-glitch draws.

The structured-packet extension was declared after these source-disjoint validation results were available. It reused the opened noise and therefore adds no source-disjoint validation cohort. It completed 24 baseline records and 144 variants on the same 12 injection contexts: two structured waveform families, two source $h_{\mathrm{rss}}$ levels, and original, reversed, and extra-delay forms. The source levels were $10^{-21}$ and $10^{-20}\,\mathrm{Hz}^{-1/2}$, not matched network SNR values. Both families used a 256 Hz carrier, with compact packets contained within the last four seconds of each context.

<div id="tab:p2_controls">

| Form                  | correlation ratio above | Energy above | correlation ratio upward | Energy upward |
|:----------------------|----------:|-------------:|-----------:|--------------:|
| Original              |   $48/48$ |      $21/48$ |    $40/48$ |       $17/48$ |
| Time reversed         |   $48/48$ |      $21/48$ |    $40/48$ |       $17/48$ |
| Extra detector delays |   $38/48$ |      $21/48$ |    $30/48$ |       $17/48$ |

Structured-packet exceedances and matched-baseline upward crossings at unchanged cuts. Each row contains 48 variants on shared noise; no independent-trial or equal-FAR interpretation is implied. All downward crossings were zero.

</div>

For originals, the paired gain was $\Delta J=(40-17)/48=23/48$. Each original family produced $24/24$ correlation ratio exceedances; energy produced $11/24$ for the phase-coded packet and $10/24$ for the phase-related packet train. However, the extra-delay phase-coded packets also produced $24/24$ correlation ratio exceedances. The corresponding packet-train count was $14/24$. Only ten of the 48 matched original/extra-delay pairs were original-positive and extra-delay-negative for correlation ratio. The structured-packet extension therefore extends the measured fixed-cut response while revealing limited timing specificity for these structured challenges. Its binding outcome is a completed descriptive extension; the source-disjoint validation no-go decision is unchanged.

Accepting a consistently time-reversed signal is compatible with generic unmodeled burst sensitivity, because the reversed waveform can remain coherent between detectors. Its acceptance is not, alone, a failure of generic burst detection. It does mean that the tested threshold decisions have not validated time orientation, message content, or controlled origin. Similarly, maximizing correlation over a physically allowed lag interval places the selected lag inside that interval by construction; it does not prove that the actual signal arrival times obey one common-source geometry. Selecting the maximum pair in a three-detector network does not impose a common sky solution on all detectors.

<figure id="fig:p2">
<img src="figures/P2_DUYARLILIK_VE_KONTROLLER.png" />
<figcaption>Structured-packet threshold responses on previously examined noise. The right panel subtracts contributions from matched baselines already above their cuts. Complete original-signal response coexists with high acceptance of over-delayed copies. Variants share noise and are not independent trials.</figcaption>
</figure>

# Physical-source models and detector projection

Two explicitly limited Newtonian sources connect physical parameters to measured response. Source amplitudes follow from mass and distance; they are not subsequently normalized to a chosen $h_{\rm rss}$. Full source histories are retained in the preceding 64-s reference and four-second target. The source derivations, conservation checks and approximation bounds are given in the scientific supplement.

The accelerated-source calculation is a nonrelativistic specialization of published rocket/exhaust bookkeeping (Sellers et al. 2022), distinct from the historical constant-mass reference. A rocket of initial mass $M_0$ moves along one axis, ejecting mass ballistically at fixed backward relative speed $u$. Its prescribed velocity is $v=v_0+\Delta v\,g[(t-t_0)/T]$, where $g(x)=10x^3-15x^4+6x^5$ inside the burn and equals zero or one outside. Newtonian mass and momentum conservation give $$M(t)=M_0e^{-[v(t)-v_0]/u},\qquad -\dot M=\frac{M\dot v}{u}.
 \label{eq:rocket-mass}$$ For observer inclination $\iota$ and polarization angle $\psi$, subtracting the constant pre-burn strain yields the leading quadrupole memory $$\begin{pmatrix}\Delta h_+\\\Delta h_\times\end{pmatrix}
 =\frac{2Gu^2[M_0-M(t)]}{c^4D}\sin^2\iota
 \begin{pmatrix}\cos2\psi\\\sin2\psi\end{pmatrix}.
 \label{eq:rocket-polarizations}$$ The post-burn offset is retained. This leading slow-motion ledger requires an energy supply; it is not a relativistic propulsion or feasible-engine model. Its whole-burn radiated energy follows the general polarization-flux convention (Sutton 2013), without applying finite-burst $h_{\rm rss}$ formulas to permanent memory.

The declared parameters are $M_0=1.89813\times10^{27}$ kg, $v_0=0.001c$, $\Delta v=0.001c$, $u=0.01c$, and $T=0.01,0.1,10$ s. Burns are centred at context time 66 s. The ten-second burn begins at 61 s and therefore changes the reference; strain also continues beyond the observed record. At the fixed geometry the asymptotic $h_+$ memory is $6.0060\times10^{-20}$. The processed target $h_+$ power fractions in 64–768 Hz are respectively $3.5210\times10^{-4}$, $5.9234\times10^{-10}$ and $2.6078\times10^{-13}$. These are windowed strain-power fractions, not fractions of total radiated energy.

The second source comprises equal compact masses $m=10^{24}$ kg in a circular orbit of component radius $a$. It is equally compatible with a natural compact binary. With orbital phase $\phi$, $$\begin{aligned}
 \Omega^2&=\frac{Gm}{4a^3},\qquad f_{\rm GW}=\frac{\Omega}{\pi},\qquad
 h_0=\frac{8Gma^2\Omega^2}{c^4D},\label{eq:binary-kepler}\\
 h_+&=-\frac{h_0}{2}(1+\cos^2\iota)\cos2\phi,\qquad
 h_\times=-h_0\cos\iota\sin2\phi.\label{eq:binary-polarizations}
\end{aligned}$$ A fixed $2\psi$ polarization rotation is then applied. The chosen GW frequencies are 64, 256 and 512 Hz. The largest omitted 68-s inspiral phase is approximately $0.00183$ rad. Persistence in both intervals gives a source-only target/reference energy ratio near unity; this is a normalization diagnostic, not noisy-data detection efficiency.

Both models use $D=0.01$ pc, $\iota=\pi/3$ and $\psi=0.2$ rad. Detector signals share one source geometry, $$h_I(t)=F_I^+h_+(t-\tau_I)+F_I^\times h_\times(t-\tau_I).$$ The finite test uses four already-open contexts, six fixed source settings, and original/extra-delay projections: 48 variants. Parameters, controls and cuts were fixed before these new scores. This conditional response does not supply an artificial-origin inference, population efficiency, distance exclusion or event-rate bound.

<figure id="fig:physical_sources">
<embed src="figures/PHYSICAL_SOURCE_MODELS.pdf" />
<figcaption>Specified source waveforms before real detector noise is added. The rocket memory continues beyond the record, and the long burn affects the reference. The compact pair exists in both reference and target. These are source predictions at the declared mass, distance and orientation, not detected signals or source-population bounds.</figcaption>
</figure>

## Physical-source response in detector noise

The experiment completed the 24 unchanged baseline replays and all 48 prespecified physical-source variants. The latter comprise six source configurations, their original and extra-delay copies, and four already-open noise contexts (two in each epoch). These are four reused source blocks, not a new independent validation sample. All mass, motion, distance, orientation and timing parameters were fixed before the new scores; the source distance was $D=0.01\,\mathrm{pc}$ in every configuration. The amplitude scaling, thresholds and score implementations were unchanged.

<div id="tab:p3actual">

| Source configuration             | correlation ratio orig. | correlation ratio delay | Orig. up/down | Delay up/down | energy ratio |
|:---------------------------------|:---------:|:---------:|:-------------:|:-------------:|:------:|
| Rocket, $T=0.01\,\mathrm{s}$     |    4/4    |    1/4    |      3/0      |      1/1      |  0/4   |
| Rocket, $T=0.1\,\mathrm{s}$      |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Rocket, $T=10\,\mathrm{s}$       |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $64\,\mathrm{Hz}$  |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $256\,\mathrm{Hz}$ |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $512\,\mathrm{Hz}$ |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |

Physical-source fixed-cut exceedances. The up/down columns count correlation ratio upward/downward threshold transitions relative to matched uninjected baselines, out of four trials per row and control. One of the four selected baselines was already correlation ratio positive; therefore 4/4 above-cut outcomes for the shortest rocket contain three new crossings. The energy ratio also remains below its cuts for all 24 delayed copies. Fractions describe this finite grid, not population efficiency.

</div>

For the $0.01\,\mathrm{s}$ rocket–exhaust memory source, the original correlation ratio scores are $1.8697$, $2.8164$, $2.5991$ and $2.5063$, against matched baseline scores $1.1936$, $1.1460$, $1.0266$ and $1.2475$. The short source thus produces a positive, parameter-explicit response in both epochs. Its delayed copy is still accepted in the first O4a context, where it creates an upward crossing; the formerly positive last O4b context moves below the cut. This gives one upward and one downward crossing for the four delayed short-rocket trials, with zero net lift. Acceptance of this delayed copy retains the known timing-specificity limitation.

The $0.1$ and $10\,\mathrm{s}$ rockets and all three persistent compact-pair configurations produce no new crossings in either method at the specified parameters. Their correlation ratio exceedances all inherit the same positive O4b baseline. This is compatible with the source-only diagnostic showing strong loss of processed in-band power for longer memory rises, and with the target/reference normalization of a source present throughout the record. It does not establish that reference normalization alone causes every noisy non-crossing. The full physical source was retained: all 24 compact-pair units and eight long-rocket units alter the 64-s reference, for 32/48 units in total; the remaining 16 short-rocket units leave it bitwise unchanged.

Across the 24 original units, the correlation ratio has 9 exceedances, six matched-baseline exceedances, three upward crossings and no downward crossings. The 24 delayed units have six exceedances, six matched-baseline exceedances, one upward and one downward crossing. The energy ratio has no exceedances or crossings in either group. The original-group descriptive net-lift difference is $J_{\rm corr}-J_{\rm energy}=3/24=0.125$; it is not an equal-FAR performance claim or a significance test. These injections establish the explicit source–detector–measured-response link for two stated Newtonian source approximations, with strongest response in the shortest rocket case. They are not observed celestial events, an engineered-origin inference, a range/rate exclusion, a general detection-efficiency estimate or a demonstration of engineering feasibility. The earlier noise-guard failure and structured-packet timing limitation remain unchanged.

# Broad-lag timing diagnosis

Inter-detector correlation over a physical travel-time window is an established waveform-consistency tool, rather than a new detector concept (Cadonati 2004). Joint network approaches use a common sky-dependent response to two source polarizations, together with coherent, incoherent or null-space consistency quantities (Sutton et al. 2010; Klimenko et al. 2016). The declared envelope delay diagnostic is designed to supplement the present pairwise statistic; it does not implement those complete network analyses or classify a signal’s origin.

The following is a mathematical observation about the present observable, not a newly measured result. For a sufficiently narrowband packet, a cross-correlation can be approximated by a slowly varying overlap factor times $\cos(2\pi f_0\tau+\phi)$. Taking its absolute value permits approximately half-cycle-spaced maxima. At $f_0=256$ Hz, that spacing is $1/(2f_0)=1.953125$ ms, or eight samples at 4096 Hz. A maximum selected inside a physical lag window can therefore coexist with a much larger displacement of the packet envelopes. Modulated finite packets need not obey that approximation exactly.

An additional network limitation follows directly from the response-matrix dimensions. For two detectors and two unrestricted polarizations, a full-rank $2\times2$ response spans the whole two-detector data space; the orthogonal null space is then zero-dimensional. Consequently, an unrestricted two-detector null-energy construction alone cannot supply a nontrivial consistency rejection. Antenna-pattern degeneracy, conditioning and additional signal assumptions require explicit treatment. This dimensional observation follows the response and projection formulation in Patrick J. Sutton et al. (2010); it is not an implementation of that pipeline.

The broad-lag diagnosis is a separately declared, completed development-only diagnostic on already-open cached contexts. Its envelope definition, conditioning, padding, lag support and treatment of ties or uninformative inputs were fixed before its new measurements in the accompanying protocol. Every active pair is reported, including the pair producing the original network maximum. An approximately constant carrier envelope has no localized arrival time; a common taper can introduce artificial envelope structure, and noise can move a peak. Such cases must remain explicitly ambiguous or uninformative. The protocol reconstructed all existing declared records: 24 unmodified baselines, 144 structured-packet variants and 48 physical-source variants, for 216 diagnostic records. Each reconstructed correlation ratio/energy ratio score and its full saved record had to match exactly before any new curve was committed. The raw signed linear correlation is evaluated at integer lags from $-1433$ to $1433$ samples, approximately $\pm0.35$ s, using the same full-vector normalization. This support covers the largest declared extra delay, $0.30$ s, plus the largest physical cap. The envelope diagnostic uses centered squared analytic-signal magnitude on the same already-windowed whitened target. No new smoothing, near-peak threshold or fitted acceptance cut is introduced. Exact maxima and ties are retained; zero centered-envelope energy is returned as undefined. The old physical-lag maximum and the broader curves are all reported, without turning a peak location into a new physical-pass decision.

## Completed broad-lag diagnosis on reopened data

The diagnosis evaluated all 216 registered diagnostic records: 24 unmodified baselines, 144 structured-packet variants and 48 physical-source variants. It retains 432 detector-pair records, each with a signed raw and centered analytic-envelope-power correlation curve over the fixed $\pm1433$-sample support (approximately $\pm0.35$ s). The original correlation and energy scores and their lineage were required to match the saved records before each new curve was evaluated. The original thresholds and decisions were not changed.

For each record we identify the pair that supplied the *old* target network maximum, before considering its new broad-lag curve. This pair was unique in all 216 records. The broad-lag summary below counts whether the absolute broad maximum in that same pair lies outside its physical cap. All returned curves are numerically defined and have a unique exact floating-point maximum; neither fact establishes that their peak is an unambiguous physical arrival time. The curve categories are descriptive measurements, not a new acceptance decision.

<div id="tab:p4actual">

| Records                    | $n$ | Old correlation ratio above | Raw peak outside | Envelope peak outside |
|:---------------------------|----:|--------------:|-----------------:|----------------------:|
| Unmodified noise           |  24 |             4 |               21 |                    17 |
| Packets, original          |  48 |            48 |                4 |                     9 |
| Packets, reversed          |  48 |            48 |                3 |                    10 |
| Packets, extra delay       |  48 |            38 |               48 |                    48 |
| 10-ms rocket, original     |   4 |             4 |                0 |                     0 |
| 10-ms rocket, extra delay  |   4 |             1 |                4 |                     4 |
| Other sources, original    |  20 |             5 |               15 |                    15 |
| Other sources, extra delay |  20 |             5 |               15 |                    15 |

Broad-maximum locations in the unique pair supplying each old target correlation ratio maximum. “Outside” refers to the complete exact broad-maximum set lying beyond that pair’s integer physical cap. Old correlation ratio counts are unchanged fixed-cut exceedances, including already-positive baselines. Rows share noise and sources and are not independent trials. The physical-source study “other sources” are the two longer rocket burns and three persistent compact-pair configurations.

</div>

All 48 over-delayed packet copies have both broad maxima outside the physical cap in the original score-determining detector pair. This includes all 38 copies that previously exceeded the correlation ratio cut. Every active raw-correlation pair is outside in all 48 records; every envelope pair is outside in 47 of 48 records. The one exception is a nonscore-determining detector pair in a weak phase-coded case. Thus this finite failure mode is not removed by simply choosing a different pair when interpreting the old winning statistic.

The four original short-rocket records have both broad maxima inside their original score-determining detector pair’s cap, while all four extra-delay copies have both maxima outside. The sole extra-delay copy accepted by the old correlation ratio cut is the first O4a context: its raw broad maximum is at $-152.588$ ms and its envelope maximum at $-149.902$ ms, compared with the declared injected H1–L1 delay of $-151.831$ ms and a light-travel bound of approximately $10.013$ ms. These are descriptive locations in injected noisy records, not a new source localization or an uncertainty-qualified time-of-flight estimate.

The diagnostic also demonstrates why a new veto cannot be certified merely by observing the delayed copies. Four physically projected original packets have their raw broad maximum outside the cap; nine have an envelope maximum outside. All four raw exceptions are weak injections in O4b with L1–V1 as the original score-determining detector pair. Their maxima are $27.588$ or $29.541$ ms, close to but outside that pair’s $26.448$-ms light-travel bound; their physical-cap maximum remains 0.9793–0.9992 times the broad maximum. Polarization, noise and finite-window processing affect the location selected by absolute correlation. An envelope maximum likewise remains subject to the shared Hann-window limitation established above.

The protocol also retained the ratio of the raw physical-cap maximum to the raw broad maximum. Its observed range is $[0.9793221059,1]$ for the 48 original packets and $[0.0148484340,0.7466750320]$ for the 48 extra-delay copies; their medians are 1 and 0.1982606041. These nonoverlapping finite-panel ranges are a descriptive finding, not a threshold selected or applied by this study. They do not establish separation from arbitrary instrumental glitches or transfer to unopened source blocks. A rule based on this ratio would be a new method requiring a separately fixed criterion and validation.

For the other five physical-source configurations, the broad-maximum locations in each original score-determining detector pair follow the corresponding matched-noise locations exactly. Together with their absence of new threshold crossings, this supports treating those maxima as timing-uninformative for the injected source at these parameters; it is not a measurement of that source’s delay. The raw broad-peak locations are inside the original score-determining detector pair’s cap for only three of 24 unmodified-noise records, and the envelope locations for seven of 24. These noise categories are not population false-alarm probabilities.

The broad-lag diagnosis therefore supplies a measured explanation of the finite short-lag specificity limitation: high local correlation and a physically allowed local maximizer can coexist with a stronger, substantially over-delayed correlation maximum. It does not implement or validate a replacement veto, common-sky fit, physical origin classifier or search-level calibration. The failed new-source noise guard, original packet and physical-source outcomes and the incomplete global tail campaign remain unchanged.

<figure id="fig:p4_p2_delays">
<embed src="figures/P4_ACTUAL_P2_DELAYS.pdf" />
<figcaption>Saved broad-lag curves for the first O4a extra-delay correlation ratio-positive phase-coded packet at the higher declared strength with matching original projection and unmodified noise. All use the first declared O4a H1–L1 context; exact record identifiers are given in the supplementary figure provenance. Panel A shows absolute normalized correlation of the fixed whitened targets; its inset resolves the old physical-lag interval. Panel B shows signed centered analytic-envelope-power correlation. The declared source lag is <span class="math inline"> − 151.831</span> ms (dashed), known injection metadata rather than an estimated arrival time. The delayed copy’s broad raw maximum is <span class="math inline"> − 152.344</span> ms while its old accepted short-lag maximum is <span class="math inline"> + 9.521</span> ms. Its envelope maximum is <span class="math inline"> − 125.977</span> ms. Shared taper structure and noise can shift envelope peaks; no new acceptance criterion or validated timing estimator is inferred.</figcaption>
</figure>

<figure id="fig:p4_p3_delays">
<embed src="figures/P4_ACTUAL_P3_DELAYS.pdf" />
<figcaption>Saved broad-lag curves for the first extra-delay correlation ratio-positive 10-ms rocket–exhaust memory model with matching original projection and the same unmodified noise as in Fig. <a href="#fig:p4_p2_delays" data-reference-type="ref" data-reference="fig:p4_p2_delays">3</a>. Panel definitions and deterministic selection follow that figure. The declared delayed-source lag is <span class="math inline"> − 151.831</span> ms; the broad raw and envelope maxima occur at <span class="math inline"> − 152.588</span> and <span class="math inline"> − 149.902</span> ms, respectively, while the accepted old short-lag maximum is <span class="math inline"> + 8.545</span> ms. These are illustrative saved-curve diagnostics, not a measured population false-alarm probability, independent validation or a source-origin claim.</figcaption>
</figure>

# Randomized real-record survey and bounded follow-up

## fixed sample and interpretable measurements

A subsequent non-neural survey audited all 4096 preselected H1 detector-time records: 2048 from O4a and 2048 from O4b. The sampling unit was one four-second target and its complete preceding 64-second support at 4096 Hz. A reproducible Fisher–Yates permutation with seed 20261030 selected 128 distinct physical source blocks per run and 16 distinct targets per source without replacement. Rejection sampling removed integer-modulo bias. The eligible metadata frame contained 136 O4a and 203 O4b source blocks after the declared whole-source and protected-interval exclusions. The 4096 support intervals were nonoverlapping. Selection preceded raw access, full-support quality and feature scoring; a quality rejection did not trigger a replacement. The inclusion probability for a record in source $s$ and run $r$ was $(128/N_r)(16/M_s)$, where $M_s$ is the source's eligible target count. This probability describes the pre-quality metadata frame, not a quality-conditioned population.

Whole-source exclusions retained the original controlled-benchmark test, foreground and known H3 held-out protections, together with the 20 most recently touched primary H1 source blocks. Some other historically opened development or calibration source containers remained eligible and were annotated. This is an exploratory, finite survey of that declared H1 frame, not a globally unopened validation sample or a representative network search. Random selection, source grouping and nonoverlap do not establish independent detector noise.

The source-group split was fixed from the complete selected plan, before quality outcomes: 2432 training, 800 calibration and 864 test targets. Reference fitting used only valid training records, with separate O4a/H1 and O4b/H1 featurewise medians and MAD scales, an interquartile fallback and omission of zero-scale dimensions. The score was the largest absolute standardized deviation among the active fixed features. The calibration summaries and the eight highest test ranks were exploratory; eight was a review budget rather than a detection threshold. Both run-specific references retained 18 of the 19 extracted dimensions: carrier-ACF peak lag had zero training MAD and IQR and was omitted by the fixed degeneracy rule. This was not a post-ranking feature removal.

The 19 features retain local and absolute powers, transient concentration and shape, reference-normalized spectral concentration and subband fractions, and signed carrier and analytic-envelope autocorrelation peaks and lags. A 64–768-Hz Butterworth bandpass, specified by SciPy's butter with N=4 and output=sos (four second-order sections), was applied forward and backward to the complete 68-second array, using the fixed 27-sample odd extension. It is a finite-record conditioning rule, not a strict hard band limit. Periodogram/Welch spectral summaries retained bins $64\le f<768$ Hz; the reference consisted of 16 nonoverlapping four-second segments. The reference-PSD regularizer was fixed at $10^{-12}$ times its largest retained bin. Carrier ACF lags covered $1/768$–$1/64$ s, and envelope ACF lags 0.08–1 s. These ACF summaries are not estimated source periods or evidence of coding.

## Complete selection accounting and measured cost

The execution produced 4020 finite 19-feature vectors, 76 quality rejections and 0 input rejections; no selected record remained unresolved. Each source file was checked against its publisher checksum; the selected strain arrays and numerical definitions were retained for reproduction. Valid-strain, category-2 burst-quality and the four declared hardware-injection exclusion conditions were checked over all 68 seconds. The continuous-wave hardware-injection flag was recorded without being used as an exclusion; it cannot be used to describe this sample as CW-injection-free or to identify the cause of a particular peak.

| Run / detector | Selected | Finite-feature records | Quality rejected | Input rejected |
|:---|:---|:---|:---|:---|
| O4a/H1 | 2048 | 2016 | 32 | 0 |
| O4b/H1 | 2048 | 2004 | 44 | 0 |

The 4020 valid targets provide 16080 s of summed four-second H1 target exposure. Their 273360 s of summed processing support is a different quantity; intervals between sampled targets are not surveyed exposure. Valid training, calibration and test denominators were 2384, 786 and 850, respectively. The score timeline below shows the measured rank values at the actual GPS coordinates. The supplementary ACF displays retain the same observation gaps and excluded records.

The fixed-budget review ranks and their score-driving feature were:

| Review record | Run | Target GPS | Score | Largest-deviation feature |
|:---|:---|:---|:---|
| O4a | 1384223040 | 119.920 | spectral entropy |
| O4b | 1416849600 | 57.730 | envelope acf lag s |
| O4b | 1416849120 | 56.718 | envelope acf lag s |
| O4b | 1416850000 | 56.443 | envelope acf lag s |
| O4b | 1418424800 | 55.891 | envelope acf lag s |
| O4b | 1418647040 | 55.891 | envelope acf lag s |
| O4b | 1418647120 | 55.891 | envelope acf lag s |
| O4b | 1418647200 | 55.891 | envelope acf lag s |

A large robust deviation identifies departure from the finite training reference. Its scale is not a calibrated tail probability, and a score-driving feature does not identify an instrumental or celestial cause.

The eight review records came from 4 physical source-time groups. For 7 records, the largest standardized deviation was the envelope-ACF peak-lag coordinate, at lags 0.863525391–0.878173828 s. Of these, 4 shared the exact discrete lag 0.863525390625 s and the same score 55.890673; these were not maxima pinned to the 1-s search boundary. The highest-ranked record, GPS 1384223040, was instead driven by spectral entropy. This concentration and the exact ties describe the fixed feature/ranking behavior, not eight independent anomalies or an inferred source period. The feature definition and ordering were not retuned after inspecting them. The seven O4b review ranks did not exceed the separate finite calibration source-group cut used by the injection assay; review ranking was not conditioned on a cut crossing.

The conditioned, non-reference-whitened target periodogram peaked at 508.25 Hz for GPS 1384223040 and 510.75 Hz for all seven O4b review records. Substantial narrowband power was also present in their reference spectra. The numerical PSD floor regularized no retained bin in any of these eight records. These measured spectral facts do not attribute the structures to a calibration line, hardware injection, environment or celestial source; no release-specific line-list match was performed.

On the review host, summed local reads and feature extraction took 369.47 s, including 214.13 s of feature calculation. The recorded mean local record cost was 0.0939 s; source-file acquisition, integrity checks, interruptions and post-processing are separate costs. The elapsed interval from the first campaign creation to the final selected-record record was 89.87 min, including operational interruption. Source grouping amortized each whole-file transfer across its 16 targets; this throughput was not obtained by treating a synthetic scheduler task or one cached feature as a completed full-network search. The execution used CPython 3.12, NumPy 2.3.5, SciPy 1.17.0 and h5py 3.16.0 with float64 features and one numerical thread. This is a new host CPU execution, distinct from the historical Windows neural runtime.

<figure id="fig:cpu4096_score">
<img src="figures/CPU4096_SCORE_TIMELINE.png" />
<figcaption>Actual random-sample H1 feature scores for 4020 quality-accepted targets, shown at their actual GPS separations in each run. Training-reference, calibration and test roles were fixed by source group before raw access and scoring. Stars identify the fixed top-eight test review ranks; they are not eight detections. Excluded selected records have no score, and gaps do not add observed exposure. The vertical scale is symmetric logarithmic.</figcaption>
</figure>

## Source-held-out phenomenological response

A separately fixed assay selected one target in each of 12 test source groups, six per run, before their scores were opened for the assay. It planned 144 injections: a 256-Hz sine-Gaussian, a phase-coded four-packet sequence, a smooth turning chirp and a persistent 256-Hz line, each at target-band RMS ratios 0.5, 2 and 8 relative to the same unmodified noise. Every signal was added to the full 68-second strain before conditioning; signal in the reference was retained. These are specified phenomenological sensitivity probes, not physical transmitter, RAMAcraft or warp-source waveforms. The assay completed 144 variants and recorded 0 preselected variants as ineligible without substitution. Each usable noise context was replayed to the main archived raw-array identity and bitwise-equal 19-feature values before any variant was accepted.

The robust feature score and the H1-local energy ratio log-power ratio used their own calibration source-group maxima. The nominal $q=0.05$ cut was the $\lceil(G+1)(1-q)\rceil$th ordered maximum for $G$ calibration groups, with strict exceedance. This does not establish equal physical false-alarm rates, exchangeability or group independence. Context new crossings required an unmodified context at or below its method's cut and the injected context above it. The additional source-group endpoint, fixed before the assay, replaced only the selected target within the original group's other valid records and required the entire unmodified group maximum to be below its cut. Ordinary exceedances and already-positive baselines were retained.

Across 144 variants in 12 fully eligible source contexts, context new crossings were 96/144 for robust feature ranking and 69/144 for energy ratio; source-group new crossings were 87/144 and 69/144. The equal-context mean difference in context new-crossing fraction, robust feature ranking minus energy, was 0.1875. The corresponding source-group new-crossing difference was 0.1250 across 12 contexts. These paired finite-context contrasts do not supply a population confidence interval or matched-FAR superiority claim. At RMS ratio 2, the turning chirp gave 6/12 crossings for robust feature ranking versus 11/12 for energy ratio, so the sign of the paired fixed-cut response contrast depended on waveform family. The full-support persistent 256-Hz line gave 0/36 and 0/36 new crossings, respectively. This finite control does not establish sensitivity to persistent GW beacons. The injection-response figure below reports both endpoints by family and strength; the source-group noise responses accompany them in the supplement.

A subsequent saved-score audit retained the registered cuts and all 144 assay records. Both methods had the same twelve baseline-negative contexts at the context endpoint. At the source-group endpoint, GPS 1384223440 was already positive for robust feature ranking but not energy. A post-hoc common-negative subset excludes that same context from both methods and gives 87/132 versus 63/132 new group crossings in eleven contexts. Its equal-context contrast is $2/11$; because five contexts are O4a and six are O4b, its equal-run contrast is instead $3/16$. The original 87/144 versus 69/144 endpoint remains unchanged. These opportunity and weighting checks do not establish equal population false-alarm rates.

The accompanying post-hoc calibration-rank table reports every common deterministically attainable exceedance count through 5/25, then evaluates the same test groups and assay contexts. Strict inequalities and actual score ties are retained; O4b 3/25 is not jointly attainable and is omitted. test scores never select the cuts. All 22 rows are released without choosing a favorable operating point. These retained-score summaries clarify the comparison, rather than creating another confirmatory search.

<figure id="fig:cpu4096_injections">
<img src="figures/CPU4096_INJECTION_RESPONSE.png" />
<figcaption>Prespecified phenomenological injections on the same H1 noise contexts. Counts give new crossings divided by the twelve planned usable source contexts for each family and amplitude; source-group baselines that are already positive cannot create a new crossing. Top panels use the selected context endpoint at the fixed source-group cut; lower panels use the separately fixed source-group maximum endpoint. Robust feature ranking and H1-local energy share injected strain but have separately calibrated finite cuts. Signals were added before full-support conditioning, and repeated variants share noise. These fractions are not physical detection efficiencies at an established FAR.</figcaption>
</figure>

## Predeclared top-rank timing review

The fixed review rule yielded 8 test records. All received a bounded follow-up disposition: 7 had the full requested coeval detector coverage, and 1 had available-pair diagnostics with incomplete requested coverage. Other access or quality outcomes remain explicit in the supplementary table; absence from a metadata index was not interpreted as detector absence. H1 inputs and baseline features were revalidated against the survey records, and each available coeval detector retained the same full-support source-integrity and quality checks.

The pair review reused the exact pinned broad-lag raw and centered analytic-envelope-power correlation mathematics of the earlier broad-lag study diagnosis. Its conditioning is the earlier symmetric-Hann 17-segment, 64–768-Hz inclusive FFT rule, distinct from the new feature screen's Butterworth/PSD convention. The broad interval was $\pm1433$ samples at 4096 Hz; the physical H1–L1, H1–V1 and L1–V1 caps were 41, 111 and 108 samples. Exact ties and the intersection of the full maximizing set with each physical cap were retained. No old correlation ratio acceptance cut was transported to the new candidates. Pair maxima are descriptive timing diagnostics, not a common-sky fit, a validated rejection criterion, a calibrated candidate significance or an origin classifier. Among 20 measured coeval pairs, the exact broad maximizing set intersected the physical cap for 1/20 raw curves and 2/20 envelope curves. The envelope broad maxima lay wholly outside the H1–L1 cap for 8/8 H1–L1 pairs. These measured timing outcomes limit a simple common-transient interpretation but do not supply a validated veto or prove the absence of a GW. For GPS 1418424800, the official metadata identified the expected V1 source but did not provide its required publisher checksum; the source was not downloaded, and its H1–L1 diagnostic remains separately available.

# A fixed phase-coded packet and a conditional amplitude bound

## Signal model, detector response and finite timing domain

To obtain a quantitative negative statement for a specified in-band morphology, a separate calculation reused the 12 H1 raw-strain contexts selected before the preceding injection assay. These comprise six targets in each run and 12 source-time groups. The strain-array identities were checked before projection. The family, statistic, timing domain and numerical budget were fixed before the new projection values were calculated. The already examined noise and the exploratory choice of this family remain explicit; this is not a new blinded confirmation. Neither the 4096-record counter nor the historical full-search counter was changed.

The received strain is a four-packet, binary-phase waveform,
$$h_{H1}(t)=A_{\rm det}e_\tau(t)\sin(2\pi\,256t+\phi),\qquad
e_\tau(t)=\sum_{j=1}^{4}c_j\exp\!\left[-\frac{(t-\tau-t_j)^2}{2\sigma^2}\right],$$
with $c=(+1,-1,-1,+1)$, $t_j=(0.5,1.5,2.5,3.5)$ s and $\sigma=0.04$ s. For a linearly polarized source and a fixed antenna factor during the packet, $h_{H1}=F_+h_+$, so $A_{\rm det}=|F_+|A_+$ with a sign absorbed into $\phi$. The reported endpoint concerns the public released H1 strain; no additional amplitude-calibration systematic is inferred. An intrinsic source bound requires a specified nonzero $F_+$, and a blind direction supplies none. The waveform is a phenomenological coded-emission hypothesis, not a demonstrated technological transmitter or a decoded message.

Arrival offsets cover $\tau\in[-0.25,0.25]$ s at native-sample spacing $1/4096$ s, giving 2049 grid points in each context. A conservative mismatch certificate extends the endpoint to continuous arrivals in that interval. The 12 four-second targets contain 48 s of samples; the allowed pulse-train anchor intervals total only 6 s and are separated in GPS time. They do not create a continuous survey. Analytic Gaussian tails were retained: the linear projection uses the raw interval $[-2,4)$ s within each complete 68-s input, and does not clip the signal at the target start. No reference-PSD estimate, whitening, learned model or nonlinear re-ranking enters this new statistic.

At each arrival, the two raw sine/cosine templates form $T_\tau$, with Gram matrix $G_\tau=T_\tau^\mathsf{T}T_\tau$ and least-squares coefficient vector $z_\tau=G_\tau^{-1}T_\tau^\mathsf{T}x$. Multiplication of both templates and strain by $\sqrt{dt}$ leaves the coefficients unchanged and gives the Gram units used below. The statistic $M$ is the largest $\|z_\tau\|_2$ over the 12 contexts and all arrivals. It is a coefficient amplitude in strain units, not a matched-filter SNR or calibrated detection probability. Two fixed wrong-code projections provide descriptive controls only.

<figure id="fig:phase_packet_observed">
<img src="figures/PHASE_PACKET_TEMPLATE_AND_PROJECTIONS.png" />
<figcaption>Specified packet and measured raw-strain projection amplitudes. Panel (a) retains the carrier and signed four-Gaussian envelope. Panel (b) compares the original code with two declared wrong-code controls over the same twelve contexts and arrival interval. The dashed line is the maximum for the specified code. These control amplitudes are not false-alarm probabilities or rankings of source origin. Context-to-GPS identities are provided in the fixed protocol.</figcaption>
</figure>

## Phase-ensemble coverage and measured endpoint

The amplitude model assumes at most one packet in the declared union and a carrier phase uniform on $[0,2\pi)$ independently of additive nuisance, model choice, interval selection and the fixed analysis. At the true arrival on the grid, $z=b+A_{\rm det}(\cos\phi,\sin\phi)^\mathsf{T}$. For every fixed noise projection $b$, the circle-intersection argument in the supplement gives $P_\phi(\|z\|\le r)\le\arcsin(r/A_{\rm det})/\pi$ when $r\mathrel{<}A_{\rm det}$. Taking the maximum over more fixed search points makes the upper endpoint more conservative; this argument does not produce a detection false-alarm probability.

For continuous arrival offsets, the certified response factor is at least $0.9938264$; the calculation used the smaller fixed value $\kappa=0.99$. Full-packet strain energy satisfies $h_{\rm rss,H1}^2\le0.142\,\mathrm{s}\,A_{\rm det}^2$. With $\alpha=0.1$ and a $10^{-8}$ numerical inflation of the measured maximum, the endpoint is
$$U_A=\frac{M(1+10^{-8})}{0.99\sin(0.1\pi)},\qquad
 U_h=U_A\sqrt{0.142\,\mathrm{s}}.$$

The observed maximum was $M=1.89915451346\times10^{-23}$, at the O4a target starting at GPS 1384223440 with arrival shift $-0.066162109375$ s. This gives $U_A=6.20787188565\times10^{-23}$ and
$$\boxed{U_h=2.33930537030\times10^{-23}\,\mathrm{Hz}^{-1/2}}.$$

The uncoded control maximum was $1.67269193769\times10^{-23}$ and the alternating-code control maximum was $2.71467562583\times10^{-23}$. The latter exceeds the specified-code maximum, so these projections do not show a unique preference for the target code. No significance or technological interpretation is assigned to these descriptive comparisons.

Under the stated random-phase, one-packet model, $U_h$ is an upper confidence endpoint with at least 90% phase-ensemble coverage throughout the declared timing domain. It is not a posterior probability for the current source amplitude and is not uniform over every fixed phase. A fixed noise waveform equal to the negative of a fixed-phase signal is an explicit counterexample to an all-phase absence claim. The result therefore limits this received packet model in the specified data, rather than excluding technological sources generally.

A secondary calculation used $\alpha=0.025$ and gave $9.21352849850\times10^{-23}\,\mathrm{Hz}^{-1/2}$. This is a more conservative phase-ensemble endpoint and an illustration of allocating a four-family error budget. It does not adjust for every historical method choice or establish a completed simultaneous analysis of the other families.

## Injection response, numerical checks and computational cost

The same fixed statistic was evaluated for 57 coefficient amplitudes from $10^{-25}$ to $10^{-18}$, 32 evenly spaced phases and five arrival offsets in each context: 109440 superpositions on 12 shared backgrounds. Exact linear responses accelerated these evaluations; no variant was counted as a new independent noise observation. Signals used fixed coefficient $A_{\rm det}$ rather than phase-dependent $h_{\rm rss}$ renormalization. A strict comparison to the numerically guarded observed maximum defined the full-search statistic-exceedance fraction.

The first tested amplitude at which both reported crossing fractions reached 0.9 was $A_{\rm det}=3.16227766017\times10^{-23}$, corresponding to approximately $h_{\rm rss,H1}=1.19078254972\times10^{-23}\,\mathrm{Hz}^{-1/2}$. The full-search statistic exceeded the threshold in 1876/1920 superpositions, or 0.9770833. Requiring the projection at the actual injected arrival to exceed it gave 1866/1920, or 0.971875; the corresponding average analytic continuous-phase crossing fraction was 0.9726517. The larger full-search count can be driven by a different arrival and is not a localization or detection-recovery rate. At the smallest tested amplitude it already gave 64/1920 exceedances, while the true-location count was zero, illustrating this distinction. These are conditional responses on the retained backgrounds, not the confidence endpoint and not matched-FAR performance measurements. The distinction between response and an amplitude-confidence construction is retained; GW burst analyses likewise state signal-model and efficiency assumptions for their limits (B. P. Abbott et al. 2010).

<figure id="fig:phase_packet_efficiency">
<img src="figures/PHASE_PACKET_EFFICIENCY_AND_BOUND.png" />
<figcaption>Finite injection response and the separate coverage argument. Panel (a) shows the transition region of the released 57-level amplitude grid; its horizontal coordinate is the conservative normalization $A\sqrt{0.142\,\mathrm{s}}$. Blue points require a threshold crossing at the actual injected arrival, whereas the dotted grey curve permits a larger statistic at any searched arrival. The observations share twelve actual noise records; the dashed curve is the mean analytic continuous-phase fraction at the true arrival. The vertical endpoint follows from phase-ensemble coverage, not by relabeling an efficiency crossing. Panel (b) gives the analytic worst-fixed-noise small-projection probability as a function of $A/M$ with the conservative continuous-arrival factor. Neither panel supplies a noise FAR or technological-origin probability.</figcaption>
</figure>

Direct full-68-s injections checked the linear acceleration on 240 comparisons; the largest reported relative discrepancy was below $1.31\times10^{-12}$. A separate entire-grid check had an absolute coefficient discrepancy below $2.91\times10^{-35}$. The measured numerical execution took 15.545 s with peak resident memory 134.09 MiB on the review host, using CPython 3.12.14, NumPy 2.3.5 and one numerical thread. It made no network request, installation or neural call. This is a measured host calculation, not a promised Windows wall-time limit. The protocol, all twelve raw inputs, response arrays, efficiency table and proof-validation program accompany the result.

## A separate conservative envelope over all valid survey targets

A distinct calculation used the stored raw, demeaned four-second target variances in all 4020 valid survey records. It did not run 4020 matched-template searches or replace the twelve-context result. For a virtual four-second projection with the same packet basis, mean removal preserves the certified Gram lower bound $0.14\,\mathrm{s}$. If $v_i$ is the saved variance, Cauchy--Schwarz gives the coefficient ceiling $M_i\le\sqrt{4v_i/0.14}$. Substituting this larger ceiling into the same phase-ensemble construction yields a conservative upper endpoint for one packet at any permitted arrival in any included record.

The largest resulting endpoint was $8.78939530015\times10^{-17}\,\mathrm{Hz}^{-1/2}$, at an O4b target beginning at GPS 1418568960. This is orders of magnitude weaker than the matched result on twelve contexts, because it permits all raw variance to lie in the packet subspace. It is reported without a quality- or score-based removal of that loud record. The 4020 supports retain their original roles and 76 quality rejections remain excluded; no independence assumption, added source exposure, full-search background or rate limit is inferred. This broad-support relaxation and the sharper twelve-context calculation answer different conditional questions and must not be interchanged.

## Relation to standard inference and practical cost

Unknown-phase quadrature filtering and confidence limits derived from the loudest observed statistic are established techniques, rather than new principles introduced here (Jaranowski, Królak, and Schutz 1998; Biswas et al. 2009). Nor is robustness to an unspecified noise-distribution family itself new: Dergachev (2013) developed universal upper-limit statistics for ill-behaved backgrounds. Our result should therefore be read as a reproducible, finite-record application with a different stated coverage ensemble, not as a general replacement for those methods.

The distinction is that the present endpoint randomizes the source carrier phase while conditioning on an arbitrary additive-noise realization. It requires neither a fitted noise probability density nor independent noise records. In exchange, it assumes one member of one fixed waveform family, a uniform carrier phase independent of the nuisance and selection, a fixed linear projection, and a certified continuous-arrival response. Freezing the projection protocol after the records were already inspected does not establish independence of that earlier selection from a hypothetical signal phase; this remains an explicit model assumption. No noise false-alarm probability follows from the construction. The four-Gaussian waveform was specified in the 30 October H1 secondary-assay plan; it differs from the earlier two-second, eight-chip structured transient used to diagnose delay specificity.

The cost of this assumption tradeoff is measurable. The 90-percent endpoint multiplies the observed maximum coefficient norm by 3.2687556, including the conservative arrival factor and numerical guard. With the numerical inflation omitted, a fixed-nuisance geometric stress case attains the analytic 10-percent exclusion probability; a 262144-point phase quadrature gives 0.0999985. This illustrates sharpness of the underlying circle inequality, not validation of a new detector-noise model. Fixed-phase cancellation supplies the complementary counterexample: a nuisance equal to the negative signal leaves zero projection, so unrestricted fixed-phase absence cannot follow.

Retained coefficients also quantify the common-envelope cost. Applying the unchanged formula separately gives pointwise endpoints from $1.55457\times10^{-23}$ to $2.33931\times10^{-23}\,\mathrm{Hz}^{-1/2}$. The common unknown-context endpoint is 1.50479 times the smallest; taking the smaller value would change its scope. Such sensitivity loss from maximum representations is already recognized (Dergachev 2024). Practical value here is a transparent, rapidly reproducible conditional amplitude endpoint on a small heterogeneous panel. No superiority in sensitivity, false-alarm control, or computational cost over a calibrated Gaussian, injection-based, or universal-statistic search has been demonstrated.



| Inference construction | Randomness or coverage ensemble | Additional requirements | Present supported comparison |
|:---|:---|:---|:---|
| Gaussian quadrature likelihood | Detector-noise distribution | Appropriate covariance or PSD model and search treatment | Established prior art; no equal-task sensitivity comparison performed |
| Injection-calibrated or loudest-event inference | Declared noise, signal or population ensemble | Search-specific efficiency, background and exposure for the intended claim | Our fixed-cut crossing curves do not replace a calibrated global background |
| Universal upper-limit statistic | Background-sampling construction across distribution families | Conditions of the chosen universal construction | Established robust-limit prior art, not rerun or shown inferior |
| Fixed-packet phase endpoint here | Independent uniform source phase, conditional on fixed nuisance | One packet, fixed linear model and supports, phase-independent selection, certified response | Narrow received-strain confidence endpoint with raw-input replay |
| 4020-target variance envelope here | Same stipulated phase ensemble | Separate demeaned projection and saved variance/Gram bounds | Much weaker conservative envelope; no new matched-template scans |

These rows compare assumptions and permitted inference, not measured detector performance. The arithmetic audit took approximately 0.05 s and read retained coefficients; it is not a full strain runtime or evidence of speed superiority over any published search.

# Discussion

## Discrimination and transfer measure different properties

The combined results distinguish representation stability, discrimination, fixed-cut response and physical consistency. Historical representation checks retained selected synthetic features, while earlier probe and fusion failures remained unresolved for their original definitions. In particular, high cross-seed agreement coexisted with validation AUROC near 0.5. Removing a saturated percentile mapping subsequently recovered finite-panel ranking; it did not establish probability calibration or repair network-consistency limitations. These outcomes explain why a favorable internal diagnostic cannot stand in for an end-to-end measurement.

The reported 192-case benchmark was a positive discrimination result, with ranking AUROC 1.000000 and strong separation from single-detector contamination. The later strain pilot nevertheless gave 12/64 learned-ranking exceedances, versus 40/64 for energy. Eight learned exceedances already had positive matched noise baselines. The prescribed source-balanced recovery fractions, 0.125 and 0.625, preserve the unequal block contributions that ordinary pooled counts would obscure. This is a limitation of the tested representation, ranking, signals and operating cuts; it does not establish a general failure of learned anomaly detection.

Direct correlation responded favorably in development and on six new source blocks, accepting 96/96 originals against 43/96 for energy. The new-source screen still failed: its O4a noise counts were 3/12 versus 1/12, contrary to the prespecified epoch-wise requirement. Pooling epochs would change that criterion. The experiment therefore remains unsuccessful under its declared screen, without establishing a population false-alarm-rate increase. Nor do these transported cuts provide a matched-false-alarm comparison with energy or published search pipelines.

## A physical search interval does not certify physical timing

The structured-packet experiment exposes a more specific limitation. Above-cut response for all 48 originals accompanied acceptance of 38 over-delayed copies. For a narrowband packet, oscillatory cross-correlation supplies repeated local maxima; selecting one inside an allowed lag interval does not establish that the packet envelopes arrived within the light-travel bound. At a 256 Hz carrier, absolute-correlation maxima can recur approximately every 1.953125 ms. This mathematical observation motivates the diagnosis rather than substituting for its noisy-data measurements.

The broad-lag curves placed stronger raw and envelope maxima outside the physical cap for all 48 delayed packets in the pair driving the original score. Of the 48 original and 38 delayed above-cut records, 40 and 30, respectively, were new upward crossings relative to matched noise; eight in each group were already positive at baseline. An independent retained-curve recount verified 216 diagnostic records, 432 detector pairs and 864 curves, including exact maximizing sets. Every active raw pair peaked outside its cap in all 48 delayed records; the analogous envelope condition held for 47/48. The timing contradiction is therefore not confined to one unfavorably chosen pair.

Four physically projected originals also had raw maxima outside, and nine had envelope maxima outside. Consequently, a hard broad-peak-location veto would discard some original controls and is not a validated repair. The physical-cap/broad-maximum ratios occupied nonoverlapping ranges in this finite panel, but no ratio threshold was selected or transported to unopened sources. The curves demonstrate coexistence of an accepted in-cap local peak and a stronger broad peak outside; they do not separately identify the contributions of carrier phase, windowing, polarization, reference normalization and noise. Envelope peaks remain affected by taper structure and noise; the largest pair also does not implement a common sky and polarization fit (Sutton et al. 2010; Klimenko et al. 2016). This is a counterexample for the declared definition, not an empirical test of those coherent pipelines.

The timing panel's two-second phase-coded signal has a compact sine-fourth envelope and eight 0.25-s phase chips. It is distinct from the four-Gaussian packet used for the later amplitude endpoint. Their common 256-Hz carrier does not make their waveforms, statistics or inference interchangeable. Time reversal itself is likewise not a general violation of coherence for an unmodelled burst.

## Implications for the interpretation of structured transients

The timing counterexample identifies a concrete failure of inference rather than a new correlation principle. A high maximum selected inside a permitted light-travel interval establishes a property of the chosen statistic; it does not establish the arrival-time separation of the wave envelopes. The displaced-packet controls demonstrate this distinction in actual detector noise. Conversely, the four original signals with broad raw maxima outside the allowed interval show that rejecting every such maximum is not a cost-free correction. The result therefore constrains how this statistic can be used: its fixed-cut response must be reported alongside timing-specific negative controls and the measured losses of any proposed consistency rule.

The calibration audit supplies a second interpretive safeguard. Equal empirical exceedance counts on calibration data did not yield equal held-out noise response. An injection-count advantage at those cuts cannot be promoted to sensitivity superiority. This is directly relevant to computationally economical screening, where a simple score may be useful for allocating follow-up but does not itself supply a physical detection probability.

The separate random-phase amplitude construction answers a different question. It returns a conditional received-strain endpoint without fitting a detector-noise probability density, while explicitly paying for that choice through the independent uniform-phase assumption and conservative amplitude multiplier. Its practical contribution is an auditable route from a specified coded waveform to a numerical constraint on the inspected data. It is not a substitute for coherent source reconstruction or a calibrated discovery search. Together these measurements make the boundaries between morphology response, physical timing and amplitude inference quantitatively testable.

## Physical-source response is conditional on duration and parameters

The source experiments provide an explicit bridge from dynamics to measured response. The Newtonian rocket–exhaust specialization retains the mass budget and permanent memory, while the compact-pair proxy supplies persistent quadrupole radiation. Their physical amplitudes were not renormalized after choosing masses and a distance of 0.01 pc. The 10-ms rocket generated three new correlation-cut crossings in four reused contexts. Longer burns and the three compact-pair frequencies generated none; energy crossed in none of the 48 variants. A positive delayed short-rocket control also preserves the timing limitation.

Signal history was retained in the 64-second reference as well as the four-second target. Source-only calculations show strong loss of processed in-band power for longer memory rises and a persistent-source energy ratio near unity. These clarify the chosen normalization, but do not establish a single causal explanation for every noisy non-crossing or a general limit on continuous-wave detection. The rocket calculation specializes existing accelerated-source bookkeeping (Sellers et al. 2022); neither model establishes propulsion feasibility, artificial structure or a distance exclusion.

<div id="tab:physical_scope">

| Hypothesis                    | Relevant scale or tested construction                                        | Supported interpretation                                                                                                      |
|:------------------------------|:-----------------------------------------------------------------------------|:------------------------------------------------------------------------------------------------------------------------------|
| Classical Dyson configuration | Illustrative solar-mass, 1-AU orbital $f_{\rm GW}\simeq6.34\times10^{-8}$ Hz | Outside the transient comparison; optical/IR searches address a different observable (Suazo et al. 2024).                     |
| Asymmetric massive structure  | Compact-pair proxy at 64, 256 and 512 Hz                                     | Conditional response tested; equally compatible with a natural binary.                                                        |
| GW message or beacon          | Short phase-coded packets and packet trains with 256-Hz carrier              | Response and timing limitations measured; no message decoding or physical transmitter identified.                             |
| Accelerated massive vehicle   | Newtonian rocket–exhaust memory, $T=0.01,0.1,10$ s                           | Source-conditional injections, not an engine-feasibility test or the historical constant-mass waveform (Sellers et al. 2022). |
| Warp-fluid collapse           | Published 1-km example near 300 kHz                                          | Model-specific scaling assessed; the numerical waveform was not injected (Clough, Dietrich, and Khan 2024).                   |
| Galactic-centre Messenger     | Retrograde/nonspinning 0.63–1.07 mHz; listed prograde example 3.55 mHz       | Persistent millihertz observation, not tested by this short-target search (Abramowicz et al. 2020).                           |

Physical hypotheses and the scope of the present data products. Band or duration mismatch is not a data-derived exclusion.

</div>

<span id="tab:physical_scope" label="tab:physical_scope"></span>

Other technological hypotheses require matching observables. The illustrative stellar-scale Dyson orbit and Galactic-centre millihertz Messenger concern different bands and durations (Suazo et al. 2024; Abramowicz et al. 2020). The published warp-collapse frequency scaling does not replace an attributed numerical waveform (Clough, Dietrich, and Khan 2024). Coded packets likewise establish neither message decoding nor a physical transmitter; natural modulation remains a counterexample to assigning intelligence from modulation alone (Qiu, Wang, and He 2022).

## What could produce an anomalous response?

An unusual statistic and a physical source identification are separate results. The first asks whether a record is atypical under a declared comparison; the second asks which physical or instrumental process accounts for its strain. The completed observational test and its exploratory timeline extension selected no candidate under their stated conditional rules. Accordingly, the present evidence supports a map of possible explanations and discriminating measurements, rather than an attribution of an observed anomaly. The positive injection responses establish sensitivity to specified added signals; they do not establish that those signals occur in the observations.

Detector and environmental processes must remain explicit alternatives. Transient instrumental disturbances can resemble short GW signals, while nonstationary noise can change an energy or learned-feature baseline. Data-quality flags constrain specified conditions but do not certify the absence of every disturbance (B. P. Abbott et al. 2020). Narrow spectral artifacts can produce persistent or recurrent structure and degrade searches for narrowband signals (Goetz et al. 2026). The observation archive also contains continuous-wave hardware-injection annotations: the archived continuous-wave hardware-injection flag is false throughout the selected H1 and L1 supports. Those annotations were not vetoes in the fixed observation contract. They neither identify the cause of an individual score nor justify describing this archive as free of continuous-wave hardware injections. Candidate-specific line, injection and environmental associations have not been established.

The experiments identify additional ambiguities created by the observable itself. Of the 48 deliberately over-delayed structured packets, 38 exceeded the original correlation ratio cut. All 48 had their score-driving raw broad-lag maximum outside the physical cap. For a narrow carrier, absolute correlation can have approximately half-cycle-spaced maxima; the 256-Hz example gives a spacing of 1.953125 ms. A restricted-lag maximum can therefore appear physical while the packet displacement is not. Broad raw and envelope curves expose this ambiguity, but their maxima also fall outside the caps for some physically projected originals. They are diagnostics rather than a validated new veto. The duration-preserving source experiment supplies a different limitation: a persistent signal can affect both target and reference, leaving a ratio close to unity. Its finite noisy non-crossings cannot all be attributed to normalization alone. These observations motivate retaining absolute power, reference behavior, and raw and envelope timing as distinct measurements.

Natural GW sources remain alternatives whenever their frequencies and durations intersect the observed band. Compact-binary mergers and other short bursts require comparison with appropriate waveform and network hypotheses; the published O4a burst search illustrates such source-dependent sensitivity measurements (Abac et al. 2025). A persistent tone could instead motivate a continuous-wave search, for example for a rotating neutron star, with the relevant phase evolution and longer observation span (Riles 2023). Repeated or modulated waveforms are not specific to communication: gravitational lensing can produce repeated images or frequency-dependent amplitude and phase distortions, whose interpretation requires joint waveform and source-parameter consistency (R. Abbott et al. 2024). This study has not performed candidate-specific lensing or continuous-wave inference.

The technological-source hypotheses are conditional constructions. The phase-coded packets test a specified morphology, without decoding a message or modeling a transmitter. The Newtonian rocket–exhaust calculation links a stated acceleration and mass budget to detector strain; its strongest measured response occurred for the 10-ms rise on four reused contexts. It is distinct from a complete RAMAcraft search or an engineering-feasibility result (Sellers et al. 2022). The compact-pair proxy is equally compatible with natural orbital dynamics, so a response to it cannot identify control. Classical stellar-scale Dyson configurations and the proposed millihertz Galactic-centre Messenger probe different observables (Suazo et al. 2024; Abramowicz et al. 2020). The published 1-km warp-collapse example is near 300 kHz; its numerical waveform was not injected here, and moving a model into the present band would require a new, explicit source calculation (Clough, Dietrich, and Khan 2024).

| Possible explanation | Observable that could motivate it | What the present measurements establish | Additional discriminating evidence |
|:---------------------|:----------------------------------|:----------------------------------------|:-----------------------------------|
| Instrumental or environmental transient; changing noise state | Short excess, local feature outlier, or changing noise baseline | Unmodified noise can exceed the correlation ratio cut; the source-disjoint O4a noise guard failed. No particular environmental cause was identified. | Event-specific quality, detector-characterization and available auxiliary-channel evidence; stable response under declared conditioning. |
| Narrow line, comb, calibration feature or hardware injection | Persistent frequency concentration, harmonics, or repeated structure | Relevant hardware-injection annotations are retained. No frequency-specific attribution was made. | Match the actual GPS and frequency evolution to release-specific line/injection information; examine persistence and detector dependence. |
| Correlation alias or reference/processing effect | Short-lag carrier peak despite displaced envelopes; weak target/reference contrast for a persistent source | Delayed-packet acceptance and broad-lag ambiguity were measured; duration/reference effects were evaluated at the stated source parameters. | fixed raw/envelope timing and absolute/reference diagnostics; injection controls and independent-source evaluation of any proposed decision rule. |
| Natural transient GW source | Coherent chirp or burst within the sampled target | Generic and physical injections demonstrate finite-panel responses, not a detected celestial event. | Common-sky/polarization consistency, calibrated background, and comparison with relevant astrophysical waveform families. |
| Natural persistent source or propagation effect | Narrowband persistence, repeated waveform, or amplitude/phase modulation | The compact-pair proxy is nonunique in origin. No continuous-wave or lensing interpretation was tested on a selected observation. | Longer phase-coherent data where required; joint source-parameter, waveform and propagation-model tests. |
| Specified coded emitter or rapid massive acceleration | Declared packet coding, or duration- and parameter-dependent strain from mass motion | Packet and short-rocket responses are measured injection outcomes with retained timing and noise limitations. | Explicit source energetics/dynamics, independent observations, comparative natural/instrumental hypotheses, and validated network consistency. |
| Classical Dyson, Galactic-centre Messenger, or the published 1-km warp-collapse example | Respectively stellar-orbital, millihertz continuous, or high-frequency emission scales | The stated examples do not supply tested 64–768-Hz short-target source hypotheses. | An observation in the appropriate band/duration, or a separately validated in-band source model; no exclusion follows from the present mismatch. |

The table specifies a differential interpretation, not a probability ranking of source classes. A future selected record would first receive an instrumental and processing assessment and then a common-source GW analysis where simultaneous detector data exist. Technological interpretation would require additional comparative evidence for a stated source mechanism; visual regularity, correlation or unexplained residuals alone do not supply it. Failure to select a candidate likewise does not exclude these broad source classes: the efficiency, exposure, selection and background calibration would have to match each proposed physical exclusion.

## Observational and evidence limits

The 192 separated targets provide 768 s of target exposure, not a continuous survey or the sum of their longer processing contexts. Their registered within-source conditional test gave $p=1712/4097$ and did not reject its working null. The transformations add no independent search livetime, and their recurrence can impose a significance-resolution floor. Neither further conditional draws nor repeated injection variants complete a physical full-search background. Global false-alarm significance and population limits remain unsupported.

Evidence levels also differ. Early representation and controlled-benchmark values include preserved terminal summaries; later native result members and saved curves have explicit record-level provenance. The historical rocket waveform array and some final numerical records remain unavailable. Recounting saved scores does not constitute another raw-strain experiment. These limits are retained alongside the positive results, rather than replaced by retrospective success declarations.

## Interpretation of the completed CPU survey

The completed randomized H1 survey expands the number of measured source-grouped records while retaining the same physical questions. It provides finite feature distributions, absolute and reference behavior, source-held-out phenomenological response and bounded coeval timing dispositions. Its computational gain comes from grouped source acquisition and cheap fixed summaries, not from counting resampling draws as new observations. The 4096 completed audits establish execution completeness for this survey; they do not establish 4096 independent network trials, a population false-alarm probability or an absence of all anomalies.

The new contrast between robust feature ranking and energy at the context endpoint was 0.1875, and the source-group contrast was 0.1250 at their finite nominal group cuts. These paired measurements must be read with their source-group noise responses and actual quality denominators. No candidate was declared through a calibrated detection threshold: the eight-rank rule supplies review targets by construction. Coeval pair diagnostics can expose timing ambiguity, but without a validated common-source decision and matched search background they do not convert an outlier into a celestial or technological detection. The measured peaks therefore support a bounded feature-and-response assessment and a concrete list of unresolved interpretations, rather than a physical population exclusion.

# Conclusions

The finite study measures a divergence between strong constructed-signal discrimination, response in actual strain, noise transfer and physical-delay specificity. Its positive correlation responses coexist with a failed new-source noise criterion and substantial acceptance of over-delayed packets. The broad-lag measurements explain one failure mode while revealing costs of a simple peak-location veto. Duration-preserving source injections further show a parameter-explicit short-rocket response and absent new crossings for the longer and persistent configurations. These results support a bounded sensitivity and specificity assessment. They do not identify a technological source or provide calibrated discovery significance. Stronger inference would require validated network consistency, an appropriate full-search background and source-conditional efficiency under the intended observational selection. The later random-sample CPU survey completed all 4096 selected-record audits and retained 4020 valid feature vectors, with explicit source grouping, quality exclusions, paired injection response and candidate timing dispositions. That completed finite survey adds measured real-data behavior without altering the historical full-search background count or promoting review ranks to detections.

The subsequent fixed-family calculation adds a quantitative received-strain endpoint: $h_{\rm rss,H1}\le2.3393\times10^{-23}\,\mathrm{Hz}^{-1/2}$ at 90% phase-ensemble coverage for one prescribed 256-Hz coded packet in the twelve declared timing supports. Its coverage assumes a uniform independent carrier phase and a fixed linear projection; it permits arbitrary fixed additive noise. It is a conditional waveform-amplitude constraint, not a calibrated detection, an all-phase absence result, or an exclusion of technological populations.

Together, the results establish three requirements for interpreting this class of structured-transient statistic: report the response to both physically projected and deliberately displaced signals; accompany injection responses by the noise behavior at the same analysis unit; and state the probability ensemble underlying an amplitude constraint. The measured veto cost, calibration-to-test mismatch and conditional strain endpoint quantify why those requirements matter in the tested implementation. They provide concrete validation and reporting constraints for computationally economical screening, while leaving coherent source reconstruction and calibrated discovery inference as distinct tasks. All earlier numerical outcomes and figure inputs are retained.

# Data and analysis availability

The scientific source code and versioned reproducibility materials are available at <https://github.com/MeteMurat/gw-anomalous-controlled-dynamics>. Versioned releases provide the current paper, figure-generation inputs, numerical results and the three original fitted neural models; manuscript-only corrections are released separately from the complete reproducibility archive. Technical provenance and integrity records are retained with the code rather than reproduced in the article.

Public detector strain is available through the O4a and O4b releases of the Gravitational Wave Open Science Center (Gravitational Wave Open Science Center 2025, 2026). The accompanying code and data materials provide the analysis definitions, source selections, numerical results, figure inputs, three fitted neural models and their training schedule. Exact file identities and verification records belong to those materials rather than to the scientific interpretation.

Reproduction is separated into retained-result verification, figure and table regeneration, source-model forward calculations, and evaluation from raw strain. The new fixed-packet experiment includes all twelve 68-s strain arrays, its projection and response coefficients, injection results and geometric-coverage checks. An independent Windows execution with Python 3.11.9 and NumPy 2.3.2 repeated 109440 linear superpositions and all six validation stages. The upper endpoint was $2.3393053703000202\times10^{-23}\,\mathrm{Hz}^{-1/2}$, compared with $2.3393053702995976\times10^{-23}\,\mathrm{Hz}^{-1/2}$ on the original host; their relative difference was below $1.81\times10^{-13}$, within the declared $10^{-8}$ tolerance. The main calculation took 62.969 s and the full repetition 86.406 s. The retained-variance construction also reproduced its 4020-row numerical table exactly; it did not repeat matched-template projections on 4020 strain arrays.

The three fitted neural models and complete layer, preprocessing, loss and optimization specifications are available. Exact historical training replay additionally requires the original preprocessed training arrays, production-selection record and numerical-library build information, which were not recovered. Evaluation from raw strain through the original neural embeddings has not been independently repeated. The subsequent correlation, energy, source-model, timing and randomized feature calculations are non-neural analyses with separately documented inputs. These distinctions prevent saved-table verification from being represented as a new strain or model evaluation.

<div id="refs" class="references csl-bib-body hanging-indent">

<div id="ref-LVKO4aBurst2025" class="csl-entry">

Abac, A. G., I. Abouelfettouh, F. Acernese, et al. 2025. “<span class="nocase">All-sky search for short gravitational-wave bursts in the first part of the fourth LIGO-Virgo-KAGRA observing run</span>.” *Physical Review D* 112 (10): 102005. <https://doi.org/10.1103/wjdz-jdby>.

</div>

<div id="ref-Abbott2010GRBAmplitude" class="csl-entry">

Abbott, B. P., R. Abbott, F. Acernese, et al. 2010. “Search for Gravitational-Wave Bursts Associated with Gamma-Ray Bursts Using Data from LIGO Science Run 5 and Virgo Science Run 1.” *The Astrophysical Journal* 715 (2): 1438–1452. <https://doi.org/10.1088/0004-637X/715/2/1438>.

</div>

<div id="ref-LVKO3Burst2021" class="csl-entry">

Abbott, R., T. D. Abbott, F. Acernese, et al. 2021a. “<span class="nocase">All-sky search for short gravitational-wave bursts in the third Advanced LIGO and Advanced Virgo run</span>.” *Physical Review D* 104 (12): 122004. <https://doi.org/10.1103/physrevd.104.122004>.

</div>

<div id="ref-GWOSC2021" class="csl-entry">

Abbott, Rich, Thomas D. Abbott, Sheelu Abraham, et al. 2021b. “<span class="nocase">Open data from the first and second observing runs of Advanced LIGO and Advanced Virgo</span>.” *SoftwareX* 13: 100658. <https://doi.org/10.1016/j.softx.2021.100658>.

</div>

<div id="ref-Abramowicz2020" class="csl-entry">

Abramowicz, Marek, Michal Bejger, Eric Gourgoulhon, and Odele Straub. 2020. “<span class="nocase">A Galactic centre gravitational-wave Messenger</span>.” *Scientific Reports* 10 (1): 7054. <https://doi.org/10.1038/s41598-020-63206-1>.

</div>

<div id="ref-LVKNoiseGuide2020" class="csl-entry">

B. P. Abbott et al. (LIGO Scientific Collaboration and Virgo Collaboration). 2020. “A guide to LIGO–Virgo detector noise and extraction of transient gravitational-wave signals.” Classical and Quantum Gravity 37: 055002. <https://doi.org/10.1088/1361-6382/ab685e>.

</div>

<div id="ref-Bardes2022VICReg" class="csl-entry">

Bardes, Adrien, Jean Ponce, and Yann LeCun. 2022. “VICReg: Variance-Invariance-Covariance Regularization for Self-Supervised Learning.” International Conference on Learning Representations. <https://arxiv.org/abs/2105.04906>.

</div>

<div id="ref-Biswas2009" class="csl-entry">

Biswas, Rahul, Patrick R. Brady, Jolien D. E. Creighton, and Stephen Fairhurst. 2009. “The loudest event statistic: general formulation, properties and applications.” *Classical and Quantum Gravity* 26: 175009. <https://doi.org/10.1088/0264-9381/26/17/175009>.

</div>

<div id="ref-Cadonati2004" class="csl-entry">

Cadonati, L. 2004. “Coherent waveform consistency test for LIGO burst candidates.” *Classical and Quantum Gravity* 21 (20): S1695. <https://doi.org/10.1088/0264-9381/21/20/012>.

</div>

<div id="ref-Clough2024" class="csl-entry">

Clough, Katy, Tim Dietrich, and Sebastian Khan. 2024. “<span class="nocase">What no one has seen before: gravitational waveforms from warp drive collapse</span>.” *The Open Journal of Astrophysics* 7. <https://doi.org/10.33232/001c.121868>.

</div>

<div id="ref-Dergachev2013" class="csl-entry">

Dergachev, Vladimir. 2013. “Novel universal statistic for computing upper limits in an ill-behaved background.” *Physical Review D* 87: 062001. <https://doi.org/10.1103/PhysRevD.87.062001>.

</div>

<div id="ref-Dergachev2024" class="csl-entry">

Dergachev, Vladimir. 2024. “Efficient representations of upper limits and confidence intervals for experimental data.” *Physical Review D* 110: 085001. <https://doi.org/10.1103/PhysRevD.110.085001>.

</div>

<div id="ref-Goetz2026Lines" class="csl-entry">

Goetz, E., A. Neunzert, A. M. Knee, et al. 2026. “Narrow spectral artifact investigation and mitigation in LIGO data from the fourth LIGO-Virgo-KAGRA observing run.” arXiv:2606.05959. <https://arxiv.org/abs/2606.05959>.

</div>

<div id="ref-GWOSCO4a2025" class="csl-entry">

Gravitational Wave Open Science Center. 2025. “The O4a Data Release.” <https://doi.org/10.7935/kt51-6n86>.

</div>

<div id="ref-GWOSCO4b2026" class="csl-entry">

Gravitational Wave Open Science Center. 2026. “The O4b Data Release.” <https://doi.org/10.7935/8emv-ag54>.

</div>

<div id="ref-GWOSCO4Technical" class="csl-entry">

Gravitational Wave Open Science Center. n.d. “O4 Data Set Technical Details.” Accessed 1 November 2026. <https://gwosc.org/O4/o4_details/>.

</div>

<div id="ref-MADGRAV2026" class="csl-entry">

Inguglia, Gianluca, Huw Haigh, Ulyana Dupletsa, and Alessandro Longo. 2026. “<span class="nocase">MADGRAV: a multilevel anomaly-detection pipeline for gravitational-wave searches applied to LIGO data</span>.” arXiv:2609.39583. <https://arxiv.org/html/2609.39583v2>.

</div>

<div id="ref-Jaranowski1998" class="csl-entry">

Jaranowski, Piotr, Andrzej Królak, and Bernard F. Schutz. 1998. “Data analysis of gravitational-wave signals from spinning neutron stars. I. The signal and its detection.” *Physical Review D* 58: 063001. <https://doi.org/10.1103/PhysRevD.58.063001>.

</div>

<div id="ref-Riles2023CW" class="csl-entry">

Keith Riles. 2023. “Searches for continuous-wave gravitational radiation.” Living Reviews in Relativity 26: 3. <https://doi.org/10.1007/s41114-023-00044-3>.

</div>

<div id="ref-Klimenko2016" class="csl-entry">

Klimenko, S., G. Vedovato, M. Drago, et al. 2016. “<span class="nocase">Method for detection and reconstruction of gravitational wave transients with networks of advanced detectors</span>.” *Physical Review D* 93 (4): 042004. <https://doi.org/10.1103/physrevd.93.042004>.

</div>

<div id="ref-Loshchilov2019AdamW" class="csl-entry">

Loshchilov, Ilya, and Frank Hutter. 2019. “Decoupled Weight Decay Regularization.” International Conference on Learning Representations. <https://arxiv.org/abs/1711.05101>.

</div>

<div id="ref-Paszke2019PyTorch" class="csl-entry">

Paszke, Adam, Sam Gross, Francisco Massa, et al. 2019. “PyTorch: An Imperative Style, High-Performance Deep Learning Library.” Advances in Neural Information Processing Systems 32. <https://arxiv.org/abs/1912.01703>.

</div>

<div id="ref-Qiu2022" class="csl-entry">

Qiu, Yi, Ke Wang, and Jian-hua He. 2022. “<span class="nocase">Amplitude modulation in binary gravitational lensing of gravitational waves</span>.” arXiv:2205.01682. <https://arxiv.org/abs/2205.01682>.

</div>

<div id="ref-LVKLensing2024" class="csl-entry">

R. Abbott et al. (LIGO Scientific Collaboration, Virgo Collaboration and KAGRA Collaboration). 2024. “Search for gravitational-lensing signatures in the full third observing run of the LIGO–Virgo network.” The Astrophysical Journal 970: 191. <https://doi.org/10.3847/1538-4357/ad3e83>.

</div>

<div id="ref-GWAK2024" class="csl-entry">

Raikman, Ryan, Eric A Moreno, Ekaterina Govorkova, et al. 2024. “<span class="nocase">GWAK: gravitational-wave anomalous knowledge with recurrent autoencoders</span>.” *Machine Learning: Science and Technology* 5 (2): 025020. <https://doi.org/10.1088/2632-2153/ad3a31>.

</div>

<div id="ref-CoAD2026" class="csl-entry">

Ratner, Daniel. 2026. “<span class="nocase">Template-free search for gravitational wave events using coincident anomaly detection</span>.” *Physical Review D* 113 (12): 122005. <https://doi.org/10.1103/zjbd-smrd>.

</div>

<div id="ref-Sellers2022" class="csl-entry">

Sellers, Luke, Alexey Bobrick, Gianni Martire, Michael Andrews, and Manfred Paulini. 2022. “<span class="nocase">Searching for Intelligent Life in Gravitational Wave Signals Part I: Present Capabilities and Future Horizons</span>.” arXiv:2212.02065. <https://arxiv.org/abs/2212.02065>.

</div>

<div id="ref-Suazo2024" class="csl-entry">

Suazo, Matías, Erik Zackrisson, Priyatam K. Mahto, Fabian Lundell, Carl Nettelblad, Andreas J. Korn, Jason T. Wright, and Suman Majumdar. 2024. “Project Hephaistos – II. Dyson sphere candidates from Gaia DR3, 2MASS, and WISE.” *Monthly Notices of the Royal Astronomical Society* 531 (1): 695–707. <https://doi.org/10.1093/mnras/stae1186>.

</div>

<div id="ref-Sutton2010" class="csl-entry">

Sutton, Patrick J, Gareth Jones, Shourov Chatterji, et al. 2010. “<span class="nocase">X-Pipeline: an analysis package for autonomous gravitational-wave burst searches</span>.” *New Journal of Physics* 12 (5): 053034. <https://doi.org/10.1088/1367-2630/12/5/053034>.

</div>

<div id="ref-SuttonEnergy2013" class="csl-entry">

Sutton, Patrick J. 2013. “<span class="nocase">A Rule of Thumb for the Detectability of Gravitational-Wave Bursts</span>.” arXiv:1304.0210. <https://arxiv.org/abs/1304.0210>.

</div>

</div>


---

# Scientific supplement

# Statistical interpretation and evidence limits

This supplement preserves detailed positive and negative results, source derivations, model specifications and numerical-validation limits. Operational identifiers and exact file identities are confined to the reproducibility materials. Repeated calculations on the same strain do not create independent observations.

The paired net threshold response used in the main article is repeated to keep this supplement self-contained: $$J_{m,b}=\frac{1}{N_b}\sum_{(i,k)\in b}
\left[\mathbf{1}\{s^{\rm inj}_{m,ik}>c_{m,e(i)}\}
-\mathbf{1}\{s^0_{m,i}>c_{m,e(i)}\}\right].
\label{eq:paired_lift}$$ It is a descriptive paired threshold statistic, not a false-alarm probability.

# Representation, fusion, and scoring validation

The development sequence separates numerical reproducibility, response to constructed controls, transport across observing configurations, and evidence for a physical source. A successful criterion in one category was not taken as a substitute for the others. Earlier failed criteria were retained when subsequent methodological amendments were introduced. The evidence available for the historical measurements is recorded separately: several early values are preserved numerical summaries rather than newly reprocessed strain outputs. They are not presented as fresh raw-data reanalyses.

## Self-supervised representation and retained negative controls

The recovered bounded neural-training record reports three completed seeds ($20260919$, $20260920$, and $20260921$), using 640 training and 320 development windows, with at most six epochs. Training used the local cache; the fixed external validation panel was not touched by this training run. At the subsequent representation checks, the aggregate non-collapse fraction was $0.9921875$, the median pairwise linear CKA was $0.97555235$, and the augmentation-pair median cosine was $0.99253152$. Synthetic chirp–reverse and modulated–demodulated tasks achieved median AUROCs of $1.0$ and $0.99913194$, respectively. These are synthetic-task measurements, not observational discovery rates or physical-source detection efficiencies.

The original six-feature probe nevertheless failed: only three features exceeded the fixed $|\rho|=0.5$ requirement, compared with four required. The median repetition correlation was $0.42455493$; modulation and time–frequency excess were also below the probe threshold. An independent six-feature panel passed four of six features, with repetition $0.72264438$, but the subsequent ten-panel feature-stability assessment failed its registered overall requirements. Six of its ten panels met the four-feature screen; that partial response did not meet the overall criterion. Six of its ten panels met the four-feature screen; that partial response did not satisfy the overall criterion. These failures remain part of the result, rather than being replaced by the later confirmation.

The precision-calibrated prospective five-panel feature assessment was fixed before its new panel outcomes and used 512 ridge-training and 512 held-out synthetic test examples per panel. All five panels passed the requirement of at least four of six features together with the repetition requirement. The repetition correlation had panel median $0.74852925$ and range $[0.70902508,0.78891149]$. Coherence, two-detector residual, modulation, and instrumental features also passed on all five panels; the time–frequency excess feature passed on none. Thus the confirmatory outcome is feature-specific. The final neural-representation assessment is retained as a historical report; its separate numerical amendment was not recovered or independently repeated.

## Network fusion and topology dependence

The public-source catalogue contained 36,664 unique files after 4,438 additions to the fixed manifest. The aligned fusion panel comprised 128 training, 64 development, and 64 validation network cases, with equal O4a/O4b allocation within each partition. The original fusion result illustrates why numerical agreement alone is insufficient: median cross-seed CKA was $0.99631325$, while median validation AUROC was $0.501953125$, below the $0.8$ criterion. The controlled-positive pooled variant also failed its pooled criterion (development $0.7978515625$, validation $0.763916015625$ in the recovered summary). Stronger topology-stratified responses therefore did not justify claiming success of the original pooled decision.

The original fusion probe development AUROC was $0.49609375$, compared with $0.501953125$ on validation; a small partition difference did not indicate useful discrimination.

The subsequent fixed topology-conditioned contract retained the shared training-only PCA and ridge fit and conditioned evaluation on detector topology. It explicitly preserved the original, pooled, and topology-specific-refit failures and forbade a new PCA fit, ridge hyperparameter changes, and threshold retuning. The contract is recovered evidence of the method definition; missing terminal per-topology values are not reconstructed from the contract’s pass thresholds.

## Novelty ranking and network-consistency limitations

The first learned-ranking percentile calibration saturated on the finite training reference: the median validation AUROC was $0.578125$ for O4a and $0.5$ for O4b, whereas the underlying raw-distance controlled-panel AUROCs were $1.0$. The localization therefore supported removal of the empirical percentile mapping, rather than changing the representation or searching over nearest-neighbour settings. The retained score is the topology-conditional robust-scaled five-nearest- neighbour raw distance. In the historical raw-ranking report, median development and validation AUROCs were $1.0$ for each topology; median cross-seed validation rank correlations were $0.92628205$ and $0.91547619$. The optional affine transformation using the training leave-one-out median and interquartile range preserves ranks and is not a probability calibration. These controlled-panel results do not replace the later physical-strain pilot, which exhibited substantially weaker recovery.

The learned pair-consistency sequence exposed a distinct limitation. The initial fusion-based veto did not consistently distinguish coherent injections from single-detector contamination. A multi-detector-support variant also failed its joint criteria. The pairwise-consistency localization separated several single-detector controls well, but its coherent-versus-background validation AUROC was only $0.6201171875$ for O4a, versus $0.83984375$ for O4b. The recorded conclusion was that pairwise network-consistency discrimination was insufficient. Neither later injection recovery nor additional background rearrangements erase that limitation. The distinction between response to a constructed waveform and a common physical network source remains relevant to the subsequent correlation ratio/structured-packet study results.

# Calibration-bank construction and conditional diagnostics

The completed calibration bank contains 1,066 detector records from 12 physical source intervals, 27 detector–source streams, and 54 source files. The counts are 252 O4a/H1, 344 O4a/L1, 192 O4b/H1, 176 O4b/L1, and 102 O4b/V1. The fixed embedding array has shape $[1066,3,2,128]$ and retains the original 32-bit floating-point tensor values. The two rate branches are 4,096 and 16,384 Hz. Full-68-second quality checks produced 2,132 rate records and 12,792 required flag decisions, with no raw non-finite rejections in this calibration collection. The 1,066 detector records are not 1,066 independent network searches.

A registered norm-vector consequence of a conditional within-stream permutation model was checked with 4,096 draws. There were 3,080 exceedances of the observed maximum correlation statistic, giving the stored diagnostic $p=3081/4097=0.75201367$. This non-rejection concerns a narrow consequence of the stipulated invariance model. It does not prove stationarity, full embedding or scorer invariance, foreground/calibration transport, or the final physical noise null.

The next descriptive calculation evaluated 18,304 artificial tuples across 64 maps and 11 source blocks with the necessary detector coverage. It produced finite numerical scores and source-local mapping checks, but no physical 192-event observation or matched global null. Earlier dependent reference-recombination processing likewise completed 64 dependent development recombinations with exact identity-score parity and no new neural-encoder inference. source-disjoint reference completed one source-disjoint development reference unit containing 192 events and 480 embedding slots; raw-finiteness screening retained 96 events per topology after 55 O4a and 36 O4b rejections. These are data and computational outcomes, not additional independent full-search null trials. The original campaign remains $3/4096$; global false-alarm calibration is not inferred from the number of conditional maps.

The exact CPU accelerator has an actual Windows replay archive documenting bitwise-equivalent replay checks. Such equivalence supports cached computation and reuse of completed records. It is separate from the statistical validity of the reconstructed background.

# Earlier physical-reference calculations

The recovered 18 September terminal record establishes that the RAMAcraft analytic Figure-1 benchmark (Sellers et al. 2022) had already been reconstructed before the current physical-model extension. The source implementation uses the published order-of-magnitude detector convention $h(t)=2GMv(t)^2/(Dc^4)$, with $M=10^{-3}M_\odot$, $D=10^{21}$ m, $v_0=0.01c$, $v_f=0.5c$, and an acceleration interval of 100 s sampled at 4,096 Hz over $[-100,200)$ s. It reports a fitted 20–200 Hz spectral slope of $-0.99826357$, Parseval relative error $1.553\times10^{-16}$, and $D/(5\Delta vT)=1.361486\times10^{10}$. The published model’s approximations are retained; the high endpoint speed in this reference benchmark is not evidence of a newly validated relativistic propulsion model. The original numerical waveform array was unavailable for this review. The implementation and reported numerical output, rather than that array, support the historical benchmark values.

That same earlier stage reports six exact paired 16-kHz inputs and H1/L1 high-frequency products spanning 1,700–5,000 Hz, with overlap sanity checks. This earlier high-frequency characterization is distinct from the 64–768 Hz, four-second-target correlation ratio/energy ratio transient branch used subsequently. Detectability was explicitly not evaluated in the earlier RAMAcraft benchmark. The later source-model study extension completes a physical-model–detector–measured-response connection for its specified Newtonian rocket–exhaust and compact-pair models. It does not constitute a noisy-data replay of the historical constant-mass RAMAcraft Figure 1 waveform.

The Galactic-centre Messenger reproduction reached a partial, source-limited terminal outcome in the recovered transcript: supported-spin Eq. (3) values matched under the astrophysical $10^{-3}M_\odot$ convention, whereas the negative-spin legacy source data and an exact joint Eq. (5) SNR convention remained unresolved. The best predefined SNR diagnostic yielded $285.1695$ and $3583.9081$ against quoted values $280$ and $3600$; these were not fitted values or a complete reproduction claim. The separate relativistic runtime has a historically reported closure, but its original final numerical closure artifact was not recovered here. None of these source-reference calculations constitutes a detection or exclusion of a Galactic-centre beacon in the current transient data.

# Detailed historical controlled-benchmark record

The historical controlled benchmark is preserved in transcribed numerical summaries. This evidence level is distinct from the later complete-return record audits: the historical per-case score bank was not independently reprocessed for this manuscript integration. The bank contained 192 cases, comprising 24 background cases, 48 coherent network injections, and 24 synthetic single-detector contamination cases in each of O4a and O4b. The same cases were scored with seeds 20260919, 20260920, and 20260921; this does not create 576 independent cases.

The reported learned-ranking AUROC for coherent injections versus background was $1.000000$ for every seed in both epochs. For the learned pair-consistency comparison against single-detector contamination, the seed-wise AUROCs were $0.974826$, $0.984375$, and $0.964410$ in O4a, and $0.942708$, $0.970486$, and $0.955729$ in O4b. The corresponding medians were $0.974826$ and $0.955729$. Both reported medians exceeded the declared $0.80$ criterion. We retain the reported six-decimal precision and do not infer population confidence intervals from these rounded summaries.

The evaluation chronology is asymmetric. learned-ranking scores were fixed before the controlled-benchmark label release. learned pair-consistency was first evaluated on the controlled-benchmark bank after label release, following a historical numerical-convention binding check whose compared summary differences were zero. This is not a claim that both learned-ranking and learned pair-consistency score banks were fixed before unblinding. The complete family/amplitude summary is preserved in the supplementary section entitled “Controlled-benchmark family and nominal-amplitude summaries”. The nominal amplitude levels in that benchmark are not source strain, physical SNR, or distance, and its score medians are not detection efficiencies.

These positive discrimination results are retained alongside the subsequent negative strain-level pilot. The experiments differ in cohorts, signal families, amplitude definitions, and endpoints; a favorable finite-bank AUROC does not imply adequate sensitivity at the later transported cuts.

# A source-to-detector calculation with explicit approximation limits

The additional source study is conditional on two specified dynamical models. It does not reinterpret a generic chirp as a physical rocket or warp-collapse waveform. It also does not replace the closed observational, six-source-block validation or structured-packet study results. Source parameters determine strain amplitude directly; no arbitrary $h_{\rm rss}$ renormalization is applied after a mass and distance have been chosen.

## Newtonian rocket with a ballistic exhaust mass distribution

The published RAMAcraft calculation gives a constant-mass, no-exhaust approximation as well as an exhaust contribution and its momentum bookkeeping (Sellers et al. 2022). An earlier project run reproduced the published Figure 1 approximation; the source-to-cached-detector study considered here is a different step. The following deliberately nonrelativistic specialization fixes a constant relative exhaust speed and an explicit mass budget. Its contribution here is the specified source-to-detector response experiment; exhaust bookkeeping itself is already present in Ref. (Sellers et al. 2022).

Let a rocket move along a fixed unit vector $\boldsymbol{s}$ with speed $v(t)$. Its backward exhaust speed relative to the rocket is the positive constant $u$. A mass element released at $t'$ subsequently travels ballistically with inertial velocity $w(t')=v(t')-u$. For a prescribed monotone acceleration $a=\dot v\geq0$, Newtonian mass and momentum conservation give $$q(t)=-\dot M(t)=\frac{M(t)a(t)}{u},\qquad
 M(t)=M_0\exp\!\left[-\frac{v(t)-v_0}{u}\right].
 \label{eq:rocket-mass}$$ Writing the exhaust mass budget explicitly, $$\begin{aligned}
 M(t)+\int_{t_0}^{t}q(t')\,dt'&=M_0,\\
 M(t)v(t)+\int_{t_0}^{t}q(t')w(t')\,dt'&=M_0v_0.
 \label{eq:rocket-momentum}
\end{aligned}$$ The source second moment along the motion is $$I_{ss}=M z^2+\int_{t_0}^{t}q(t')
 \{z(t')+w(t')[t-t']\}^{2}\,dt'.$$ The terms proportional to the instantaneous ejection position cancel when $M a=q u$ is used. Consequently $$\begin{aligned}
 \ddot I_{ss}&=2\mathcal S(t),\\
 \mathcal S(t)&=M(t)v(t)^2+
       \int_{t_0}^{t}q(t')w(t')^2\,dt'\\
   &=M_0v_0^2+u^2[M_0-M(t)].
 \label{eq:rocket-second-moment}
\end{aligned}$$ This identity independently checks the exhaust implementation. The increase in kinetic energy is $\Delta K=\tfrac12 u^2(M_0-M)$; a positive energy reservoir must supply it. The ledger conserves Newtonian mass and momentum. It is not a full propulsion, equation-of-state or relativistic energy-conservation model. Internal-energy mass corrections and stress contributions beyond the leading slow-motion approximation are not resolved.

For smooth start and stop of the acceleration, define $x=(t-t_0)/T$ and $$g(x)=\begin{cases}
 0,&x\leq0,\\
 10x^3-15x^4+6x^5,&0<x<1,\\
 1,&x\geq1,
 \end{cases}\qquad v(t)=v_0+\Delta v\,g(x).$$ Here $g'(0)=g'(1)=g''(0)=g''(1)=0$. A useful independent trajectory is $z=v_0(t-t_0)+\Delta v T G(x)$, with $G=0$ for $x\leq0$, $G=\tfrac52x^4-3x^5+x^6$ inside the burn, and $G=x-\tfrac12$ afterwards.

At leading quadrupole order, with source distance $D$, observer inclination $\iota$ to $\boldsymbol{s}$ and polarization angle $\psi$, subtracting the constant pre-burn strain gives $$\begin{aligned}
 \Delta h_+(t)&=\frac{2G u^2[M_0-M(t)]}{c^4D}
               \sin^2\iota\cos2\psi,\\
 \Delta h_\times(t)&=\frac{2G u^2[M_0-M(t)]}{c^4D}
               \sin^2\iota\sin2\psi.
 \label{eq:rocket-polarizations}
\end{aligned}$$ The factor of two follows from contracting the TT tensor with the polarization tensors; the unprojected $\overline h_{ss}$ is twice the maximum $h_+$. The post-burn offset is physical ordinary-memory content of this approximation. It must not be turned off at the four-second target boundary. Waveforms are evaluated over the entire available 68-second context, including any burn portion in the 64-second reference. Finite record cropping and the existing analysis window are observation operations, not a new source cutoff.

The chosen low-speed regime must keep both rocket and inertial exhaust speeds small compared with $c$, keep the source-detector distance much larger than the motion scale, and state the leading far-zone and retardation approximations. In particular, a low-frequency memory model passed through a 64–768 Hz transient statistic is not equivalent to the broadband sensitivity estimate in the original RAMAcraft article.

The energy supplied to the rocket–exhaust kinetic ledger is distinct from the energy carried by GWs. With the trace-free quadrupole $Q_{ij}=I_{ij}-\delta_{ij}I_{kk}/3$, the axial model gives $\sum_{ij}(\dddot Q_{ij})^2=8\dot{\mathcal S}^{\,2}/3$ and hence $$E_{\rm GW}=\frac{8G}{15c^5}\int_{\rm burn}
       [uM(t)a(t)]^2\,dt.$$ The same coefficient follows by integrating the two-polarization flux over solid angle, using $\int\sin^4\iota\,d\Omega=32\pi/15$ and the flux convention of Ref. (Sutton 2013). Only that general polarization-flux convention is used here; finite-burst $h_{\rm rss}$ and narrowband range relations are not applied to the waveform with permanent memory. For the declared Jupiter-mass example with $u=0.01c$ and $\Delta v=0.001c$, the added kinetic energy is $8.11715\times10^{38}$ J. The leading modeled GW energies for burn durations $0.01,0.1,10$ s are respectively $5.53641\times10^{27},5.53641\times10^{26},5.53641\times10^{24}$ J. These are full-burn, direction-integrated source predictions, not an isotropic-equivalent detected energy or a 64–768 Hz FFT energy fraction.

## A compact two-body mass-motion proxy

For an explicit mass-motion comparison, consider equal compact point masses $m$ in a Newtonian circular orbit at radii $a$ from the center of mass. This closed source has no artificial-origin label: the same quadrupole can belong to a natural system. Its orbital angular frequency and GW frequency satisfy $$\Omega^2=\frac{Gm}{4a^3},\qquad f_{\rm GW}=\frac{\Omega}{\pi}.
 \label{eq:binary-kepler}$$ Defining $h_0=8Gma^2\Omega^2/(c^4D)$ and orbital phase $\phi$, $$\begin{aligned}
 h_+&=-\frac{h_0}{2}(1+\cos^2\iota)\cos2\phi,\\
 h_\times&=-h_0\cos\iota\sin2\phi.
 \label{eq:binary-polarizations}
\end{aligned}$$ A subsequent fixed rotation by $2\psi$ changes polarization basis only. The factors can be checked directly from $I_{ij}=2m r_i r_j$ with $\boldsymbol r=a(\cos\phi,\sin\phi,0)$ and the TT projection. These are leading quadrupole, approximately fixed-orbit waveforms, not exact general-relativistic solutions or a demonstration that an ordinary-material apparatus could be built at these separations.

The leading radiation-reaction estimate for equal masses is $$t_c=\frac{5c^5(2a)^4}{512G^3m^3},\qquad
 \frac{\dot f}{f}=\frac{3}{8t_c}.$$ For $m=10^{24}$ kg and $f_{\rm GW}=64,256,512$ Hz, the orbital radii are $744.553,295.476,186.138$ m and the speeds are approximately $0.000499,0.000793,0.000999\,c$, respectively. The largest neglected 68-second chirp phase, estimated as $\pi\dot f(68\,\mathrm{s})^2$, is approximately $0.00183$ rad at 512 Hz. This bound describes the declared fixed-orbit approximation; it is not a numerical integration of inspiral.

The signal is present throughout the reference and target. Its response to a target/reference statistic can therefore differ sharply from a transient with the same target amplitude. Artificially suppressing the first 64 seconds would remove precisely the source-duration effect the study is meant to test.

## Detector mapping and scope of the measured response

For either model the detector signal is $$h_I(t)=F_I^+h_+(t-\tau_I)+F_I^\times h_\times(t-\tau_I).$$ The same source polarizations, geometry and delays must be used in every detector. Source mass and distance remain physical parameters; normalization to an arbitrary injected $h_{\rm rss}$ would erase this link. Conditional response on the already-open noise contexts is an exploratory sensitivity measurement. It does not establish a population false-alarm probability, a distance exclusion, an event-rate bound or an engineered source.

## Declared physical sources and their finite-window response

The new forward models specify physical masses, motions and a distance of $0.01\,\mathrm{pc}$; they are not rescaled to prescribed $h_{\rm rss}$ or network signal-to-noise ratio. Both use inclination $\pi/3$ and source-polarization angle $0.2$ rad. The rocket initially has mass $1.89813\times10^{27}$ kg, speed $0.001c$, velocity increment $0.001c$, and backward relative exhaust speed $0.01c$. Its quintic velocity transition has duration $0.01$, $0.1$, or $10$ s and is centred at context time $66$ s. This exhaust-complete Newtonian model retains permanent memory and is distinct from the historical constant-mass, exhaust-neglected figure reconstruction.

For the specified geometry the asymptotic source $h_+$ memory is $6.0060\times10^{-20}$. This amplitude alone is not the signal measured by the four-second target statistic. After target demeaning, the symmetric Hann window and the declared Fourier selection, the fractions of the target $h_+$ window power lying in $64$–$768$ Hz are $3.5210\times10^{-4}$, $5.9234\times10^{-10}$ and $2.6078\times10^{-13}$ for the three durations. These are finite-window processing fractions, not fractions of total gravitational-wave radiated energy. The ten-second burn begins at $61$ s, so its first three seconds occur in the nominal reference interval; its physical strain also continues beyond the observed $68$ s. We retain both features rather than enforcing a signal-free reference or turning off the memory at a window boundary.

The compact-pair model uses two equal compact point masses of $10^{24}$ kg. Kepler’s law determines the component orbital radius for each specified gravitational-wave frequency. It is a kinematic source also compatible with natural systems, not a demonstration that an ordinary-material engineered structure could be constructed.

| $f_{\rm GW}$ (Hz) | Component radius (m) |                 $v/c$ | Omitted $68$ s phase evolution (rad) |
|------------------:|---------------------:|----------------------:|-------------------------------------:|
|                64 |              744.553 | $4.9935\times10^{-4}$ |                $8.9144\times10^{-7}$ |
|               256 |              295.476 | $7.9267\times10^{-4}$ |                $1.4376\times10^{-4}$ |
|               512 |              186.138 | $9.9870\times10^{-4}$ |                $1.8257\times10^{-3}$ |

Source-only compact-pair validity checks at leading quadrupole order. No actual detector-noise sensitivity is inferred.

The shortest leading coalescence time among these choices is approximately $48.4$ yr. The source is therefore treated as a persistent circular signal over this observation, with the stated small but nonzero omitted radiation reaction. In a source-only forward calculation, each detector’s target to median-reference selected-band energy ratio equals unity to about $10^{-15}$. Thus persistence in both intervals can be normalized away by this statistic even when the source frequency lies in band. This finding is a noiseless processing result, not a measured probability of detection in the real cached data. The separately declared 48 noisy responses are reported below and are kept distinct from this source-only calculation.

The analytic source tests independently check mass and momentum conservation, the total rocket–exhaust quadrupole and transverse–traceless projection, Kepler balance, amplitude scaling, full-history injection and common samples at $4096$ and $16384$ Hz. Forty-two implementation checks passed. They do not establish an exact relativistic source solution, a feasible engine, artificial origin, or a calibrated false-alarm probability.

## Registered cached-noise response study

The registered run used the first eligible context in the first and last opened source block of each epoch, corresponding to plan indices $[0,8,12,20]$. These four contexts cover four previously opened physical blocks, not four new validation blocks. Six fixed configurations comprise three rocket burn durations and three compact-pair frequencies at the common distance and orientation stated above. Each has an original projection and the retained detector-index extra-delay control, giving 48 variants. All 24 original baselines are replayed and required to match before these responses are calculated. The old cuts and underlying score implementations are unchanged. Signal may alter the reference as well as the target.

The Windows calculation evaluated all 24 baseline records and 48 source-model variants in 63.453 s, or 68 s including process supervision, without new data acquisition or neural-model evaluation. Independent retained-result checks reproduced the assessment. Because the original noise arrays were not included in those retained results, this verification did not repeat the calculation from strain. The measured table is not populated with source-only predictions or synthetic Gaussian-noise results.

<figure id="fig:physical_sources">
<embed src="figures/PHYSICAL_SOURCE_MODELS.pdf" />
<figcaption>Specified source waveforms before real detector noise is added. The rocket memory continues beyond the record, and the long burn affects the reference. The compact pair exists in both reference and target. These are source predictions at the declared mass, distance and orientation, not detected signals or source-population bounds.</figcaption>
</figure>

## Physical-source forward response

The returned Windows run completed the 24 unchanged baseline replays and all 48 prespecified physical-source variants. The latter comprise six source configurations, their original and extra-delay copies, and four already-open noise contexts (two in each epoch). These are four reused source blocks, not a new independent validation sample. All mass, motion, distance, orientation and timing parameters were fixed before the new scores; the source distance was $D=0.01\,\mathrm{pc}$ in every configuration. No $h_{\rm rss}$ renormalization, threshold refit, new neural-encoder inference or network acquisition was performed.

<div id="tab:p3actual">

| Source configuration             | correlation ratio orig. | correlation ratio delay | Orig. up/down | Delay up/down | energy ratio |
|:---------------------------------|:---------:|:---------:|:-------------:|:-------------:|:------:|
| Rocket, $T=0.01\,\mathrm{s}$     |    4/4    |    1/4    |      3/0      |      1/1      |  0/4   |
| Rocket, $T=0.1\,\mathrm{s}$      |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Rocket, $T=10\,\mathrm{s}$       |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $64\,\mathrm{Hz}$  |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $256\,\mathrm{Hz}$ |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |
| Compact pair, $512\,\mathrm{Hz}$ |    1/4    |    1/4    |      0/0      |      0/0      |  0/4   |

Source-model fixed-cut exceedances. The up/down columns count correlation ratio upward/downward threshold transitions relative to matched uninjected baselines, out of four trials per row and control. One of the four selected baselines was already correlation ratio positive; therefore 4/4 above-cut outcomes for the shortest rocket contain three new crossings. The energy ratio also remains below its cuts for all 24 delayed copies. Fractions describe this finite grid, not population efficiency.

</div>

For the $0.01\,\mathrm{s}$ rocket–exhaust memory source, the original correlation ratio scores are $1.8697$, $2.8164$, $2.5991$ and $2.5063$, against matched baseline scores $1.1936$, $1.1460$, $1.0266$ and $1.2475$. The short source thus produces a positive, parameter-explicit response in both epochs. Its delayed copy is still accepted in the first O4a context, where it creates an upward crossing; the formerly positive last O4b context moves below the cut. This gives one upward and one downward crossing for the four delayed short-rocket trials, with zero net lift. Acceptance of this delayed copy retains the known timing-specificity limitation.

The $0.1$ and $10\,\mathrm{s}$ rockets and all three persistent compact-pair configurations produce no new crossings in either method at the specified parameters. Their correlation ratio exceedances all inherit the same positive O4b baseline. This is compatible with the source-only diagnostic showing strong loss of processed in-band power for longer memory rises, and with the target/reference normalization of a source present throughout the record. It does not establish that reference normalization alone causes every noisy non-crossing. The full physical source was retained: all 24 compact-pair units and eight long-rocket units alter the 64-s reference, for 32/48 units in total; the remaining 16 short-rocket units leave it bitwise unchanged.

Across the 24 original units, the correlation ratio has 9 exceedances, six matched-baseline exceedances, three upward crossings and no downward crossings. The 24 delayed units have six exceedances, six matched-baseline exceedances, one upward and one downward crossing. The energy ratio has no exceedances or crossings in either group. The original-group descriptive net-lift difference is $J_{\rm corr}-J_{\rm energy}=3/24=0.125$; it is not an equal-FAR performance claim or a significance test. These injections establish the explicit source–detector–measured-response link for two stated Newtonian source approximations, with strongest response in the shortest rocket case. They are not observed celestial events, an engineered-origin inference, a range/rate exclusion, a general detection-efficiency estimate or a demonstration of engineering feasibility. The negative source-disjoint validation decision and the structured-packet timing limitation remain unchanged.

# Numerical validation of the correlation calculations

The broad-lag calculation evaluated 216 previously inspected records, comprising 24 baselines, 144 structured-packet variants and 48 source-model variants. The 432 detector-pair records contain 864 curves. Recorded execution took 232.328 s, or 240.860 s including process supervision. The physical-source response evaluated 24 baselines and 48 variants in 63.453 s, or 68 s including supervision. These computational measurements do not add observational exposure.

# Sequential design and inference boundaries

## Preserving prespecified negative outcomes

Execution completion and a scientific success screen are distinct. The learned-ranking pilot and six-source-block validation both completed the declared records and returned negative scientific decisions. Those outcomes are retained, including the unfavorable O4b B03 block and the O4a noise-guard failure. Source substitutions, removal of difficult controls, pooling of epochs against the original rule, or threshold refitting on an opened validation cohort would define a new development analysis. None was used to rewrite a completed decision.

The adaptive chronology matters. The correlation score followed the learned-ranking pilot and exploratory alternatives, and its two-block development result was not independent confirmation. The six-source-block validation was then specified on new source blocks. The structured-packet study followed the disclosure of six-source-block validation and reused its noise. We therefore describe the structured-packet study as an exploratory structured-signal extension, even though the structured-packet study signal definition and cuts were fixed before that particular execution. Source disjointness is a useful design property, but does not by itself establish independent and identically distributed draws or exchangeability.

## Numerical consistency of retained calculations

A saved-intermediate consistency check evaluated 6864 scalar comparisons across 264 records; the largest absolute difference was $1.7763568394002505\times10^{-15}$. All 240 injection records retained the reference statistics of their matched baselines. This is arithmetic validation of retained intermediates, rather than an independent repetition from raw strain. The structured-packet calculation completed 24 baselines and 144 variants in 87.141 s, or 89.422 s including process supervision, using Python 3.11.9 and NumPy 2.3.2. Operational interruption and archive-repair details are retained with the reproducibility materials.

## Thresholds and denominators

<div id="tab:frozen_cuts_audit">

| Method   |                O4a |                O4b |
|:---------|-------------------:|-------------------:|
| learned-ranking pilot |  72.59910579834697 | 33.992707434802746 |
| correlation ratio      | 1.2127042400481731 | 1.2033275141068391 |
| Energy   | 1.1835502945794922 |  1.079756725627839 |

fixed transported cuts used in the completed finite comparisons. All decisions use strict $s>c$. learned-ranking and correlation ratio have different score definitions and are not numerically interchangeable.

</div>

The calibration comparison used 12 old calibration contexts per epoch. It is not a physical false-alarm-rate calibration. The six-source-block validation noise guard uses four unmodified contexts per block, including contexts not selected for injection. By contrast, the paired net upward-crossing fraction defined above uses only the injection contexts and repeats their own baseline decisions once per variant. In the structured-packet study those repetitions give eight baseline-positive correlation ratio examples and four baseline-positive energy examples in each 48-variant control group; these counts are not eight and four additional independent noise events.

## Available evidence and inference limits

The targeted primary-source adjudication recognizes established cross-correlation, coherent burst reconstruction, anomaly-feature learning, and injection/background workflows. The completed comparisons do not benchmark against GWAK, CoAD, X-Pipeline, or cWB on matched strains at a common calibrated operating point. Reproducible implementation and checkpointing are useful methodological properties, but are not by themselves proof of a new detector principle or superior performance. These comparisons concern the tested statistics and do not establish their equivalence to the cited pipelines.

The earlier project history mentions three radial score heads and a no selected observation decision. The currently inspected observational and learned-ranking-pilot primary archives do not contain the original radial-head result archive. Therefore their detailed numerical performance is not promoted here to an independently source-verified result. That stage is retained in the result register as requiring its original evidence. It must be filled from the corresponding source record, rather than inferred from the later six-source-block validation protocol’s historical summary.

No completed experiment above supplies a population physical FAR/FAP, discovery significance, sky-averaged sensitivity, decoded extraterrestrial message, verified engineered source, or a rate/distance exclusion. The legacy three-of-4096 full-search trial state and the 4096 conditional learned-ranking draws remain separate quantities. The combined measurements support a finite validation study with both positive responses and demonstrated specificity limits.

## Controlled-benchmark family and nominal-amplitude summaries

The controlled-benchmark family–amplitude summary below preserves every family/amplitude cell in the retained benchmark summary. These are reported median consensus learned-ranking scores, not newly computed values or physical efficiencies. In particular, nonmonotone score medians across the nominal levels are retained rather than replaced with a monotone fit. Counts refer to distinct case identities per amplitude and are not multiplied by the three model seeds.

<div id="tab:f6_nominal_scores">

| Epoch | Class           | Family           | $n$ |       0.75 |       1.00 |       1.50 |
|:------|:----------------|:-----------------|----:|-----------:|-----------:|-----------:|
| O4a   | Coherent        | Multitone packet |   8 | 554.095736 | 550.147188 | 525.122654 |
| O4a   | Coherent        | Quadratic chirp  |   8 | 491.717095 | 490.408057 | 525.243715 |
| O4a   | Single detector | Multitone packet |   4 | 325.432641 | 339.400419 | 320.916819 |
| O4a   | Single detector | Quadratic chirp  |   4 | 337.317261 | 364.344029 | 359.850836 |
| O4b   | Coherent        | Multitone packet |   8 | 376.935037 | 348.726916 | 354.064971 |
| O4b   | Coherent        | Quadratic chirp  |   8 | 373.541244 | 329.553735 | 360.794944 |
| O4b   | Single detector | Multitone packet |   4 | 212.480129 | 210.660876 | 158.869088 |
| O4b   | Single detector | Quadratic chirp  |   4 | 221.754821 | 229.158579 | 173.353010 |

Historical controlled-benchmark terminal-summary values. Columns 0.75, 1.00, and 1.50 are nominal amplitude labels without a physical strain/SNR calibration. The count is per amplitude.

</div>

The historical handoff’s last-confirmed original background pilot count was two. The later observational archive records three legacy completed full-search trials. We preserve that chronological update and do not equate either count with completion of the original 4096-trial campaign. The later learned-ranking observation’s 4096 conditional transformations are a third, different quantity.

## All six-source-block validation source-block outcomes

The six-block validation summary below retains every source block. The final column gives correlation ratio/energy counts among four unmodified noise contexts in that block. It is not a ratio of false-alarm rates. The exact source times and fractions accompany the released numerical results.

<div id="tab:fresh6_all_blocks">

| Block   | correlation ratio above | Energy above | correlation ratio up | Energy up | $\Delta J$ | Noise |
|:--------|----------:|-------------:|-------:|----------:|-----------:|:------|
| O4a B01 |     16/16 |         0/16 |  16/16 |      0/16 |        $1$ | 1/0   |
| O4a B02 |     16/16 |         0/16 |   8/16 |      0/16 |      $1/2$ | 2/1   |
| O4a B03 |     16/16 |         8/16 |  16/16 |      8/16 |      $1/2$ | 0/0   |
| O4b B01 |     16/16 |         8/16 |  16/16 |      8/16 |      $1/2$ | 0/2   |
| O4b B02 |     16/16 |        12/16 |  16/16 |      4/16 |      $3/4$ | 0/2   |
| O4b B03 |     16/16 |        15/16 |   8/16 |     15/16 |    $-7/16$ | 1/0   |

All six-source-block validation block outcomes for original injections. Each block has 16 shared-noise variants. “Up” denotes upward threshold crossings relative to the own-noise baseline.

</div>

<div id="tab:fresh6_all_families">

| Form        | Family         | $n$ | correlation ratio above | Energy above |
|:------------|:---------------|----:|----------:|-------------:|
| Original    | Chirp          |  24 |        24 |           11 |
| Original    | Repeated chirp |  24 |        24 |           10 |
| Original    | Turning chirp  |  24 |        24 |           11 |
| Original    | Modulation     |  24 |        24 |           11 |
| Reversed    | Chirp          |  24 |        24 |           11 |
| Reversed    | Repeated chirp |  24 |        24 |           10 |
| Reversed    | Turning chirp  |  24 |        24 |           11 |
| Reversed    | Modulation     |  24 |        24 |           11 |
| Extra delay | Chirp          |  12 |         0 |            8 |
| Extra delay | Repeated chirp |  12 |         0 |            8 |
| Extra delay | Turning chirp  |  12 |         0 |            8 |
| Extra delay | Modulation     |  12 |        12 |            8 |

six-source-block validation outcomes by family and control. Originals and reversals contain 24 examples per family; the extra-delay challenge contains 12.

</div>

# Related work and the finite question addressed here

Inter-detector correlation is an established burst-consistency tool, not a new observable introduced here. Cadonati’s $r$-statistic scans conditioned detector data over allowed arrival-time differences and several integration windows (Cadonati 2004, secs. 2.1–2.3). X-Pipeline projects whitened network data onto signal and null subspaces and compares coherent with incoherent energies (Sutton et al. 2010, sec. II). Coherent WaveBurst reconstructs a network response using antenna responses and gravitational-wave polarizations (Klimenko et al. 2016). Our maximum over pairwise correlations is a simpler consistency statistic. It does not fit one sky direction and common polarizations to all participating detectors, and its acceptance cannot be identified with network coherence in those methods.

Learning-based anomaly searches also supply close antecedents. GWAK combines recurrent-autoencoder reconstruction features with frequency-domain correlation and a Hanford–Livingston Pearson correlation maximized over the light-travel delay (Raikman et al. 2024, secs. 3.4–3.5). CoAD learns detector-specific predictions using cross-detector coincidence as its objective and reports signal recovery at a stated false-alarm rate (Ratner 2026). The MADGRAV preprint describes sequential anomaly detection, glitch classification, coherence testing and ranking on LIGO data (Inguglia et al. 2026, abstract). Its primary abstract and author-reported preprint status were verified; we do not rely on inaccessible full-text implementation details. Thus neither learned anomaly ranking, adding correlation, nor arranging these operations in stages is claimed as a first contribution of this study.

The appropriate discovery and sensitivity comparators are calibrated burst searches. The O3 analysis uses coherent WaveBurst with BayesWave follow-up and measures injected-signal recovery at a specified inverse false-alarm rate (Abbott et al. 2021a, secs. III–IV). The published O4a search combines coherent trigger generation with XGBoost or Gaussian-mixture classification, reports its search background, and evaluates signal-family-dependent sensitivity and rate limits (Abac et al. 2025, secs. III–V). A fixed-cut acceptance fraction on our finite panels is a different endpoint. We have not rerun GWAK, CoAD, MADGRAV, X-Pipeline or coherent WaveBurst on identical data and injections, and do not infer superiority or equal-FAR sensitivity from our energy comparison.

These works establish the methods and the standard of calibrated inference; they do not supply a performance guarantee for the particular fixed definition examined here. Our operational question is whether its constructed-signal ranking, source-disjoint noise guard, physical-delay specificity, and response to duration-preserving source injections remain compatible when evaluated separately. The contribution is a source-linked finite measurement of their divergence. Strong benchmark discrimination coexists with weaker learned response in actual strain, a failed new-source noise guard, and acceptance of deliberately over-delayed packets. The later broad-lag diagnosis explains a failure mode without turning its observed ratio separation into a validated replacement classifier. Repeated variants sharing noise or source blocks are not counted as independent experiments.

Physical interpretation requires an additional model-to-response bridge. Sellers et al. derive waveforms for accelerated massive sources with explicit trajectory and sampling assumptions (Sellers et al. 2022, sec. 2); our later rocket–exhaust approximation is separately specified rather than equated with their constant-mass reference. Clough et al. evolve a particular warp-fluid collapse model whose frequency scale depends on bubble size (Clough, Dietrich, and Khan 2024, secs. 2.1, 2.4 and 3.1). Neither structured packets nor our Newtonian injections establish an artificial source, decode a message, or test that numerical warp model. Our observational working-null result is conditional on the registered finite construction, not a global false-alarm probability or a source-population exclusion. This targeted comparison supports an incremental audit paper; it establishes neither an exhaustive literature gap nor a first technosignature search.

# Exploratory time-localized observation review

This appendix adds one saved-score reanalysis. All preceding manuscript text is preserved verbatim. It is not an independent observation or a completed full-search background.

## Exploratory time-localized review of the existing observations

After the original 192 observation scores and their descriptive timeline had been examined, two endpoints were fixed for an exploratory reanalysis of the same saved scores. This was not an unopened-source confirmation. The first endpoint was the original maximum single-window score. The second was the largest minimum score of a chronologically adjacent target pair within the same exact source block, with target starts separated by at most 160 s. This single scale corresponds to two steps of the 80-s metadata grid; it was not optimized over alternative scales. There were 136 eligible pairs. Two sampled four-second targets do not establish continuous emission or observed exposure between them.

Both endpoints were evaluated on every one of the same 4096 saved within-source-block detector-record transformations, retaining the fixed leading-detector time slots. Thus the comparisons account for searching over all eligible windows or pairs within this conditional design. A Bonferroni factor of two was applied across the two endpoints, with family level $\alpha=0.05$. The original single-endpoint result remains unchanged; the additional adjustment applies to the new two-endpoint exploratory family.

<div id="tab:timeline_results">

| Endpoint              | Observed | Exceedances | $p_{\rm cond}$ | $p_{\rm adj}$ |
|:----------------------|---------:|------------:|---------------:|--------------:|
| Single-window maximum | 116.6343 |        1711 |       0.417867 |      0.835733 |
| Adjacent-pair minimum |  60.1738 |        3121 |       0.762021 |      1.000000 |

Exploratory timeline endpoints from existing scores. Exceedances include ties among 4096 conditional transformations. The adjusted values are $\min(1,2p_{\rm cond})$; they are not global instrument-noise false-alarm probabilities.

</div>

Neither endpoint selected a window or pair at the stated family level. The largest adjacent-pair minimum came from two O4a targets starting at GPS 1383624080 and 1383624160, separated by 80 s. Its visible elevation was therefore not unusual under the stated conditional working null. The three largest individual scores and two non-overlapping pair priorities were retained solely as a descriptive audit list. Their seven distinct windows supplied 16 detector records and 32 two-rate finite checks, all passing the archived declared criteria. These checks do not establish an absence of instrumental transients. Candidate-specific phase-resolved delay measurements, a common-sky fit, a null-stream test and an external glitch-catalog check were not present in this archive-only review.

<figure id="fig:timeline_reanalysis">
<img src="figures/GW_TIMELINE_EXPLORATORY_EN.png" />
<figcaption>Existing observation scores at their actual sampled times, shown separately by observing epoch, and the two exploratory statistics compared with the unchanged conditional transformations. Circles mark the largest score in each epoch, not detections. The intervals between plotted targets are not surveyed exposure. Lower-panel vertical lines mark the observations; neither comparison rejects the conditional working null.</figcaption>
</figure>

The reanalysis read saved score and quality records, without new strain acquisition, representation inference or training. It added no independent noise livetime and left the original full-search counter at three of 4096. Within-block permutation invariance remains a working assumption rather than an established model of temporal instrument noise. The result is a bounded negative finding for this exploratory rule, not an exclusion of all anomalies or a completed discovery calibration.

# Exploratory peak and neighboring-target reanalysis

The reanalysis used the exact original foreground archive and its 192 identity scores together with all 4096 stored score vectors. The resulting array had shape $4097\times192$, including identity. Input identity was checked for the 8201 saved numerical records used by the score extraction. The saved protocol was fixed before computing the new pair statistic, but after all identity scores and the descriptive timeline had been examined. Its statistical status is therefore exploratory. No original operating cut, selected membership, source exclusion, trained model or old result was changed.

For fixed sampled target times $t_i$, exact source-block labels $b_i$ and saved consensus scores $S_i^{(r)}$, where $r=0$ denotes identity, let $$\begin{aligned}
\mathcal{E}&=\{(i,j): b_i=b_j,\ i,j\text{ consecutive within }b_i,
                    \ 0<t_j-t_i\le160\,{\rm s}\},\\
P_r&=\max_{1\le i\le192}S_i^{(r)},\\
C_r&=\max_{(i,j)\in\mathcal{E}}
                         \min\{S_i^{(r)},S_j^{(r)}\}.
\end{aligned}$$ The single fixed scale is two original 80-s metadata-grid steps. In particular, no smoothed trace, additional time scale or fitted amplitude threshold was searched. A high pair minimum requires both sampled targets to have elevated scores, but says nothing about the unobserved interval between their four-second targets. The fixed geometry contained $|\mathcal{E}|=136$ pairs.

For $T\in\{P,C\}$, the same rule was applied to identity and every saved map: $$p_T=\frac{1+\sum_{r=1}^{4096}\mathbf{1}\{T_r\ge T_0\}}{4097},
\qquad p_{T,\mathrm{adj}}=\min(1,2p_T).$$ A point-level follow-up value was compared against the whole-graph single-window maxima; a pair-level value was compared against the whole-graph pair maxima. The same factor of two was then applied. This accounts for the specified window/pair searches and two endpoints under the supplied conditional working null; it does not calibrate arbitrary additional visual patterns. The H1 record and time slot remained fixed, while whole L1 and, where present, V1 bundles were independently permuted within each exact block as in the original design. The transformations reuse physical records, do not establish temporal stationarity or exchangeability, and add no independent background duration. In particular, the pair analysis is not evidence that all temporal-noise correlations are preserved by shuffling donor records.

The observed single-window maximum was $P_0=116.63425977697752$, with 1711 exceedances and $p_P=1712/4097=0.41786673175494266$. The observed adjacent-pair minimum was $C_0=60.17383564033912$, with 3121 exceedances and $p_C=3122/4097=0.7620209909690017$. Their two-endpoint adjusted values were respectively $0.8357334635098853$ and $1$. No single peak or pair met the stated family criterion. No new coherent-gravitational-wave or technological-source candidate was thereby established.

<div id="tab:timeline_priorities">

| Priority      | Target-start GPS        |    Score | $p_{\rm adj}$ |
|:--------------|:------------------------|---------:|--------------:|
| Single 1, O4a | 1382654880              | 116.6343 |      0.835733 |
| Single 2, O4a | 1383608640              |  98.5419 |             1 |
| Single 3, O4a | 1383108960              |  88.9271 |             1 |
| Pair 1, O4a   | 1383624080 / 1383624160 |  60.1738 |             1 |
| Pair 2, O4b   | 1416414080 / 1416414160 |  44.2390 |             1 |

Descriptive audit priorities, not statistically selected events. Pair scores are the smaller of their two constituent scores. Full event, source, quality and embedding identities are supplied in the saved audit.

</div>

The audit list used the three highest individual scores and two greedily chosen non-overlapping pairs, irrespective of statistical acceptance. It contained seven distinct windows, 16 detector embedding records and 32 finite checks. Their saved embeddings agreed with the corresponding network-bank entries; all declared per-rate finite and full-context quality criteria passed. Across the full observation archive, the 480 detector records have 960 passing per-rate finite checks. The declared 68-s criteria were valid strain, category-2 burst-quality, compact-binary hardware-injection exclusion, burst hardware-injection exclusion, detector-characterization hardware-injection exclusion and stochastic-background hardware-injection exclusion. These checks are an archived quality/provenance review, not a raw-strain replay or proof that all glitches are absent.

Continuous-wave hardware-injection flags were annotations under the original observation contract, not vetoes. The archived continuous-wave hardware-injection flag is false for H1 and L1 in every full-context support bin at both rates, while the V1 annotation is true. Thus this archive cannot be described as continuous-wave-hardware-injection-free. The annotation does not establish that an injection caused a score peak, and no retrospective veto was introduced. The archived learned pair statistic remained diagnostic only. Phase-resolved strain was not included in the embedding return, so no new candidate-specific arrival-time measurement, sky fit, null stream or external glitch-catalog record is claimed. With no statistically selected candidate, none was promoted to costly physical follow-up in this bounded review.

The score extraction and analysis took 2.3101 s on the review host, excluding figure production, auditing and manuscript compilation. This is reuse of completed inference, not a new raw-data throughput measurement or a speedup estimate for the original 4096 full-search campaign. The latter remains three of 4096. The new result, fixed rule, all 192 single-window values, 136 pair values, 4096 null endpoints and seven-window evidence audit are included in the accompanying reanalysis bundle. The exact input identities accompany the released analysis.

# Randomized detector-record sample and numerical reproducibility

This completed survey follows the historical experiments without changing their inputs, cuts, decisions or completion units. The distinct counters are retained explicitly.

| Record or experiment | Retained status | Unit and interpretation |
|:---|:---|:---|
| Legacy full-search background campaign | 3/4096 | Completed legacy full-search trials; not updated by the new detector-record survey. |
| H1 conditional-noise assay | 10/4096 | Conditional donor units with fixed other-detector observations. |
| Registered within-source transformations | 4096/4096 | Dependent transformations of the retained 192-target observation. |
| New randomized H1 detector-record survey | 4096/4096 audited; 4020 finite vectors | 76 quality rejections and 0 input rejections; no unresolved selected records. |

## Sampling, support and data integrity

The new allocation uses the corrected, fixed and identity-verified metadata frame after all protected-source exclusions, rather than the earlier illustrative five-stratum proposal. The resulting eligible source counts are 136 O4a/H1 and 203 O4b/H1. All 4096 selected source/GPS keys, candidate queues, source-group roles, inclusion probabilities and protected physical intervals accompany the results. Source selection was without replacement, but source reuse in earlier opened development/calibration containers is annotated. The scope is therefore exploratory and source-grouped, not fresh global confirmation. The full sample comprises 256 distinct source-time groups, with 16 nonoverlapping 68-second supports in each. Target exposure and context exposure remain distinct, and no unobserved interval is filled by the display.

Whole HDF5 source files were verified against publisher checksums before measurement; each accepted support was required to contain 278528 finite float64 samples on the declared grid. Independent record auditing verified fixed membership, source identities, implementation/runtime bindings, quality disposition and preservation of earlier record identities. That audit did not independently reread every raw strain array, and must not be called an additional raw-data replication. Completed record accounting is separate from finite-feature status.

All accepted and rejected outcomes retain valid-strain, category-2 burst-quality and compact-binary hardware-injection exclusion, burst hardware-injection exclusion, detector-characterization hardware-injection exclusion and stochastic-background hardware-injection exclusion evidence over the complete support. The mandatory continuous-wave hardware-injection flag was not added retrospectively as a veto. Quality exclusion does not show that every retained record is free of instrumental disturbance; the follow-up did not supply a complete auxiliary-channel or glitch-catalog investigation.

## Fixed features and model reuse

Robust feature ranking denotes the fixed maximum-deviation score described below. The local reference-power comparator is an energy ratio; the two statistics use distinct normalization rules.

The numerical feature source was fixed before strain access. The largest robust standardized deviation over the active feature dimensions defines the main score, separately fitted by run on valid training data only. MAD is multiplied by 1.482602218505602; the interquartile fallback divides IQR by 1.348979500392164, zero-scale dimensions are omitted, and the complete fitted model is retained. All 19 scalar features and absolute/reference diagnostics accompany the score. The feature screen makes no neural-model call and trains no representation. It must not be conflated with the earlier learned embedding/ranking pathway, whose recovered checkpoints have different raw-input replay requirements.

Carrier and envelope autocorrelations are within-target structure summaries. The actual-GPS descriptive periodogram uses a coarse fixed 4096-frequency grid and the observation window; it does not concatenate gaps or provide a recurrence significance. Permuting the timestamps of precomputed scores would leave their maximum unchanged and cannot calibrate the morphological maximum. No timestamp-permutation discovery probability is reported.

| Run | test records | Largest grid-peak period s | Normalized periodogram power | Sampling-window power at peak |
|:---|:---|:---|:---|:---|
| O4a | 426 | 283.369 | 0.0918 | 0.0008 |
| O4b | 424 | 687.311 | 0.0779 | 0.0006 |

The listed periods identify maxima on that fixed descriptive grid only. No source period, preferred recurrence, p-value or extrapolation across unobserved gaps is inferred. The full frequency grid and the sampling-window diagnostics accompany the released analysis.

<figure id="fig:cpu4096_carrier">
<img src="figures/CPU4096_CARRIER_ACF.png" />
<figcaption>Carrier autocorrelation peaks in the finite H1 target records, at actual GPS times and with the fixed source-group roles. The signed, zero-lag-normalized linear ACF is maximized only within its declared short-lag interval. This range-limited feature is neither a source-period estimate nor proof of phase-coherent persistence between separated records. Exclusions have no computed ACF and sampled gaps remain visible.</figcaption>
</figure>

<figure id="fig:cpu4096_envelope">
<img src="figures/CPU4096_ENVELOPE_ACF.png" />
<figcaption>Analytic-envelope autocorrelation peaks of the same H1 targets over the fixed 0.08–1-s lag interval. Envelope structure is a separate observable from carrier phase. Its uncalibrated extremum is not evidence of communication, a preferred physical source or recurrence across unobserved time.</figcaption>
</figure>

## Spectral diagnostics of the fixed review ranks

The following values are from the same conditioned target and reference periodograms used by the fixed feature extractor, before target PSD division by the reference. The bin fractions refer to the retained spectral band. These are measured features, not calibrated line-identification probabilities.

| Target GPS | Target peak Hz | Target peak fraction | Reference peak Hz | Reference peak fraction | Floor-regularized fraction |
|:---|:---|:---|:---|:---|:---|
| GPS 1384223040 | 508.25 | 0.3743 | 508.25 | 0.3078 | 0.0 |
| GPS 1416849600 | 510.75 | 0.3869 | 510.75 | 0.4524 | 0.0 |
| GPS 1416849120 | 510.75 | 0.2512 | 507.25 | 0.2506 | 0.0 |
| GPS 1416850000 | 510.75 | 0.5659 | 510.75 | 0.4995 | 0.0 |
| GPS 1418424800 | 510.75 | 0.6342 | 510.75 | 0.6344 | 0.0 |
| GPS 1418647040 | 510.75 | 0.6029 | 510.75 | 0.6181 | 0.0 |
| GPS 1418647120 | 510.75 | 0.6219 | 510.75 | 0.6202 | 0.0 |
| GPS 1418647200 | 510.75 | 0.6164 | 510.75 | 0.6317 | 0.0 |

Reference peak power demonstrates that narrowband structure was not confined to the four-second target. Neither its persistence nor the continuous-wave hardware-injection annotation identifies its physical origin. Hardware-injection, detector-line and environmental comparisons at the actual GPS/frequency would require additional release-specific evidence; a numerical regularizer did not create the ranked bins in these records.

## Finite injection response and noise transfer

The 12 fixed contexts were allocated by test source group before assay score access. Each noise baseline was bitwise replayed against its survey feature record. Signal addition preceded full-support conditioning, so any signal in the 64-second reference was retained. The fixed nominal group cuts, ordinary crossings, baseline-positive cases, context new crossings and source-group new crossings are released individually. No target was substituted after an unfavorable quality or response result. The table reports all four families and all three amplitudes, with their actual eligible denominators.

| Family | RMS ratio | Contexts | Feature-ranking new | Energy new | Feature-ranking group new | Energy group new |
|:---|:---|:---|:---|:---|:---|:---|
| Persistent line | 0.5 | 12 | 0 | 0 | 0 | 0 |
| Persistent line | 2.0 | 12 | 0 | 0 | 0 | 0 |
| Persistent line | 8.0 | 12 | 0 | 0 | 0 | 0 |
| Phase-coded packets | 0.5 | 12 | 12 | 0 | 11 | 0 |
| Phase-coded packets | 2.0 | 12 | 12 | 11 | 11 | 11 |
| Phase-coded packets | 8.0 | 12 | 12 | 12 | 11 | 12 |
| Sine-Gaussian | 0.5 | 12 | 12 | 0 | 11 | 0 |
| Sine-Gaussian | 2.0 | 12 | 12 | 11 | 11 | 11 |
| Sine-Gaussian | 8.0 | 12 | 12 | 12 | 11 | 12 |
| Turning chirp | 0.5 | 12 | 6 | 0 | 5 | 0 |
| Turning chirp | 2.0 | 12 | 6 | 11 | 5 | 11 |
| Turning chirp | 8.0 | 12 | 12 | 12 | 11 | 12 |

The finite test source-group noise behavior was:

| Run | Method | Exceeding test groups | Groups with valid records |
|:---|:---|:---|:---|
| O4a | Feature ranking | 2 | 27 |
| O4a | energy ratio | 1 | 27 |
| O4b | Feature ranking | 0 | 27 |
| O4b | energy ratio | 2 | 27 |

These noise responses are descriptive held-out source-group counts at cuts learned from the separate calibration groups. They do not establish a time-based false-alarm rate or an independently calibrated physical search. Context responses at a group-maximum cut are not per-record fixed-FAR recoveries. The source-group endpoint tests the same maximum operation used by the cut but remains dependent on a small, potentially nonexchangeable finite noise sample. In particular, favorable injection recovery cannot erase a high noise response, and an absence of new crossings can reflect an already-positive unmodified group. The paired differences are exploratory finite-panel effects, not population superiority estimates.

## Coeval detector timing measurements

Every selected test review record has a follow-up disposition, including unavailable or quality-rejected partners:

| Run | Target GPS | Quality-valid detectors | Disposition |
|:---|:---|:---|:---|
| O4a | 1384223040 | H1, L1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1416849600 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1416849120 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1416850000 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1418424800 | H1, L1 | H1–L1 timing evaluated; required V1 source verification unavailable |
| O4b | 1418647040 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1418647120 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |
| O4b | 1418647200 | H1, L1, V1 | Timing evaluated for all requested, quality-accepted detectors |

For each measured pair, the table gives its broad raw and envelope peak lag in milliseconds, followed by whether the entire exact maximizing set has any intersection with the physical cap. If multiple broad maxima tie, the displayed lag is the first in ascending signed-lag order; all tied samples are retained numerically. A yes/no is diagnostic and does not define a newly validated acceptance decision.

| Target GPS | Pair | Cap samples | Raw lag ms; cap intersection | Envelope lag ms; cap intersection |
|:---|:---|:---|:---|:---|
| GPS 1384223040 | H1–L1 | 41 | -121.094; no | -311.279; no |
| GPS 1416849600 | H1–L1 | 41 | -136.475; no | 27.832; no |
| GPS 1416849600 | H1–V1 | 111 | 172.852; no | -129.883; no |
| GPS 1416849600 | L1–V1 | 108 | -191.895; no | 80.078; no |
| GPS 1416849120 | H1–L1 | 41 | -28.809; no | 67.871; no |
| GPS 1416849120 | H1–V1 | 111 | -178.223; no | -31.738; no |
| GPS 1416849120 | L1–V1 | 108 | -244.141; no | 35.889; no |
| GPS 1416850000 | H1–L1 | 41 | 302.979; no | -63.721; no |
| GPS 1416850000 | H1–V1 | 111 | 52.490; no | 61.523; no |
| GPS 1416850000 | L1–V1 | 108 | -151.611; no | -82.031; no |
| GPS 1418424800 | H1–L1 | 41 | -55.420; no | -12.451; no |
| GPS 1418647040 | H1–L1 | 41 | 6.348; yes | -45.166; no |
| GPS 1418647040 | H1–V1 | 111 | -147.461; no | -30.273; no |
| GPS 1418647040 | L1–V1 | 108 | -291.504; no | -3.418; yes |
| GPS 1418647120 | H1–L1 | 41 | -134.033; no | -17.334; no |
| GPS 1418647120 | H1–V1 | 111 | 173.340; no | 37.842; no |
| GPS 1418647120 | L1–V1 | 108 | -237.305; no | 54.443; no |
| GPS 1418647200 | H1–L1 | 41 | -263.916; no | -30.273; no |
| GPS 1418647200 | H1–V1 | 111 | 207.031; no | -19.287; yes |
| GPS 1418647200 | L1–V1 | 108 | -148.438; no | 64.453; no |

The review is not a common-sky polarization fit, null-stream test, physical-event attribution or calibrated detection. A missing metadata-index alias does not prove that the detector was absent. All source-access failures, publisher checksums, quality dispositions, signed curves and portable bounded input arrays are retained where produced. No candidate-specific environmental or hardware-injection cause is assigned merely from a quality annotation or spectral feature.

## Execution and repeatability

Grouped source reads and reuse of finished feature records reduce redundant work without reducing the selected record count. The campaign's fixed deadline and record chain survive resumptions. The transfer interruption and append-only acquisition-resource amendment are preserved rather than erased from the execution record. The original source-transfer ledger's conservative debit includes uncertain failed opens, so it is not a measurement of physical bytes received. Network transfer, local measurement, assay, follow-up, figure production and manuscript rendering are distinct costs. The completed host survey's numerical profile is recorded separately from the original Windows neural environment.

Displaying saved plots and recounting numerical outputs are distinct from evaluating strain again. Source selections, input identities, training/calibration/test allocations, fitted robust reference values, 19-feature tables, scores, timing measurements and recorded costs permit numerical verification and reproduction. This new non-neural real-strain execution does not close the still-separate original full-network null campaign.

# Additional retained scientific figures

The following figures preserve earlier completed analyses and source-scope calculations alongside the five unique products used by the historical main text and timeline supplement, and the four additional displays of the completed randomized survey. They are displays of the recorded experiments or explicitly labelled source-scale calculations. Repeated displays of the same observations do not add independent exposure or new observations. The figure index records the source archive, retained image identity, numerical inputs and available source scripts for every product.

<figure id="fig:atlas_observation_conditional">
<img src="figures/F7_CONDITIONAL_RESULT.png" />
<figcaption>Registered conditional observation result for the 192 selected four-second targets. The observed maximum learned-ranking score is compared with 4096 conditional transformations. There were 1711 exceedances including ties, giving the registered result p = 1712/4097, which did not reject its working null. These transformations are not 4096 new physical full-search trials. The retained numerical result and transformation maxima permit regeneration of this display without a new strain or neural-model evaluation.</figcaption>
</figure>

<figure id="fig:atlas_learned_pilot">
<img src="figures/PILOT_RECOVERY_COMPARISON.png" />
<figcaption>Completed strain-level pilot for the fixed learned ranking. Left: recovery fractions within the six declared physical evaluation blocks. Right: equal-source-block recovery, 0.125 for the learned ranking and 0.625 for energy ratio. The primary panel contained 64 original injections in eight shared noise contexts; ordinary cut exceedances were 12/64 and 40/64, respectively. The panel did not support expansion of the tested learned ranking. Fixed-cut recovery in a small dependent panel is not a matched false-alarm-rate superiority measurement. The archived result, original plotting source and retained image are preserved together.</figcaption>
</figure>

<figure id="fig:atlas_correlation_development">
<img src="figures/KORELASYON_DEV_KARSILASTIRMA.png" />
<figcaption>Correlation development on four opened contexts from two physical source blocks, using the archived cuts calibrated from 24 contexts. Original-injection exceedances were 32/32 for correlation ratio, 24/32 for energy ratio and 0/32 for the fixed learned ranking. The other panels retain the time-reversal and extra-delay controls used in that development experiment. This favorable development response was followed by the separately reported source-disjoint six-block test; the latter failed its O4a noise guard and is not superseded by this earlier figure.</figcaption>
</figure>

<figure id="fig:atlas_physical_frequency_scope">
<img src="figures/FREKANS_KAPSAMI.png" />
<figcaption>Frequency-scale comparison for the explicitly discussed physical-source examples and the later 64–768 Hz transient branch. This is a source-scope calculation, not a measurement of an observed unusual signal. Classical stellar-orbit Dyson examples and the proposed Galactic-centre millihertz beacon require different bands and durations. A source model outside this branch is not observationally excluded by a no-candidate result inside it; changing a source scale requires a separately specified physically consistent model.</figcaption>
</figure>

<figure id="fig:atlas_initial_timeline">
<img src="figures/GW_MEVCUT_192_ZAMAN_SKOR.png" />
<figcaption>Initial descriptive timeline of the existing 192 learned-ranking observation scores at their actual GPS times. The later English timeline figure and declared maximum/neighbor-pair comparisons use the same saved observations. Gaps are not analysed livetime, and plotting separated samples does not supply scores or sensitivity in the unobserved intervals. The initial timeline motivated exploratory review rather than an unopened-data confirmation or a physical source attribution.</figcaption>
</figure>

The captions define the scientific scope of each retained figure. Source-only physical-model illustrations and actual noisy source-model study measurements remain distinct evidence classes. No technological origin, global discovery significance or source-population exclusion is inferred from this atlas.


# Neural implementation and dependency specification

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
| Temporal reconstruction head | Conv1d 256→128, kernel 3, padding 1, bias; GELU; Conv1d 128→1, kernel 1, bias. Linear interpolation returns the original temporal length, with unaligned interpolation corners. |
| TF reconstruction head | Conv2d 128→64, kernel 3, padding 1, bias; GELU; Conv2d 64→1, kernel 1, bias. Bilinear interpolation returns the original TF shape, with unaligned interpolation corners. |
| Parameter count | 1,804,082 float32 parameters in 64 model tensors per recovered checkpoint, matching the released layer declarations including projector and reconstruction heads. |
| Initialization | Kaiming-normal Conv/Linear weights, output-fan variance scaling, initialization argument ReLU-compatible initialization gain; zero biases. GroupNorm scales start at one and offsets at zero. The forward activation is GELU. |
| Excluded inputs | Detector identity, CW status and technological-source labels do not enter the network. Unwhitened log-RMS amplitude is retained externally and is not fused into the network. |
| Training cells | O4a/H1, O4a/L1, O4b/H1, O4b/L1 and O4b/V1, each with low/mid and high-frequency branches: ten cells. |
| Bounded data selection | From already integrity-verified production-training slots, choose the latest 32 greedily 68-s-spaced items per cell for internal development, and the earliest 64 spaced items ending at least 68 s before the development minimum. These are branch-specific counts, not a count of statistically independent physical observations. |
| Training extent | Six epochs, 20 logical training batches and ten development batches per epoch; up to 120 optimizer updates per seed. Branches are not mixed within a logical batch. The 20 training batches receive a deterministic seed/epoch permutation. |
| Optimizer | AdamW, one uniform parameter group, initial base learning rate $3\times10^{-4}$, weight decay $10^{-4}$, betas (0.9,0.999), epsilon $10^{-8}$; gradient L2 norm clipped to 1. |
| Actual learning rates | Epoch indices 0–5: $3\times10^{-5}$, $9.75\times10^{-5}$, $1.65\times10^{-4}$, $2.325\times10^{-4}$, $3\times10^{-4}$, $3\times10^{-4}$. Five-epoch linear warmup is followed by the first point of the inherited cosine schedule; the nominal minimum rate $3\times10^{-6}$ is not reached by this bounded fit. |
| Checkpoint rule | Strictly smallest mean internal-development composite loss; ties retain the earlier epoch. The actual bounded trainer stops at six epochs, without the generic JIT trainer's patience rule. |
| Low-memory implementation | A logical 32-item batch first evaluates projected features without parameter gradients, obtains the batch VICReg feature gradients, then replays per-item forwards/backwards with reconstruction contributions divided by 32 before one optimizer step. It is not batch-size-one training. |
| Precision and CPU controls | Float64 preprocessing followed by float32 model inputs and parameters; no mixed-precision training. Four intra-operation threads, one inter-operation thread, and deterministic operation selection are requested by the actual trainer. Exact original training library/build metadata has not been independently recovered; later inference-runtime checks must not be substituted silently. |

## Preprocessing and augmentations

The preceding 64-second reference and four-second target are linearly detrended separately. Reference PSD estimation uses four-second Hann Welch segments with 50% overlap, median averaging and density scaling. A positive floor is the maximum of float64 tiny and $10^{-12}$ times the median positive in-band PSD, falling back to all positive PSD bins if required. The target Fourier coefficients are divided by the square root of the interpolated PSD. The inverse-transformed target is hard-bandlimited at inclusive branch edges, then centered by its median and divided by $1.4826\operatorname{MAD}$. Missing positive PSD or zero/nonfinite MAD is rejected. The STFT uses periodic Hann windows, FFT divided by window sum, log10 power with a float64-tiny floor, integer starts, 50% overlap and no zero padding. Window/hop/FFT lengths are (1048,524,1048) and (4192,2096,4192), yielding 30 time frames and 404 or 870 frequency bins.

Each item produces two fixed-rule stochastic views. The temporal view receives an integer, zero-padded shift uniformly within ±0.125 s, a random sign with probability 0.5, log-uniform gain in [0.9,1.1], and Gaussian noise with RMS 0.005 times the transformed signal RMS. A contiguous mask of $\lfloor0.02N\rfloor$ samples is zeroed; its pre-mask augmented waveform is the reconstruction target. The TF view masks one uniformly selected time column across frequencies and reconstructs the original base TF array. The TF array is not recomputed after the temporal perturbations. Random generators are seeded from a deterministic combination containing the model seed, epoch, batch sequence, item index, view index and branch. Development views always use seed 20260919 and epoch zero, for all three models.

Invariance is MSE between projected views. The variance term averages the two mean hinge penalties on $1-\sqrt{\operatorname{var}(z)+10^{-4}}$, using population variance. For each view, the centered covariance is divided by $B-1$; off-diagonal squared entries are summed and divided by feature dimension, and the two view terms are added. Reconstruction averages temporal and TF masked Huber losses with delta 1, each first averaged over the two views. Only masked entries contribute. The loss weights are exactly (25,25,1,1).

## Fitted neural models and training selection

The three fitted models retain their verified original identities. Each model contains 64 tensors stored in 32-bit floating-point precision with 1,804,082 parameters; all tensor keys and shapes agree with the released architecture, and no nonfinite stored values were found. The saved optimizer states record 120 updates per parameter. Best epoch index 5 (the sixth epoch) and development losses 22.44843092896044, 21.1369436269626 and 21.111260562669486 agree exactly with the retained terminal ledger. The saved model metadata precede the final training-completion record; this difference in record timing does not imply an incomplete fit. These are file, tensor-structure and metadata checks, not a strict framework load or a neural-output replay.

The archived training schedule specifies every selected item. Its ten cells contain 640 training and 320 internal-development branch-specific items, with 960 unique slot keys and 958 distinct detector/run/GPS target triples. Two exact target starts repeat across frequency branches, and other cross-branch 68-second supports overlap within partitions. The declared 68-second spacing within each branch cell and the training/development separation across branches were verified from the schedule. These checks do not establish whole-source independence. Exact selected-item identities are available; the referenced compact training arrays and production ledger remain unavailable, so their numerical contents and selection from the full eligible pool have not been replayed.

The recovered weights supply the particular fitted parameters needed to replay the original raw-input learned embeddings and dependent learned rankings. Matching inputs and numerical-runtime validation remain necessary. Cached embedding/scorer arithmetic can be checked without running the network; direct correlation/energy, source-only physical calculations and the later structured-packet, source-model and broad-lag correlation diagnostics have their own non-neural inputs and requirements. Retraining from the declared definition produces a new replication whose agreement must be assessed, not assumed identical to the original fit.

## Neural and non-neural analysis dependencies

The following mapping distinguishes learned inputs from the statistic evaluated on them. The code-and-result audit covers the available archived evidence; it is not a live examination of the workstation or a new raw-data experiment.

| Calculation | Role of the neural models | Reproduction boundary |
|:--|:--|:--|
| Learned single-detector representation and its diagnostic criteria | Three seeded neural fits and fixed inference | The original fitted checkpoints are recovered; raw-input replay still requires matching inputs and numerical-runtime checks. |
| Source catalog and declared quality/finite checks | Metadata and numerical validation | No neural architecture is required for these checks themselves. |
| Fusion, learned ranking and representation consistency | Neural embeddings followed by standardization/PCA, nearest-neighbor distances or pair formulas | These downstream operations can use the valid retained banks; raw-to-bank replay needs the models. |
| Calibration/foreground embedding production and learned strain pilot | fixed neural inference, with an independent non-neural energy comparator in the pilot | Stored results remain inspectable; regenerating learned responses needs matching weights and inputs. |
| Correlation development | New correlation and energy calculations; the learned-score comparison reuses matched pilot outputs | No new neural-encoder calls in the correlation development run. The reused learned comparator retains its upstream dependence. |
| Six-source-block, structured-packet, physical-source and broad-lag studies | Raw correlation/energy, analytic source histories and timing diagnostics | Their archived native summaries report zero new neural-encoder calls. Matching raw inputs, numerical definitions and source parameters remain necessary. |
| Observational timeline review | Statistical reuse of retained neural-derived scores | No new model inference or new observed exposure is created. |
| Completed randomized H1 record survey | Fixed non-neural Fourier, autocorrelation and local-reference features | All 4096 selected records were audited, with finite vectors and exclusions reported separately; actual raw-strain execution is distinct from synthetic tests. |

| Experiment or computation | Retained completed count | Meaning |
|:--|:--|:--|
| Original full-search background campaign | 3/4096 | The original full-search trial unit. |
| H1 conditional-noise assay | 10/4096 | Conditional donor units with fixed other-detector observations. |
| Registered transformations of the existing observations | 4096/4096 | Transformations of the retained observation set; no new independent observing exposure. |
| Completed randomized H1 detector-record survey | 4096/4096 audited; 4020 finite vectors | Real source/GPS records, with 76 quality and 0 input exclusions. |

Thirteen synthetic feature tests and separate implementation checks accompany the numerical code. They verify software behavior rather than increasing the real-strain sample or the number of completed full-search background trials.

The three fitted neural models define the learned statistics reported here. They do not recover every earlier failed training variant, its original inputs or its numerical environment. Historical failures retain their stated evidence level. The original item schedule is now available; exact training replay additionally requires its referenced input arrays and numerical environment. Retraining with new tensors must be labeled a new replication and its numerical and scientific agreement evaluated explicitly.


\clearpage

# Fixed-packet phase-ensemble amplitude inference

This note independently checks a narrowly defined amplitude-confidence construction. It does not establish a detection, a false-alarm probability, an artificial origin, an all-sky limit, or a source-population rate. The four-Gaussian waveform was specified in the 30 October 2026 H1 secondary-assay injection plan before its assay projection, rather than in the earlier two-second eight-chip timing panel. Its use for a new bound on already examined data remains exploratory; that historical provenance does not turn this analysis into an independent confirmation.

## Signal and projection

Use the previously specified received-strain packet

$$
 h(t;A,\tau,\phi)=A e_\tau(t)\sin(\omega t+\phi),\qquad
 e_\tau(t)=\sum_{j=1}^4c_j\exp[-(t-\tau-t_j)^2/(2\sigma^2)],
$$

with $c=(+1,-1,-1,+1)$, $t_j=(0.5,1.5,2.5,3.5)\,\mathrm{s}$, $\sigma=0.04\,\mathrm{s}$, and $\omega=2\pi\,256\,\mathrm{s}^{-1}$. The carrier phase includes any constant carrier rotation induced by an arrival shift. The analytic Gaussian packet is retained rather than clipped at a four-second boundary.

The model assumes one such packet in the union of the declared supports, an initial carrier phase uniform on $[0,2\pi)$, and additive instrumental/noise strain independent of that phase. The amplitude $A\geq0$, arrival location, and arbitrary noise realization may otherwise be fixed. Noise need not be Gaussian or stationary. Other phase-correlated overlapping packets are outside this one-packet model.

At each fixed search-grid arrival, take the raw linear sine/cosine template matrix $T$, with samples multiplied by $\sqrt{\Delta}$, $\Delta=1/4096\,\mathrm{s}$. Apply the same weight to the observed raw strain vector $x$. Use a fixed raw projection window containing the four-second target $[0,4)$; the bounds below also cover an extended raw window such as $[-2,4)$. Define

$$
 G=T^\mathsf{T}T,\qquad z=G^{-1}T^\mathsf{T}x.
$$

The full-rank Gram matrix has the same $dt$-weighting. This note applies to this raw linear projection, not to nonlinear ranking, code contrast, recomputed whitening/PSD, or a filter whose response has not been included in $T$. Taking a maximum over more fixed search locations is permitted.

## Exact-grid geometric coverage

At the true grid location,

$$
 z=b+A u_\phi,\quad u_\phi=(\cos\phi,\sin\phi)^\mathsf{T},
$$

up to an immaterial interchange/rotation of the quadrature coordinates. Here $b$ is the arbitrary noise projection, independent of $\phi$. For $0\mathrel{<}r\mathrel{<}A$, the largest possible probability of a small observed norm is

$$
 \sup_b P_\phi(\|b+A u_\phi\|\leq r)
 =\frac{1}{\pi}\arcsin(r/A).
$$

To prove it, rotate $b$ to one axis and set $d=\|b\|$. In the circle-intersection regime, the probability is

$$
 \frac{1}{\pi}\arccos\!\left(\frac{A^2+d^2-r^2}{2Ad}\right).
$$

The cosine argument is minimized at $d=\sqrt{A^2-r^2}$, where it equals $\sqrt{1-(r/A)^2}$. Outside the intersection regime the probability is zero. This proves the bound, including arbitrary noise norm and orientation.

Let $M(x)$ be the maximum of $\|z\|$ over the fixed search. Because $M$ is at least the norm at the true location, for $0\mathrel{<}\alpha\mathrel{<}1/2$,

$$
 P_\phi\!\left[A\mathrel{>}\frac{M(x)}{\sin(\pi\alpha)}\right]\leq\alpha.
$$

Thus the upper endpoint has at least $1-\alpha$ coverage over random source phase, uniformly over any fixed additive-noise realization. No factor for the number of searched records/arrival locations is needed for this conservative upper endpoint: taking a larger maximum only enlarges it. This argument supplies no detection significance or noise false-alarm probability.

## Continuous arrivals and a conservative response factor

Search every native sample over $\tau\in[-0.25,0.25]\,\mathrm{s}$. Any allowed continuous arrival is within $|\delta|\leq\Delta/2$ of a grid point. At that grid point,

$$
 z=b+A B_\delta u_\phi,\qquad
 B_\delta=G^{-1}T^\mathsf{T}T_{\mathrm{true}}.
$$

If $\sigma_{\min}(B_\delta)\geq\kappa\mathrel{>}0$, then a small norm implies

$$
 \|B_\delta^{-1}b+A u_\phi\|
 \leq\frac{\|z\|}{\kappa}.
$$

The circle argument therefore gives

$$
 P_\phi\!\left[A\mathrel{>}\frac{M(x)}{\kappa\sin(\pi\alpha)}\right]\leq\alpha.
$$

To bound the response loss, absorb the carrier shift into $\phi$; only the envelope changes. The pseudoinverse norm and the envelope derivative give

$$
 \|B_\delta-I\|_2\leq
 \frac{|\delta|D}{\sqrt{\lambda_{\min}(G)}},
 \qquad D\geq\sup_\tau\|e_\tau'\|_{\Delta,2}.
$$

For $g(t)=\exp[-t^2/(2\sigma^2)]$,

$$
 \int g'(t)^2dt=\frac{\sqrt\pi}{2\sigma},\qquad
 \mathrm{TV}(g'^2)=\frac{4}{e\sigma^2}.
$$

The shifted Riemann-sum inequality
$\Delta\sum_n f(n\Delta-a)\leq\int f+\Delta\,\mathrm{TV}(f)$
holds uniformly in $a$. Minkowski's inequality over the four pulses yields the conservative discrete bound

$$
 D=4\sqrt{\frac{\sqrt\pi}{2\sigma}
          +\Delta\frac{4}{e\sigma^2}}
   =18.9230902035.
$$

Using the Gram lower bound $0.14$ established below,

$$
 \sigma_{\min}(B_\delta)\geq
 1-\frac{\Delta D}{2\sqrt{0.14}}
 =0.9938264055315.
$$

The implemented choice **$\kappa=0.99$** is deliberately smaller and hence conservative. The declared pulse-train anchor intervals total $12\times0.5=6\,\mathrm{s}$ across the 12 declared records; this is distinct from the 48 seconds of target samples. No event-rate inference is made from either number.

## Bounds on the Gaussian Gram matrix

Let $E=\int e_\tau^2dt$ and $C=\int e_\tau^2e^{i2\omega t}dt$. For the sine/cosine basis, the two whole-line Gram eigenvalues are $(E\pm|C|)/2$. The same identity holds for discrete weighted sums over the projection window.

Each product of two Gaussian pulses integrates to

$$
 \sigma\sqrt\pi\,
 \exp[-(t_i-t_j)^2/(4\sigma^2)].
$$

There are four diagonal terms and twelve ordered cross terms. Since the minimum pulse separation is one second, the magnitude of all cross terms is at most
$12\sigma\sqrt\pi e^{-156.25}$.
Thus the total envelope energy differs negligibly from

$$
 4\sigma\sqrt\pi=0.2835926161448826.
$$

For a shifted sampled Gaussian, Poisson summation bounds the relative zero-frequency quadrature error by

$$
 \epsilon_0\leq
 \frac{2e^{-\beta^2}}{1-e^{-3\beta^2}},\qquad
 \beta=\pi\sigma/\Delta.
$$

At the quadrature frequency $2\omega$, the corresponding absolute Fourier-series factor is bounded by

$$
 \epsilon_c\leq e^{-\Omega^2}
   +\frac{2e^{-(\beta-\Omega)^2}}{1-e^{-\beta^2}},\qquad
 \Omega=\omega\sigma.
$$

Here $\beta^2\mathrel{>}260000$, $\Omega^2\mathrel{>}4100$, and $(\beta-\Omega)^2\mathrel{>}200000$; both $\epsilon_0$ and $\epsilon_c$ are much smaller than $10^{-100}$. Multiplying by the sixteen product coefficients bounds the discrete quadrature anisotropy. The continuous counterpart is even more direct, with its $e^{-\Omega^2}$ factor.

For all allowed arrivals, every pulse centre is at least $d=0.25\,\mathrm{s}$ inside the target. Using $(\sum_j c_jg_j)^2\leq4\sum_jg_j^2$ and a monotone Gaussian-tail sum, the omitted target envelope energy is bounded by

$$
 E_{\mathrm{out}}\leq
 32\left[\Delta+\frac{\sigma^2}{2d}\right]
 e^{-(d/\sigma)^2}
 =1.19565\times10^{-18}.
$$

Removing samples outside the four-second target subtracts a positive-semidefinite Gram matrix whose trace is at most $E_{\mathrm{out}}$. Consequently, the deliberately loose bounds

$$
 \lambda_{\min}(G_{\mathrm{target}})\mathrel{>}0.14,
 \qquad\lambda_{\max}(G_{\mathrm{full\ packet}})\mathrel{<}0.142
$$

hold with substantial margin. A larger raw projection window containing the target preserves the lower bound. These analytic bounds are the certificate; sampled Gram checks in the validation program are corroboration.

## Received strain endpoint

For the complete Gaussian packet,
$h_{\mathrm{rss}}^2\leq0.142A^2$, including unknown phase. Therefore a conservative endpoint at $\alpha=0.1$ is

$$
 h_{\mathrm{rss},90}^{H1}
 =\frac{M(x)\sqrt{0.142}}{0.99\sin(0.1\pi)}.
$$

Here $M$ is the norm of least-squares amplitude coefficients in strain units, not a normalized matched-filter SNR. Its coverage is over the explicitly specified independent uniform source phase. It is not a posterior probability for the current amplitude and is not uniform over a fixed phase nuisance parameter.

For a linearly polarized source, $h_{H1}=F_+h_+$. A source-frame amplitude conversion requires a specified nonzero antenna factor, $h_{\mathrm{rss},+}=h_{\mathrm{rss}}^{H1}/|F_+|$. A blind antenna direction supplies no intrinsic-source bound. No distance, all-sky, transmitter-energy or technological-population bound follows automatically.

## Fixed-phase counterexample and other exclusions

For any fixed phase $\phi_0$, set the deterministic noise waveform to $n=-A T u_{\phi_0}$. Then $x=0$, every search projection vanishes, and the positive amplitude is excluded with certainty. Thus the random-phase assumption is essential; the result must not be advertised as a noise-independent, all-phase absence theorem.

No fixed-phase guarantee, claim of technological origin, calibrated detection FAP, source-rate exclusion, multiple overlapping phase-correlated packet exclusion, or adaptive-template selection guarantee is established. If template parameters or the analysis operator were chosen as a function of the same unknown source phase in the examined data, the fixed-procedure coverage argument would not apply automatically. The prior existence of the packet definition is useful provenance; this new bound remains an explicitly exploratory, model-conditional analysis.

## Numerical check

The independent phase-coverage validation program uses only the Python standard library. It checks the circle probabilities with 200000 uniform phases per noise setting, including the analytic worst case, evaluates direct sampled Gram matrices for four- and six-second raw projection windows, and records the chosen conservative response constants. It performs no GW-data access, model training or network request. At the exact-grid geometric worst case, the observed failure fraction is 0.100000, as predicted.


## Protocol, inputs and numerical result

The projection protocol and numerical results are retained with their exact input identities in the reproducibility materials. This calculation does not change the archived 4096-record survey, the original full-search count, or the successful Windows retained-table replay. All twelve supports retain their declared data-quality flags; continuous-wave hardware-injection annotation remains an annotation, not an unreported veto. The two wrong-code controls are descriptive projections and are excluded from the primary confidence calculation.

| Quantity | Actual value | Interpretation |
|:---|:---|:---|
| Contexts / source-time groups | 12 / 12 | Six O4a and six O4b H1 records; previously used contexts |
| Target samples / packet-anchor union | 48 s / 6 s | Separate GPS supports; no rate claim |
| Arrival grid | 2049 per context | Native sample spacing; continuous-offset response certificate applied |
| Observed maximum coefficient norm | $1.89915451346\times10^{-23}$ | Raw two-quadrature least-squares amplitude; not SNR |
| 90% phase-ensemble $h_{\rm rss,H1}$ endpoint | $2.33930537030\times10^{-23}\,\mathrm{Hz}^{-1/2}$ | Uniform independent phase, one specified packet, fixed analysis |
| Secondary $\alpha=0.025$ endpoint | $9.21352849850\times10^{-23}\,\mathrm{Hz}^{-1/2}$ | More conservative illustration, not a full-history selection correction |
| Injection superpositions | 109440 | 57 strengths, 32 phases, five offsets, twelve shared backgrounds |
| First tested strength with both crossing fractions at least 0.9 | $A=3.16227766017\times10^{-23}$ | True-location 1866/1920; full-search 1876/1920; not the confidence endpoint |
| Numerical runtime / peak memory | 15.545 s / 134.09 MiB | Host measurement; no network or neural evaluation |



## A variance-based envelope on the complete valid support set

This additional construction applies a different fixed projection from the six-second calculation above. On each four-second target, let $P_4$ subtract the sample mean and use $B=P_4T$. The norm of its least-squares coefficients obeys
$$\| (B^\mathsf{T}B)^{-1}B^\mathsf{T}P_4x\|_2
 \le \frac{\|P_4x\|_2}{\sigma_{\min}(B)}
 \le \sqrt{\frac{4v_T}{0.14}}.$$
The $dt$ weighting is used in both numerator and Gram matrix. To certify mean removal, define $I_q=dt\sum_ne_\tau(n\,dt)e^{i\omega n\,dt}$. The Gram loss has operator norm $|I_q|^2/4$. On the whole line the four shifted complex Gaussian sums cancel because their centres differ by an integer second and the signs sum to zero. The finite-target remainder consists only of tails, bounded for $d=0.25$ s by
$$|I_q|\le8\left(dt+\frac{\sigma^2}{d}\right)
 e^{-d^2/(2\sigma^2)}
 =1.75071197819\times10^{-10}\,\mathrm{s}.$$
The mean-removal Gram loss is therefore no larger than $7.66248107648\times10^{-21}\,\mathrm{s}$, so the deliberately loose $0.14\,\mathrm{s}$ lower bound remains valid. Since $P_4$ is a contraction, the same envelope-derivative certificate gives the declared $\kappa=0.99$. Applying the phase-ensemble argument to the virtual projection and then enlarging the endpoint by Cauchy--Schwarz gives
$$U_{h,i}^{\rm var}=
 \frac{\sqrt{4v_{T,i}/0.14}\sqrt{0.142\,\mathrm{s}}}
 {0.99\sin(0.1\pi)}
 =6.58404198073\sqrt{v_{T,i}}\,\mathrm{Hz}^{-1/2}.$$

The maximum of these per-support ceilings supplies one conservative endpoint for a single packet at an unspecified location in the declared union. The CSV entries are not 4020 independently calibrated limits. Signal phase must remain uniform independently of additive nuisance and the fixed selection/analysis, as in the sharper calculation. No noise distribution, event-rate process, source-distance model or technological-origin classification is supplied.

| Support set | Records | Minimum individual envelope | Median individual envelope | Maximum envelope |
|:---|---:|---:|---:|---:|
| O4a/H1 | 2016 | $3.46326\times10^{-18}$ | $7.01592\times10^{-18}$ | $3.52306\times10^{-17}$ |
| O4b/H1 | 2004 | $1.01332\times10^{-19}$ | $2.49929\times10^{-17}$ | $8.78940\times10^{-17}$ |
| Complete valid support set | 4020 | $1.01332\times10^{-19}$ | $9.13646\times10^{-18}$ | $8.78940\times10^{-17}$ |

All envelope values are in $\mathrm{Hz}^{-1/2}$ and are variance relaxations, not measured matched-template amplitudes. The original role counts remain 2384 training, 786 calibration and 850 test, with 256 source-time groups. In the separate test-only subset, the largest envelope was $4.56382101874\times10^{-17}\,\mathrm{Hz}^{-1/2}$; its median was $9.48890071461\times10^{-18}\,\mathrm{Hz}^{-1/2}$. The separate projection protocol and record-level source identities are released alongside the all-support CSV. Its numerical processing took 1.379 s on the host and read saved records rather than fetching additional strain. The weak global endpoint is retained rather than replaced by the sharper value from a smaller support set. The numerical summary and separate proof-validation record accompany the released results.



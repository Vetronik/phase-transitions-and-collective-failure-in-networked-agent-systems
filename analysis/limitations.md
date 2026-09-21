# Limitations ledger

- The primary confirmation has 20 graph-signal pairs per cell; bootstrap intervals describe this finite sample and do not compensate for low replication.
- The pilot was reduced from the planned E10 grid and is exploratory. The deviation is recorded in `protocol/deviations.csv`.
- Confirmation rows predate terminal error-vector storage, so covariance is measured in the separate mechanism and scaling batches.
- The size/time sweep uses one graph and five signal instances per condition. Shared-source disorder therefore creates large uncertainty across cells.
- The complete-graph criticality benchmark has short finite-time chains and a narrow coupling window. Its susceptibility maximum at the upper tested edge is not a critical-point estimate.
- Only connected random-regular sparse graphs were used for the main result. Topology, normalization, directedness, synchronous dynamics, and continuous opinions remain untested. A one-pass private-signal comparator was explored, but it changed the information representation and did not deduplicate latent common sources; genuine message-provenance effects therefore remain untested.
- The binary heat-bath model is a controlled mathematical reference, not an empirically calibrated model of humans or LLMs.

# mechanism_protocol results ledger

This file is generated from immutable run output. It is descriptive; it does not replace the preregistered analysis.

Rows: 400. Conditions: 2.

## Paired treatment contrasts

| J | q | rho_in | delta agent accuracy | delta majority score | delta severe failure |
|---:|---:|---:|---:|---:|---:|
| 3 | 0.55 | 0.25 | 0.0670 | -0.0175 | 0.2500 |

## Covariance status

```csv
N,J,q,rho_in,horizon,vbar,var_loss,cbar,rho_eff,n_eff,status,samples
128,0.0,0.55,0.25,100,0.2472451171875,0.014750386147043814,0.012919718973496913,0.05225469817346952,16.761942007670857,ok,200
128,3.0,0.55,0.25,100,0.2390099609375,0.19572869075602622,0.19538789335302248,0.8174884954025641,1.221128900491259,ok,200
```

Hierarchical uncertainty intervals are written to the accompanying CSV and resample graph clusters with signal instances nested within graphs.

Interpretation rules: agreement is not accuracy; severe-failure effects are terminal risk changes; covariance must be estimated from repeated terminal error vectors and is not inferred from agreement alone.
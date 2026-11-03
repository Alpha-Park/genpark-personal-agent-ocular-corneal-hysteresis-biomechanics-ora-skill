---
name: genpark-personal-agent-ocular-corneal-hysteresis-biomechanics-ora-skill
description: Dynamic corneal biomechanical assessment, Corneal Hysteresis (CH), Corneal Resistance Factor (CRF), and Corneal-Compensated IOP (IOPcc) quantification.
---

# Ocular Corneal Hysteresis Biomechanics (ORA) Skill

## Overview
Computes dynamic bi-directional air-pulse applanation metrics, measuring corneal viscoelastic energy absorption (Corneal Hysteresis, CH), overall elastic resistance (Corneal Resistance Factor, CRF), and tonometric correction (Corneal-Compensated Intraocular Pressure, IOPcc). Standard library only, zero external dependencies.

## Key Capabilities
- **Viscoelastic Damping Quantification**: Evaluates corneal hysteresis ($CH = P_1 - P_2$) to assess optic nerve head vulnerability and keratoconus / ectasia susceptibility.
- **Corneal Resistance Factor**: Derives structural resistance ($CRF = P_1 - 0.7 \times P_2$) reflecting corneal architecture.
- **Tonometric Compensation**: Accurately computes $IOP_{cc}$ to prevent under- or over-estimation of intraocular pressure caused by corneal thickness and stiffness variations.
- **Bilateral Asymmetry Analysis**: Detects clinically significant interocular biomechanical divergence between OD and OS.

## Reference Limits
- **Normal Corneal Hysteresis (CH)**: Population mean ~10.5 mmHg (normal threshold $\ge 8.5$ mmHg)
- **Normal Corneal Resistance Factor (CRF)**: Population mean ~10.2 mmHg (normal threshold $\ge 8.0$ mmHg)

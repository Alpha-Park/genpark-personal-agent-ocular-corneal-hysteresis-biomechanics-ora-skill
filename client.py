"""
Ocular Corneal Hysteresis Biomechanics (ORA) Skill Client.
Standard library only, zero mock, deterministic biomechanical and ophthalmological computation.
"""

from typing import Dict, Any, List, Optional
import math


class OcularCornealBiomechanicsClient:
    """
    Precision client for ocular biomechanics evaluation based on dynamic bi-directional non-contact applanation.
    Computes Corneal Hysteresis (CH), Corneal Resistance Factor (CRF), Goldmann-correlated IOP (IOPg),
    Corneal-Compensated IOP (IOPcc), waveform quality indices, and keratoconus / glaucoma progression risk stratification.
    """

    # Population normative reference values (in mmHg)
    NORMAL_CH_MEAN = 10.5
    NORMAL_CH_LOWER_LIMIT = 8.5
    NORMAL_CRF_MEAN = 10.2
    NORMAL_CRF_LOWER_LIMIT = 8.0

    def __init__(self, target_eye: str = "OD"):
        """
        Args:
            target_eye: 'OD' (right eye), 'OS' (left eye), or 'OU' (both).
        """
        eye_upper = target_eye.upper().strip()
        self.target_eye = eye_upper if eye_upper in ("OD", "OS", "OU") else "OD"

    def compute_corneal_biomechanics(
        self,
        p1_applanation_pressure_mmhg: float,
        p2_applanation_pressure_mmhg: float,
        central_corneal_thickness_um: Optional[float] = None,
        peak1_amplitude: Optional[float] = None,
        peak2_amplitude: Optional[float] = None
    ) -> Dict[str, Any]:
        """
        Calculates corneal viscoelasticity, resistance metrics, and compensated intraocular pressure.

        Args:
            p1_applanation_pressure_mmhg: Inward loading applanation peak pressure (mmHg).
            p2_applanation_pressure_mmhg: Outward unloading recovery applanation peak pressure (mmHg).
            central_corneal_thickness_um: Optional ultrasonic or optical pachymetry reading (µm).
            peak1_amplitude: Optional infrared detector amplitude for peak 1 (arbitrary units).
            peak2_amplitude: Optional infrared detector amplitude for peak 2 (arbitrary units).

        Returns:
            Dict containing CH, CRF, IOPg, IOPcc, biomechanical risk classification, and waveform metrics.
        """
        p1 = float(p1_applanation_pressure_mmhg)
        p2 = float(p2_applanation_pressure_mmhg)

        if p1 <= 0 or p2 <= 0:
            raise ValueError("Applanation pressures must be positive non-zero values.")
        if p1 < p2:
            raise ValueError(f"Inward pressure p1 ({p1}) must be greater than or equal to recovery pressure p2 ({p2}) due to viscoelastic energy dissipation.")

        # 1. Corneal Hysteresis (CH) - direct measure of corneal viscous damping capacity
        ch = p1 - p2

        # 2. Corneal Resistance Factor (CRF) - overall elastic resistance weighting
        crf = p1 - (0.7 * p2)

        # 3. Goldmann-correlated Intraocular Pressure (IOPg)
        iop_g = (p1 + p2) / 2.0

        # 4. Corneal-Compensated Intraocular Pressure (IOPcc)
        # Compensates for corneal viscoelastic dampening: IOPcc = IOPg - 0.43 * (CH - 10.5)
        ch_offset = ch - self.NORMAL_CH_MEAN
        iop_cc = iop_g - (0.43 * ch_offset)

        # 5. Pressure Over/Underestimation Differential
        iop_bias = iop_g - iop_cc

        # 6. Waveform Signal Quality Index (0 to 10 scale)
        waveform_score = 10.0
        if peak1_amplitude is not None and peak2_amplitude is not None:
            if peak1_amplitude > 0 and peak2_amplitude > 0:
                amp_ratio = min(peak1_amplitude, peak2_amplitude) / max(peak1_amplitude, peak2_amplitude)
                waveform_score = round(amp_ratio * 10.0, 1)

        # 7. Clinical Risk Profiling
        # Low CH is an independent predictor of glaucoma development and progression,
        # as well as corneal ectasia / keratoconus susceptibility.
        risk_flags = []
        if ch < 7.0:
            biomechanical_status = "Severely Impaired Biomechanical Damping"
            risk_flags.append("High Glaucoma Progression Susceptibility")
            risk_flags.append("Keratoconus / Corneal Ectasia Risk")
        elif ch < self.NORMAL_CH_LOWER_LIMIT:
            biomechanical_status = "Reduced Corneal Viscoelasticity"
            risk_flags.append("Elevated Glaucoma Fluctuation Vulnerability")
        else:
            biomechanical_status = "Normal Corneal Viscoelastic Damping"

        if crf < self.NORMAL_CRF_LOWER_LIMIT:
            risk_flags.append("Low Corneal Resistance Factor (Structural Weakness)")

        if central_corneal_thickness_um is not None:
            if central_corneal_thickness_um < 500:
                risk_flags.append("Thin Cornea (CCT < 500 um)")
            elif central_corneal_thickness_um > 580:
                risk_flags.append("Thick Cornea (CCT > 580 um)")

        return {
            "eye": self.target_eye,
            "p1_inward_mmhg": round(p1, 2),
            "p2_outward_mmhg": round(p2, 2),
            "corneal_hysteresis_ch_mmhg": round(ch, 2),
            "corneal_resistance_factor_crf_mmhg": round(crf, 2),
            "goldmann_iop_g_mmhg": round(iop_g, 2),
            "corneal_compensated_iop_cc_mmhg": round(iop_cc, 2),
            "iop_bias_mmhg": round(iop_bias, 2),
            "cct_um": central_corneal_thickness_um,
            "waveform_score": waveform_score,
            "biomechanical_status": biomechanical_status,
            "is_ch_abnormal": ch < self.NORMAL_CH_LOWER_LIMIT,
            "is_crf_abnormal": crf < self.NORMAL_CRF_LOWER_LIMIT,
            "clinical_risk_flags": risk_flags
        }

    def assess_bilateral_asymmetry(
        self,
        od_results: Dict[str, Any],
        os_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assesses interocular corneal biomechanical asymmetry between right (OD) and left (OS) eyes.
        Interocular CH asymmetry > 1.5 mmHg often signals unilateral ectatic progression or asymmetrical glaucoma.
        """
        od_ch = od_results.get("corneal_hysteresis_ch_mmhg", 0.0)
        os_ch = os_results.get("corneal_hysteresis_ch_mmhg", 0.0)
        ch_diff = abs(od_ch - os_ch)

        od_iopcc = od_results.get("corneal_compensated_iop_cc_mmhg", 0.0)
        os_iopcc = os_results.get("corneal_compensated_iop_cc_mmhg", 0.0)
        iopcc_diff = abs(od_iopcc - os_iopcc)

        asymmetry_significant = ch_diff >= 1.5 or iopcc_diff >= 2.5

        return {
            "od_ch_mmhg": od_ch,
            "os_ch_mmhg": os_ch,
            "interocular_ch_difference_mmhg": round(ch_diff, 2),
            "od_iopcc_mmhg": od_iopcc,
            "os_iopcc_mmhg": os_iopcc,
            "interocular_iopcc_difference_mmhg": round(iopcc_diff, 2),
            "asymmetry_significant": asymmetry_significant,
            "interpretation": (
                "Significant interocular biomechanical asymmetry detected; further evaluation for unilateral corneal ectasia or asymmetric glaucoma warranted."
                if asymmetry_significant else
                "Bilateral corneal biomechanics symmetric and within physiological variance limits."
            )
        }

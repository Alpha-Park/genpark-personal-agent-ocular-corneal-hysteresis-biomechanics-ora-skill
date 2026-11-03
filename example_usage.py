"""
Example usage of Ocular Corneal Hysteresis Biomechanics (ORA) Skill.
Standard library only, zero mock.
"""

from client import OcularCornealBiomechanicsClient


def run_demo():
    print("=== Ocular Corneal Hysteresis Biomechanics (ORA) Demo ===")

    client_od = OcularCornealBiomechanicsClient(target_eye="OD")
    client_os = OcularCornealBiomechanicsClient(target_eye="OS")

    # 1. Evaluate Right Eye (OD) - Normal physiological biomechanics
    od_res = client_od.compute_corneal_biomechanics(
        p1_applanation_pressure_mmhg=21.4,
        p2_applanation_pressure_mmhg=11.0,
        central_corneal_thickness_um=545.0,
        peak1_amplitude=240.0,
        peak2_amplitude=225.0
    )

    print("\n--- Right Eye (OD) Biomechanics ---")
    print(f"Corneal Hysteresis (CH): {od_res['corneal_hysteresis_ch_mmhg']} mmHg")
    print(f"Corneal Resistance Factor (CRF): {od_res['corneal_resistance_factor_crf_mmhg']} mmHg")
    print(f"Goldmann IOP (IOPg): {od_res['goldmann_iop_g_mmhg']} mmHg")
    print(f"Corneal-Compensated IOP (IOPcc): {od_res['corneal_compensated_iop_cc_mmhg']} mmHg")
    print(f"IOP Bias (IOPg - IOPcc): {od_res['iop_bias_mmhg']} mmHg")
    print(f"Status: {od_res['biomechanical_status']}")
    print(f"Risk Flags: {od_res['clinical_risk_flags']}")

    # 2. Evaluate Left Eye (OS) - Reduced hysteresis (susceptible cornea)
    os_res = client_os.compute_corneal_biomechanics(
        p1_applanation_pressure_mmhg=18.5,
        p2_applanation_pressure_mmhg=11.2,
        central_corneal_thickness_um=505.0,
        peak1_amplitude=210.0,
        peak2_amplitude=160.0
    )

    print("\n--- Left Eye (OS) Biomechanics ---")
    print(f"Corneal Hysteresis (CH): {os_res['corneal_hysteresis_ch_mmhg']} mmHg")
    print(f"Corneal Resistance Factor (CRF): {os_res['corneal_resistance_factor_crf_mmhg']} mmHg")
    print(f"Goldmann IOP (IOPg): {os_res['goldmann_iop_g_mmhg']} mmHg")
    print(f"Corneal-Compensated IOP (IOPcc): {os_res['corneal_compensated_iop_cc_mmhg']} mmHg")
    print(f"Status: {os_res['biomechanical_status']}")
    print(f"Risk Flags: {os_res['clinical_risk_flags']}")

    # 3. Interocular Asymmetry Assessment
    asymmetry = client_od.assess_bilateral_asymmetry(od_res, os_res)
    print("\n--- Interocular Biomechanical Asymmetry ---")
    print(f"CH Difference: {asymmetry['interocular_ch_difference_mmhg']} mmHg")
    print(f"IOPcc Difference: {asymmetry['interocular_iopcc_difference_mmhg']} mmHg")
    print(f"Significant Asymmetry: {asymmetry['asymmetry_significant']}")
    print(f"Clinical Interpretation: {asymmetry['interpretation']}")


if __name__ == "__main__":
    run_demo()

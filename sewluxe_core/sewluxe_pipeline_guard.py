"""
SewLuxe Pipeline Guard (حارس مسار الإنتاج الصارم)
=================================================
Enforces strict sequential execution of the Etsy Sewing Pattern Pipeline.
Prevents skipping phases, hallucinating fabric/color, or generating deliverables
before passing mandatory gates.

The Golden Sequence:
--------------------
Phase 0: CAD & Measurement Pre-Production Audit Gate (STOP & REPORT)
  - Sub-step 0.1: Visual DNA & Fabric/Color Forensics (The Single Vulnerability Law: Initial Input Precision)
  - Sub-step 0.2: Component-locked CAD configuration in PatternFast (Persistent Design ID)
  - Sub-step 0.3: Deep cross-examination (Piece inventory, ghost piece purge, seam symmetry)
  - Sub-step 0.4: A4-First Fast Audit (Page 1 calibration square, Page 2 piece inventory + specs)
  - Sub-step 0.5: Executive Pre-Production Audit Report with Visual Flat Sketch [HARD STOP: User Approval Required]

Phase 1: 1:1 CAD Flat Sketch + Photorealistic Editorial Photoshoot (3 poses)
Phase 2: PatternFast Multi-Format Batch Export (A4, Letter, A0 across all sizes)
Phase 3: 16-Page Luxury Instruction Booklet PDF (ReportLab)
Phase 3.5: Pre-Flight Automated Booklet Linter Gate (sewluxe_booklet_linter.py)
Phase 4: Standalone Customer Delivery Guides (Printing Guide, Sewing Tips Guide, Download Hub)
Phase 5: Advanced Digital Formats (Projector File PDF, Layered A0 PDF)
Phase 6: 10 High-Converting Etsy Listing Slides + SEO Package
"""

import os
import json
import sys
from typing import Dict, Any, List, Optional
from datetime import datetime

# Enforce UTF-8 output on Windows consoles
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

class PipelineGateViolationError(Exception):
    """Raised when an attempt is made to bypass a required pipeline phase or gate."""
    pass

class SewLuxePipelineGuard:
    PHASES = [
        "PHASE_0_DNA_AND_FABRIC_FORENSICS",
        "PHASE_0_CAD_CONFIG_AND_DESIGN_ID",
        "PHASE_0_A4_FIRST_AUDIT",
        "PHASE_0_USER_APPROVAL_GATE",
        "PHASE_1_CAD_FLAT_SKETCH",
        "PHASE_1_EDITORIAL_PHOTOSHOOT",
        "PHASE_2_BATCH_PATTERN_EXPORT",
        "PHASE_3_BOOKLET_COMPILATION",
        "PHASE_3_5_BOOKLET_LINTER_GATE",
        "PHASE_4_CUSTOMER_DELIVERY_GUIDES",
        "PHASE_5_ADVANCED_DIGITAL_FORMATS",
        "PHASE_6_ETSY_SLIDES_AND_SEO"
    ]

    PHASE_DESCRIPTIONS = {
        "PHASE_0_DNA_AND_FABRIC_FORENSICS": "Sub-Step 0.1: Visual DNA (The Single Vulnerability Law) + Fabric & Color Forensics",
        "PHASE_0_CAD_CONFIG_AND_DESIGN_ID": "Sub-Step 0.2: PatternFast CAD Configuration & Persistent Design ID",
        "PHASE_0_A4_FIRST_AUDIT": "Sub-Step 0.4: A4-First Fast Audit (Page 1 square, Page 2 specs, ghost pieces)",
        "PHASE_0_USER_APPROVAL_GATE": "Sub-Step 0.5: Executive Audit Report with Visual Flat Sketch & Explicit User Approval (HARD STOP)",
        "PHASE_1_CAD_FLAT_SKETCH": "Phase 1: Native PatternFast Vector Flat Sketch (1800x1800 at 300 DPI)",
        "PHASE_1_EDITORIAL_PHOTOSHOOT": "Phase 1: 3 Photorealistic Editorial Model Photos (Front, 3/4 Side, Back)",
        "PHASE_2_BATCH_PATTERN_EXPORT": "Phase 2: Multi-format batch export across all sizes (A4, Letter, A0 ZIPs)",
        "PHASE_3_BOOKLET_COMPILATION": "Phase 3: 16-Page Luxury Illustrated Instruction Booklet PDF",
        "PHASE_3_5_BOOKLET_LINTER_GATE": "Phase 3.5: Automated PDF Pre-Flight Linter Audit (Zero defects)",
        "PHASE_4_CUSTOMER_DELIVERY_GUIDES": "Phase 4: Standalone Guides (Printing Guide, Sewing Tips, Download Hub)",
        "PHASE_5_ADVANCED_DIGITAL_FORMATS": "Phase 5: Projector File PDF + Multi-Size Layered A0 PDF",
        "PHASE_6_ETSY_SLIDES_AND_SEO": "Phase 6: 10 Listing Slides (2000x2000) + Complete Etsy SEO"
    }

    def __init__(self, project_dir: str):
        self.project_dir = os.path.abspath(project_dir)
        os.makedirs(self.project_dir, exist_ok=True)
        self.state_file = os.path.join(self.project_dir, "pipeline_state.json")
        self.state = self._load_state()

    def _load_state(self) -> Dict[str, Any]:
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        
        # Initialize default state
        init_state = {
            "project_dir": self.project_dir,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "garment_dna": {},
            "fabric_spec": {},
            "patternfast": {},
            "phases": {p: {"status": "PENDING", "completed_at": None, "notes": ""} for p in self.PHASES}
        }
        self._save_state(init_state)
        return init_state

    def _save_state(self, state: Dict[str, Any]):
        state["updated_at"] = datetime.now().isoformat()
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

    def verify_gate(self, target_phase: str):
        """
        Validates that all preceding phases have passed before allowing target_phase.
        Raises PipelineGateViolationError if any prior phase is not COMPLETED.
        """
        if target_phase not in self.PHASES:
            raise ValueError(f"Unknown pipeline phase: '{target_phase}'")

        target_idx = self.PHASES.index(target_phase)
        for i in range(target_idx):
            prior_phase = self.PHASES[i]
            prior_status = self.state["phases"][prior_phase]["status"]
            if prior_status != "COMPLETED":
                error_msg = (
                    f"\n[PIPELINE GATE VIOLATION / خرق مسار الإنتاج الصارم]\n"
                    f"Cannot enter: {target_phase} ({self.PHASE_DESCRIPTIONS[target_phase]})\n"
                    f"Prior mandatory phase is NOT COMPLETED: {prior_phase} ({self.PHASE_DESCRIPTIONS[prior_phase]})\n"
                    f"Current status: {prior_status}\n"
                    f"قاعدة صارمة: لا يمكن تخطي أي مرحلة من المراحل أو العمل العشوائي بدون إتمام المراحل السابقة والموافقة الصريحة للمستخدم!"
                )
                raise PipelineGateViolationError(error_msg)

    def complete_phase(self, phase: str, notes: str = "", metadata: Optional[Dict[str, Any]] = None):
        """
        Marks a phase as COMPLETED after verifying prerequisite gates.
        """
        self.verify_gate(phase)
        self.state["phases"][phase]["status"] = "COMPLETED"
        self.state["phases"][phase]["completed_at"] = datetime.now().isoformat()
        self.state["phases"][phase]["notes"] = notes
        if metadata:
            self.state["phases"][phase]["metadata"] = metadata
        self._save_state(self.state)
        print(f"[PipelineGuard] Phase marked COMPLETED: {phase}")

    def lock_dna(self, silhouette: str, closure: str, pockets: str, back: str):
        """Locks the anatomical DNA of the garment."""
        self.state["garment_dna"] = {
            "silhouette": silhouette,
            "closure": closure,
            "pockets": pockets,
            "back": back,
            "locked_at": datetime.now().isoformat()
        }
        self.complete_phase("PHASE_0_DNA_AND_FABRIC_FORENSICS", notes=f"DNA locked: {silhouette}, {closure}")

    def lock_fabric(self, fabric_type: str, weight: str, drape: str, color_name: str, color_hex: str = ""):
        """Locks the fabric weave, weight, drape, and exact color."""
        self.state["fabric_spec"] = {
            "fabric_type": fabric_type,
            "weight": weight,
            "drape": drape,
            "color_name": color_name,
            "color_hex": color_hex,
            "locked_at": datetime.now().isoformat()
        }
        self._save_state(self.state)
        print(f"[PipelineGuard] Fabric and color locked: {fabric_type} ({color_name})")

    def register_design_id(self, design_id: int, url: str):
        """Registers the persistent PatternFast Design ID."""
        self.verify_gate("PHASE_0_CAD_CONFIG_AND_DESIGN_ID")
        self.state["patternfast"] = {
            "design_id": design_id,
            "url": url,
            "registered_at": datetime.now().isoformat()
        }
        self.complete_phase("PHASE_0_CAD_CONFIG_AND_DESIGN_ID", notes=f"Design ID {design_id} registered ({url})")

    def pass_user_approval(self, user_confirmation_text: str = "User approved in chat"):
        """Unlocks Phase 1 after explicit user approval."""
        self.verify_gate("PHASE_0_USER_APPROVAL_GATE")
        self.complete_phase("PHASE_0_USER_APPROVAL_GATE", notes=user_confirmation_text)

    def print_status_dashboard(self):
        """Prints a human-readable summary of the project pipeline status."""
        print("=" * 80)
        print(f"SEWLUXE PIPELINE AUDIT DASHBOARD: {os.path.basename(self.project_dir)}")
        print("=" * 80)
        for phase in self.PHASES:
            info = self.state["phases"][phase]
            status = info["status"]
            desc = self.PHASE_DESCRIPTIONS[phase]
            mark = "[DONE]" if status == "COMPLETED" else "[WAIT]" if status == "PENDING" else "[FAIL]"
            print(f"  {mark:<6} [{status:9s}] {phase:<36} : {desc}")
        print("=" * 80)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SewLuxe Pipeline Guard")
    parser.add_argument("--project-dir", required=True, help="Path to project directory")
    parser.add_argument("--status", action="store_true", help="Display pipeline status")
    parser.add_argument("--verify", type=str, help="Verify gate for specific phase")
    args = parser.parse_args()

    guard = SewLuxePipelineGuard(args.project_dir)
    if args.status:
        guard.print_status_dashboard()
    elif args.verify:
        try:
            guard.verify_gate(args.verify)
            print(f"[PASSED] Gate for {args.verify} is clear.")
        except PipelineGateViolationError as e:
            print(e)
            sys.exit(1)

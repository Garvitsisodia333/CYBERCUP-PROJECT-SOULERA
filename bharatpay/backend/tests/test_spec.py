import os
import json
import pytest

SPEC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../spec/openapi.json"))

def test_openapi_spec_structure_and_coverage():
    """Test 1: OpenAPI spec exists, parses valid JSON, and covers only intended public endpoints."""
    assert os.path.exists(SPEC_PATH), f"Specification file missing at {SPEC_PATH}"
    
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        spec = json.load(f)

    assert spec.get("openapi", "").startswith("3.")
    assert "info" in spec
    assert "paths" in spec

    paths = spec["paths"]
    
    # Documented endpoints that MUST be present
    expected_paths = {
        "/api/v2/auth/login",
        "/api/v2/auth/me",
        "/api/v2/accounts/{account_id}/statement",
        "/api/v2/upi/merchants",
        "/api/v2/payments/upi-transfer"
    }

    assert set(paths.keys()) == expected_paths, f"Mismatch in documented paths. Found: {set(paths.keys())}"

def test_shadow_and_zombie_endpoints_strictly_excluded():
    """Test 2: Spec strictly excludes the 2 shadow/zombie endpoints for detection testing."""
    with open(SPEC_PATH, "r", encoding="utf-8") as f:
        spec_text = f.read()

    forbidden_tokens = [
        "/api/v1/kyc/aadhaar-pan-dump",
        "aadhaar-pan-dump",
        "/api/internal/debug/override-limit",
        "override-limit"
    ]

    for token in forbidden_tokens:
        assert token not in spec_text, f"OpenAPI spec illegally contains shadow endpoint reference: {token}"

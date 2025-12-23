# Integration tests
from src.auth import LoginSystem
from src.qr_code import QRGenerator

def test_full_flow():
    """Test login → generate QR → scan QR"""
    auth = LoginSystem()
    qr = QRGenerator()
    
    # 1. Login
    result = auth.login("student1@school.com", "Student@123")
    assert result["success"] == True
    
    # 2. Generate QR
    qr_data = qr.generate_qr(result["user"])
    assert "ST001" in qr_data
    
    # 3. Scan QR
    scanned = qr.scan_qr(qr_data)
    assert scanned["name"] == "Ali Khan"
    
    print("✅ Integration test passed: Full flow works")

if __name__ == "__main__":
    print("=" * 50)
    print("RUNNING INTEGRATION TESTS")
    print("=" * 50)
    test_full_flow()
    print("=" * 50)
    print("✅ INTEGRATION TEST PASSED!")
    print("=" * 50)
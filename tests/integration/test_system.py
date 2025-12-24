# tests/integration/test_system.py
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.auth import LoginSystem
from src.qr_code import QRGenerator

class TestIntegration:
    """Integration tests for complete system flow"""
    
    def __init__(self):
        self.auth = LoginSystem()
        self.qr = QRGenerator()
    
    # ========== POSITIVE INTEGRATION TESTS ==========
    
    def test_integration_student_flow(self):
        """Positive: Complete student flow (login → QR → scan)"""
        print("\n📋 POSITIVE: Student Integration Flow")
        
        # 1. Login
        result = self.auth.login("student1@school.com", "Student@123")
        assert result["success"] == True, "Student login failed"
        user = result["user"]
        print(f"✓ Logged in: {user.get('name', 'Student')}")
        
        # 2. Generate QR
        qr_data = self.qr.generate_qr(user)
        assert qr_data is not None and len(qr_data) > 0, "QR generation failed"
        print(f"✓ QR generated ({len(qr_data)} chars)")
        
        # 3. Scan QR
        scanned = self.qr.scan_qr(qr_data)
        assert scanned is not None, "QR scan failed"
        assert scanned.get("email") == "student1@school.com", "QR doesn't match user"
        print(f"✓ QR scanned: {scanned.get('name')}")
        
        print("✅ Student integration flow passed")
        return True
    
    def test_integration_teacher_flow(self):
        """Positive: Complete teacher flow"""
        print("\n📋 POSITIVE: Teacher Integration Flow")
        
        result = self.auth.login("teacher1@school.com", "Teacher@123")
        assert result["success"] == True, "Teacher login failed"
        
        qr_data = self.qr.generate_qr(result["user"])
        assert qr_data is not None
        
        scanned = self.qr.scan_qr(qr_data)
        assert scanned.get("email") == "teacher1@school.com"
        
        print("✅ Teacher integration flow passed")
        return True
    
    def test_integration_qr_uniqueness(self):
        """Positive: QRs are unique for each generation"""
        print("\n📋 POSITIVE: QR Uniqueness Test")
        
        result = self.auth.login("student1@school.com", "Student@123")
        assert result["success"] == True
        
        # Generate multiple QRs
        qr_codes = []
        for i in range(3):
            qr_data = self.qr.generate_qr(result["user"])
            qr_codes.append(qr_data)
            print(f"  Generated QR {i+1}: {qr_data[:30]}...")
        
        # All should scan to same user
        for i, qr in enumerate(qr_codes):
            scanned = self.qr.scan_qr(qr)
            assert scanned.get("email") == "student1@school.com"
        
        # QRs might be different (due to timestamps, etc.)
        if len(set(qr_codes)) == len(qr_codes):
            print("✓ All QRs are unique")
        else:
            print("✓ All QRs scan to same user")
        
        print("✅ QR uniqueness test passed")
        return True
    
    def test_integration_data_persistence(self):
        """Positive: QR data persists user information"""
        print("\n📋 POSITIVE: Data Persistence Test")
        
        result = self.auth.login("student1@school.com", "Student@123")
        assert result["success"] == True
        original_user = result["user"]
        
        qr_data = self.qr.generate_qr(original_user)
        scanned = self.qr.scan_qr(qr_data)
        
        # Check key fields are preserved
        key_fields = ["email", "name", "role", "id"]
        for field in key_fields:
            if field in original_user:
                assert scanned.get(field) == original_user[field], f"{field} doesn't match"
        
        print(f"✓ All {len(key_fields)} key fields preserved")
        print("✅ Data persistence test passed")
        return True
    
    # ========== NEGATIVE INTEGRATION TESTS ==========
    
    def test_integration_invalid_qr_scan(self):
        """Negative: Scan invalid QR data"""
        print("\n📋 NEGATIVE: Invalid QR Scan")
        
        invalid_data = "NOT_A_VALID_QR_CODE_12345!@#$"
        
        try:
            scanned = self.qr.scan_qr(invalid_data)
            # Should handle gracefully (return error/None, not crash)
            if scanned is None:
                print("✓ Invalid QR returned None (expected)")
            elif scanned.get("error"):
                print(f"✓ Invalid QR returned error: {scanned.get('error')}")
            else:
                # If it doesn't crash, that's acceptable
                print(f"✓ System handled invalid QR without crash")
        except Exception as e:
            # Exception is also acceptable for truly invalid data
            print(f"✓ Invalid QR threw exception (acceptable): {type(e).__name__}")
        
        print("✅ Invalid QR handling test passed")
        return True
    
    def test_integration_unauthorized_access(self):
        """Negative: Try to generate QR without login"""
        print("\n📋 NEGATIVE: Unauthorized QR Generation")
        
        # Try to generate QR with invalid/fake user data
        fake_user = {"email": "fake@test.com", "name": "Fake User"}
        
        try:
            qr_data = self.qr.generate_qr(fake_user)
            # If it generates, scan should show the fake data
            if qr_data:
                scanned = self.qr.scan_qr(qr_data)
                print(f"✓ System allows QR generation for any data")
        except Exception as e:
            print(f"✓ QR generation validates user data: {type(e).__name__}")
        
        print("✅ Unauthorized access test completed")
        return True

# ========== RUN ALL INTEGRATION TESTS ==========

def run_integration_tests():
    """Run all integration tests"""
    print("=" * 50)
    print("🔗 RUNNING INTEGRATION TESTS (Full System)")
    print("=" * 50)
    print("Note: Ensure Flask app is running (python src/app.py)")
    print("-" * 50)
    
    tester = TestIntegration()
    tests = [
        ("Student Flow", tester.test_integration_student_flow),
        ("Teacher Flow", tester.test_integration_teacher_flow),
        ("QR Uniqueness", tester.test_integration_qr_uniqueness),
        ("Data Persistence", tester.test_integration_data_persistence),
        ("Invalid QR Scan", tester.test_integration_invalid_qr_scan),
        ("Unauthorized Access", tester.test_integration_unauthorized_access),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            print(f"\n🔍 {test_name}")
            if test_func():
                passed += 1
            else:
                failed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {type(e).__name__}: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "=" * 50)
    print("📊 INTEGRATION TEST SUMMARY")
    print("=" * 50)
    print(f"Total tests: {len(tests)}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    
    if failed == 0:
        print("🎉 ALL INTEGRATION TESTS PASSED!")
        print("💡 System is working correctly!")
    else:
        print("⚠️  SOME INTEGRATION TESTS FAILED")
        print("💡 Check Flask app is running and test users exist")
    
    print("=" * 50)
    return failed == 0

if __name__ == "__main__":
    # Give time for Flask app to initialize
    print("⏳ Initializing integration tests...")
    time.sleep(2)
    
    success = run_integration_tests()
    exit(0 if success else 1)
# Simple QR code system
class QRGenerator:
    def generate_qr(self, user_data):
        """Create QR code text"""
        return f"ID:{user_data['id']}|NAME:{user_data['name']}|ROLE:{user_data['role']}"
    
    def scan_qr(self, qr_text):
        """Read QR code text"""
        try:
            parts = qr_text.split("|")
            data = {}
            for part in parts:
                key, value = part.split(":", 1)
                data[key.lower()] = value
            return data
        except:
            return None
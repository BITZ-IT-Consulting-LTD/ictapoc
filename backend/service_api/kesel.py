import json
from .registries import get_registry

class KeSEL:
    """
    Kenya Secure Exchange Layer (Huduma Bridge).
    Handles secure, decentralized data exchange between the Orchestration Layer and Authoritative Registries.
    """

    @staticmethod
    def exchange(target_registry_name, payload, security_context=None):
        """
        Simulates the secure P2P exchange described in the architecture.
        
        Args:
            target_registry_name (str): The mock registry to query (e.g., 'IPRS', 'BRS').
            payload (dict): The query parameters.
            security_context (dict): Mock certificates/signatures.
        
        Returns:
            dict: The response from the authoritative registry.
        """
        
        # 1. Trust & Security Layer Check (Simulated)
        # In a real system, this would verify the NPKI Digital Certificate of the sender.
        print(f"[KeSEL] Verifying Security Header from Agency Security Server...")
        if not security_context or not security_context.get('signed'):
            print(f"[KeSEL] WARNING: Unsigned request intercepted.")
            # For POC, we might allow it but log it. Real system would block.
        
        # 2. Service Directory Lookup
        from .services import RegistryService
        
        # 3. Encrypted Data Output (Simulated)
        print(f"[KeSEL] Routing encrypted packet to {target_registry_name} via DB-driven Registry Adapter...")
        
        # 4. Query Registry
        identifier = payload.get('identifier') or payload.get('id_number') or payload.get('pin') or payload.get('upi') or payload.get('birth_certificate_number') or payload.get('notification_number') or payload.get('mother_id') or payload.get('father_id')
        response = RegistryService.query(target_registry_name, identifier)
        
        # 5. Return Response (Signed by Registry's Security Server)
        print(f"[KeSEL] Received response from {target_registry_name}. Verifying signature...")
        return response

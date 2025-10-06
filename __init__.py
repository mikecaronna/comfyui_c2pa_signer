"""
C2PA Signer Custom Node for ComfyUI

This custom node enables C2PA (Coalition for Content Provenance and Authenticity)
signing of images using the c2patool CLI.
"""

from .c2pa_node import NODE_CLASS_MAPPINGS as SIGNER_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS as SIGNER_DISPLAY_MAPPINGS
from .c2pa_verifier import C2PAVerifier

# Combine mappings from all modules
NODE_CLASS_MAPPINGS = {
    **SIGNER_MAPPINGS,
    "C2PAVerifier": C2PAVerifier
}

NODE_DISPLAY_NAME_MAPPINGS = {
    **SIGNER_DISPLAY_MAPPINGS,
    "C2PAVerifier": "C2PA Verifier"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

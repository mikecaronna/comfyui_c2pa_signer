"""
C2PA Signer Custom Node for ComfyUI

This custom node enables C2PA (Coalition for Content Provenance and Authenticity)
signing of images using the c2patool CLI.
"""

from .c2pa_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

import os
import json
import tempfile
import subprocess
from PIL import Image
import numpy as np


class C2PAVerifier:
    """
    A ComfyUI custom node for verifying and reading C2PA manifests from signed images.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("manifest_json", "summary", "image")
    FUNCTION = "verify_image"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def verify_image(self, image):
        """
        Verify and read C2PA manifest from a signed image.

        Args:
            image: ComfyUI image tensor (batch, height, width, channels)

        Returns:
            Tuple of (full_manifest_json, human_readable_summary, passthrough_image)
        """

        # Convert ComfyUI tensor to PIL Image
        image_np = image[0].cpu().numpy()
        image_np = (image_np * 255).astype(np.uint8)
        pil_image = Image.fromarray(image_np)

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save image to temp file
            temp_path = os.path.join(temp_dir, "verify.png")
            pil_image.save(temp_path, format="PNG")

            # Call c2patool to read manifest
            try:
                cmd = ["c2patool", temp_path]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True
                )

                # Parse the JSON output
                try:
                    manifest_data = json.loads(result.stdout)
                except json.JSONDecodeError:
                    # No C2PA manifest found
                    summary = "❌ No C2PA manifest found in this image"
                    manifest_json = "{}"
                    print(summary)
                    return (manifest_json, summary, image)

                # Extract key information for summary
                summary_parts = []

                # Check if manifest exists
                if "active_manifest" in manifest_data:
                    summary_parts.append("✅ C2PA Manifest Found")

                    # Validation status
                    if "validation_state" in manifest_data:
                        validation = manifest_data["validation_state"]
                        if validation == "Valid":
                            summary_parts.append(f"🔒 Signature: Valid")
                        else:
                            summary_parts.append(f"⚠️ Signature: {validation}")

                    # Signature info
                    if "signature_info" in manifest_data:
                        sig_info = manifest_data["signature_info"]
                        if "issuer" in sig_info:
                            summary_parts.append(f"👤 Issuer: {sig_info['issuer']}")
                        if "alg" in sig_info:
                            summary_parts.append(f"🔐 Algorithm: {sig_info['alg']}")

                    # Count assertions
                    manifests = manifest_data.get("manifests", {})
                    if manifests:
                        first_manifest = next(iter(manifests.values()))
                        assertions = first_manifest.get("assertions", [])
                        if assertions:
                            summary_parts.append(f"📋 Assertions: {len(assertions)}")
                            # List assertion labels
                            labels = [a.get("label", "unknown") for a in assertions[:5]]
                            for label in labels:
                                summary_parts.append(f"  • {label}")
                            if len(assertions) > 5:
                                summary_parts.append(f"  • ... and {len(assertions) - 5} more")

                else:
                    summary_parts.append("❌ No C2PA manifest found")

                summary = "\n".join(summary_parts)
                manifest_json = json.dumps(manifest_data, indent=2)

                print(f"C2PA Verification:\n{summary}")

                return (manifest_json, summary, image)

            except subprocess.CalledProcessError as e:
                # Error running c2patool
                error_msg = f"❌ Error verifying C2PA manifest:\n{e.stderr}"
                print(error_msg)
                return ("{}", error_msg, image)

            except FileNotFoundError:
                error_msg = (
                    "❌ c2patool not found. Please install c2patool and ensure it's in your PATH.\n"
                    "Download from: https://github.com/contentauth/c2pa-rs/releases"
                )
                print(error_msg)
                return ("{}", error_msg, image)

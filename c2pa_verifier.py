import os
import json
import tempfile
import subprocess
from PIL import Image
import numpy as np


class C2PAVerifier:
    """
    A ComfyUI custom node for verifying and reading C2PA manifests from signed images.

    IMPORTANT: To verify signed images, provide the file path to the signed file.
    C2PA manifests are stored in file metadata, not in image pixels/tensors.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
            },
            "optional": {
                "file_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
            }
        }

    RETURN_TYPES = ("STRING", "STRING", "IMAGE")
    RETURN_NAMES = ("manifest_json", "summary", "image")
    FUNCTION = "verify_image"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def verify_image(self, image, file_path=""):
        """
        Verify and read C2PA manifest from a signed image.

        Args:
            image: ComfyUI image tensor (batch, height, width, channels)
            file_path: Optional path to a signed image file on disk

        Returns:
            Tuple of (full_manifest_json, human_readable_summary, passthrough_image)
        """

        # If file_path is provided, verify that file directly
        if file_path and file_path.strip():
            verify_path = file_path.strip()

            # Check if file exists
            if not os.path.exists(verify_path):
                error_msg = (
                    f"❌ File not found: {verify_path}\n\n"
                    "Please check:\n"
                    "• The file path is correct\n"
                    "• The file exists on your computer\n"
                    "• You're using forward slashes (/), not backslashes (\\)"
                )
                print(error_msg)
                return ("{}", error_msg, image)

            print(f"🔍 Verifying signed file: {verify_path}")

        else:
            # No file path provided - use image tensor
            # This won't work for signed images because manifests are in file metadata, not pixels
            info_msg = (
                "ℹ️  IMPORTANT: To verify a signed image, you need to provide a file path.\n\n"
                "Why? C2PA signatures are stored in the image FILE's metadata, not in the pixels.\n"
                "When images flow through ComfyUI, only the pixels are passed along.\n\n"
                "How to use this node:\n"
                "1. First, sign an image (it saves to the output folder)\n"
                "2. Copy the full path to that signed file\n"
                "3. Paste the path into the 'file_path' field of this node\n\n"
                "Example path: C:/Users/YourName/Documents/ComfyUI/output/C2PA_signed_20251006_094628.png\n\n"
                "⚠️  Checking the image tensor anyway, but it likely has no signature..."
            )
            print(info_msg)

            # Convert ComfyUI tensor to PIL Image and try to verify
            # (This will almost always fail for signed images, but we'll try for educational purposes)
            image_np = image[0].cpu().numpy()
            image_np = (image_np * 255).astype(np.uint8)
            pil_image = Image.fromarray(image_np)

            # Create temporary directory for processing
            temp_dir_obj = tempfile.TemporaryDirectory()
            temp_dir = temp_dir_obj.name
            verify_path = os.path.join(temp_dir, "verify.png")
            pil_image.save(verify_path, format="PNG")

        # Call c2patool to read manifest
        try:
            cmd = ["c2patool", verify_path]

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
                if file_path and file_path.strip():
                    summary = (
                        "❌ No C2PA manifest found in this file\n\n"
                        "This means the file is not signed, or the signature was removed.\n"
                        "Make sure you're checking a file that was created by the C2PA Image Signer node."
                    )
                else:
                    summary = (
                        "❌ No C2PA manifest found\n\n"
                        "This is expected! Image tensors don't include file metadata.\n\n"
                        "📝 To verify a signed image:\n"
                        "1. Sign an image (check the output folder for the saved file)\n"
                        "2. Enter the full path to that file in the 'file_path' field above\n\n"
                        "Example: C:/Users/YourName/Documents/ComfyUI/output/C2PA_signed_20251006_094628.png"
                    )
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

            # Add helpful note if they didn't use file_path
            if not (file_path and file_path.strip()):
                summary += "\n\n💡 TIP: For best results, use the 'file_path' field to verify signed files directly!"

            manifest_json = json.dumps(manifest_data, indent=2)

            print(f"C2PA Verification:\n{summary}")

            return (manifest_json, summary, image)

        except subprocess.CalledProcessError as e:
            # Error running c2patool
            # Check if it's the "no claim found" error
            if "No claim found" in e.stderr or "No claim found" in e.stdout:
                # No C2PA manifest found - provide helpful guidance
                if file_path and file_path.strip():
                    summary = (
                        "❌ No C2PA manifest found in this file\n\n"
                        "This means the file is not signed, or the signature was removed.\n"
                        "Make sure you're checking a file that was created by the C2PA Image Signer node."
                    )
                else:
                    summary = (
                        "❌ No C2PA manifest found\n\n"
                        "This is expected! Image tensors don't include file metadata.\n\n"
                        "📝 To verify a signed image:\n"
                        "1. Sign an image (check the output folder for the saved file)\n"
                        "2. Enter the full path to that file in the 'file_path' field above\n\n"
                        "Example: C:/Users/YourName/Documents/ComfyUI/output/C2PA_signed_20251006_094628.png"
                    )
                print(summary)
                return ("{}", summary, image)
            else:
                # Some other error from c2patool
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

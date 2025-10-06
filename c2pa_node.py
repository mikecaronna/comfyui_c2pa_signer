import os
import json
import tempfile
import subprocess
import shutil
import folder_paths
from PIL import Image
import numpy as np
import torch
from datetime import datetime

class C2PASigner:
    """
    A ComfyUI custom node for signing images with C2PA manifests using c2patool CLI.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "image": ("IMAGE",),
                "private_key_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "cert_path": ("STRING", {
                    "default": "",
                    "multiline": False,
                }),
                "filename_prefix": ("STRING", {
                    "default": "C2PA_signed",
                    "multiline": False,
                }),
            },
            "optional": {
                "manifest_json": ("STRING", {
                    "default": "{}",
                    "multiline": True,
                }),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("signed_image",)
    FUNCTION = "sign_image"
    CATEGORY = "image/postprocessing"
    OUTPUT_NODE = True

    def sign_image(self, image, private_key_path, cert_path, filename_prefix="C2PA_signed", manifest_json="{}"):
        """
        Sign an image with C2PA manifest using c2patool.

        Args:
            image: ComfyUI image tensor (batch, height, width, channels)
            private_key_path: Path to the private key file
            cert_path: Path to the certificate file
            manifest_json: Optional JSON string for custom attestations

        Returns:
            Signed image as ComfyUI tensor
        """

        # Convert ComfyUI tensor to PIL Image
        # ComfyUI format: (batch, height, width, channels) with values in [0, 1]
        image_np = image[0].cpu().numpy()
        image_np = (image_np * 255).astype(np.uint8)
        pil_image = Image.fromarray(image_np)

        # Create temporary directory for processing
        with tempfile.TemporaryDirectory() as temp_dir:
            # Save input image
            input_path = os.path.join(temp_dir, "input.png")
            pil_image.save(input_path, format="PNG")

            # Prepare output path
            output_path = os.path.join(temp_dir, "output.png")

            # Parse and prepare manifest JSON
            try:
                manifest_data = json.loads(manifest_json) if manifest_json else {}
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid manifest JSON: {e}")

            # Add signing credentials to manifest
            if private_key_path and cert_path:
                manifest_data["private_key"] = private_key_path
                manifest_data["sign_cert"] = cert_path
            else:
                raise ValueError("Both private_key_path and cert_path must be provided")

            # Set default signing algorithm if not specified
            if "alg" not in manifest_data:
                manifest_data["alg"] = "es256"

            # Write manifest to temp file
            manifest_path = os.path.join(temp_dir, "manifest.json")
            with open(manifest_path, 'w') as f:
                json.dump(manifest_data, f, indent=2)

            # Call c2patool
            try:
                # Set environment variable to allow self-signed certificates
                env = os.environ.copy()
                env["C2PATOOL_ALLOWED_LIST"] = cert_path

                cmd = [
                    "c2patool",
                    input_path,
                    "-m", manifest_path,
                    "-o", output_path,
                    "-f"  # Force overwrite output file
                ]

                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    check=True,
                    env=env  # Pass modified environment with allowed cert list
                )

                print(f"C2PA signing successful: {result.stdout}")

            except subprocess.CalledProcessError as e:
                raise RuntimeError(f"c2patool failed: {e.stderr}")
            except FileNotFoundError:
                raise RuntimeError(
                    "c2patool not found. Please install c2patool and ensure it's in your PATH. "
                    "Download from: https://github.com/contentauth/c2pa-rs/releases"
                )

            # Load signed image
            signed_pil = Image.open(output_path)

            # Save the signed image to ComfyUI output directory (preserves C2PA manifest)
            output_dir = folder_paths.get_output_directory()
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            counter = 0
            while True:
                if counter == 0:
                    filename = f"{filename_prefix}_{timestamp}.png"
                else:
                    filename = f"{filename_prefix}_{timestamp}_{counter:03d}.png"
                final_path = os.path.join(output_dir, filename)
                if not os.path.exists(final_path):
                    break
                counter += 1

            # Use copy2 to preserve all metadata including C2PA manifest
            shutil.copy2(output_path, final_path)
            print(f"C2PA signed image saved to: {final_path}")

            # Convert back to ComfyUI tensor format
            signed_np = np.array(signed_pil).astype(np.float32) / 255.0
            signed_tensor = torch.from_numpy(signed_np).unsqueeze(0)

            return (signed_tensor,)


# Node registration
NODE_CLASS_MAPPINGS = {
    "C2PASigner": C2PASigner
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "C2PASigner": "C2PA Image Signer"
}

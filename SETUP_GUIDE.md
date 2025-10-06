# C2PA Image Signer - Complete Setup Guide for Beginners

This guide will walk you through everything you need to know to use the C2PA Image Signer custom node in ComfyUI.

## Table of Contents

1. [What is C2PA?](#what-is-c2pa)
2. [What You Already Have](#what-you-already-have)
3. [Installing c2patool](#installing-c2patool)
4. [Using the Node in ComfyUI](#using-the-node-in-comfyui)
5. [Troubleshooting](#troubleshooting)

---

## What is C2PA?

**C2PA (Coalition for Content Provenance and Authenticity)** is a standard for adding cryptographic signatures to digital media (images, videos, audio) to prove:
- **Who created it** (authenticity)
- **When it was created** (provenance)
- **What tools were used** (metadata)
- **If it has been modified** (integrity)

Think of it like a digital "certificate of authenticity" embedded in your image file.

### How it Works

1. **You sign an image** with your private key
2. **A manifest is embedded** in the image containing:
   - Your certificate (public key)
   - Metadata about the image
   - Custom information you want to add
3. **Anyone can verify** the signature using your public certificate

---

## What You Already Have

✅ **Good news!** I've already set up the following for you:

### 1. Custom ComfyUI Node
- **Location:** `<ComfyUI_path>/custom_nodes/c2pa_signer/`
- **Files:**
  - `c2pa_node.py` - The main node code
  - `__init__.py` - Registration file

### 2. Test Keys and Certificate
I've generated a **official test certificates from c2patool** for testing:

- **Private Key:** `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key`
- **Certificate:** `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem`

**Important Notes:**
- ✅ **Perfect for testing** and learning
- ❌ **NOT for production** - Self-signed certificates aren't trusted by validators
- 🔐 **Keep es256_private.key secret** - Anyone with this file can sign as "you"

### What the Keys Mean

- **Private Key** (`es256_private.key`):
  - Your secret signing key
  - Never share this with anyone
  - Used to create the digital signature

- **Certificate** (`es256_certs.pem`):
  - Your public certificate
  - Contains your public key
  - Embedded in signed images
  - Others use this to verify your signature

---

## Installing c2patool

The C2PA node uses a command-line tool called **c2patool** to actually sign the images. You need to install it:

### Step 1: Download c2patool

1. Go to: **https://github.com/contentauth/c2pa-rs/releases**

2. Find the **latest release** (top of the page)

3. Under "Assets", download the **Windows version**:
   - Look for: `c2patool-windows-x86_64.zip` or similar

4. **Extract the ZIP file** to a folder, for example:
   ```
   C:\Tools\c2patool\
   ```

### Step 2: Add to Windows PATH

You need to make c2patool accessible from anywhere on your system.

**Option A: Using Windows Settings (Recommended)**

1. Press `Windows + S` and search for **"Environment Variables"**
2. Click **"Edit the system environment variables"**
3. Click **"Environment Variables..."** button
4. Under **"User variables"**, find and select **"Path"**
5. Click **"Edit..."**
6. Click **"New"**
7. Add the path where you extracted c2patool, for example:
   ```
   C:\Tools\c2patool
   ```
8. Click **"OK"** on all windows
9. **Close and reopen** any command prompts or terminals

**Option B: Quick Test (Temporary)**

If you just want to test without modifying PATH:
1. Copy `c2patool.exe` to the same folder as your Python executable
2. Or reference the full path in the node (not recommended)

### Step 3: Verify Installation

Open a **new** Command Prompt or PowerShell and run:

```bash
c2patool --version
```

You should see something like:
```
c2patool 0.9.x
```

If you get an error, c2patool is not in your PATH. Go back to Step 2.

---

## Using the Node in ComfyUI

### Step 1: Restart ComfyUI

After installing the custom node, you need to restart ComfyUI:

1. Close ComfyUI completely
2. Start it again
3. The C2PA Image Signer node will be loaded

### Step 2: Find the Node

In ComfyUI:

1. **Right-click** on the canvas
2. Navigate to: **image → postprocessing**
3. Select: **C2PA Image Signer**

### Step 3: Connect the Inputs

The node has these inputs:

#### Required Inputs:

1. **image** (IMAGE type)
   - Connect from any image source (Load Image, Save Image, etc.)

2. **private_key_path** (String)
   - Enter: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key`
   - ⚠️ Use forward slashes `/` not backslashes `\`

3. **cert_path** (String)
   - Enter: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem`
   - ⚠️ Use forward slashes `/` not backslashes `\`

#### Optional Input:

4. **manifest_json** (String)
   - Leave empty `{}` for basic signing
   - Or add custom metadata (see examples below)

### Step 4: Basic Workflow Example

Here's a simple workflow:

```
[Load Image] → [C2PA Image Signer]
```

**Configuration:**
- **Load Image**: Select any image
- **C2PA Image Signer**:
  - private_key_path: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key`
  - cert_path: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem`
  - manifest_json: `{}` (or leave empty)
- **Save Image**: Save the signed image

### Step 5: Run the Workflow

1. Click **"Queue Prompt"**
2. The node will:
   - Take your input image
   - Sign it with your private key
   - Embed the C2PA manifest
   - Output the signed image

---

## Adding Custom Attestations (Advanced)

You can add custom metadata to your signed images using the **manifest_json** field.

### Example 1: Add Author Information

```json
{
  "assertions": [
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "author": [
          {
            "@type": "Person",
            "name": "Mike C"
          }
        ],
        "dateCreated": "2025-10-06"
      }
    }
  ]
}
```

### Example 2: Add Custom Data

```json
{
  "assertions": [
    {
      "label": "org.mycompany.custom",
      "data": {
        "project": "AI Generated Art",
        "model": "Stable Diffusion",
        "prompt": "A beautiful sunset over mountains",
        "version": "1.0"
      }
    }
  ]
}
```

### Example 3: Multiple Attestations

```json
{
  "assertions": [
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "author": [{"@type": "Person", "name": "Mike C"}]
      }
    },
    {
      "label": "com.myapp.workflow",
      "data": {
        "workflow_name": "Portrait Enhancement",
        "steps": ["denoise", "upscale", "color_correction"],
        "quality_preset": "high"
      }
    }
  ]
}
```

**How to use:**
1. Copy one of the examples above
2. Paste into the **manifest_json** field
3. Modify the values to match your needs
4. Make sure the JSON is valid (use a JSON validator if unsure)

---

## Verifying Signed Images

After signing an image, you can verify it contains a C2PA manifest:

### Using c2patool (Command Line)

```bash
c2patool path/to/signed_image.png
```

This will display the manifest contents, including:
- Signature information
- Assertions/metadata you added
- Validation status

### Example Output:

```
Manifest found in: signed_image.png
Signature: Valid
Algorithm: es256
Certificate: CN=C2PA Test Certificate
Assertions:
  - stds.schema-org.CreativeWork
    Author: Mike C
    Date: 2025-10-06
```

---

## Troubleshooting

### Error: "c2patool not found"

**Problem:** c2patool is not installed or not in PATH

**Solution:**
1. Verify c2patool is installed: `c2patool --version`
2. If not found, follow [Installing c2patool](#installing-c2patool)
3. Make sure to restart ComfyUI after adding to PATH

### Error: "Invalid manifest JSON"

**Problem:** The JSON in manifest_json field is malformed

**Solution:**
1. Check for missing commas, quotes, or brackets
2. Use a JSON validator: https://jsonlint.com/
3. Start with an empty object `{}` and add fields gradually

### Error: "Failed to read private key" or "Failed to read certificate"

**Problem:** File paths are incorrect

**Solution:**
1. Make sure paths use **forward slashes** `/`:
   - ✅ `<ComfyUI_path>/custom_nodes/...`
   - ❌ `C:\path\with\backslashes\...`
2. Verify files exist:
   ```bash
   ls <ComfyUI_path>/custom_nodes/c2pa_signer/keys/
   ```
3. Make sure you didn't accidentally add extra spaces

### Error: "Signature validation failed"

**Problem:** Using official test certificates from c2patool (expected for testing)

**Solution:**
- This is **normal** with official test certificates from c2patools
- The signature is still valid, just not "trusted"
- For production, get a certificate from a trusted CA

### Node Doesn't Appear in ComfyUI

**Problem:** Custom node not loaded

**Solution:**
1. Verify node files exist:
   ```
   <ComfyUI_path>/custom_nodes/c2pa_signer/
   ```
2. Check for `__init__.py` and `c2pa_node.py`
3. Restart ComfyUI completely
4. Check ComfyUI console for error messages

### The Image Doesn't Change

**Problem:** Wondering if signing worked

**Solution:**
- This is **normal** - the image looks the same visually
- The C2PA manifest is embedded in the file metadata
- Verify by:
  1. File size is slightly larger
  2. Running: `c2patool path/to/signed_image.png`

---

## Next Steps

### For Learning:
1. ✅ Start with basic signing (empty manifest_json)
2. ✅ Verify signed images with c2patool
3. ✅ Experiment with adding simple attestations
4. ✅ Try different image formats (PNG, JPEG)

### For Production:
1. 🔐 Get a proper certificate from a Certificate Authority
2. 📝 Define your attestation schema
3. 🔒 Store private keys securely (not in the custom_nodes folder)
4. ✅ Implement key rotation strategy

---

## Helpful Resources

- **C2PA Specification:** https://c2pa.org/specifications/
- **c2patool GitHub:** https://github.com/contentauth/c2pa-rs
- **Manifest Documentation:** https://github.com/contentauth/c2pa-rs/blob/main/cli/docs/manifest.md
- **JSON Validator:** https://jsonlint.com/
- **Schema.org Vocabulary:** https://schema.org/CreativeWork

---

## Security Notes

⚠️ **Important Security Reminders:**

1. **Private Key Security**
   - Never commit es256_private.key to version control
   - Never share it publicly
   - Store securely (use a password manager for production)

2. **Self-Signed Certificates**
   - Fine for testing and learning
   - Not trusted by validators
   - Won't verify as "authentic" in C2PA validators

3. **Production Use**
   - Get certificates from a trusted CA (Certificate Authority)
   - Use hardware security modules (HSM) for key storage
   - Implement proper key management

---

## Questions?

If you run into issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Verify c2patool works: `c2patool --version`
3. Check the ComfyUI console for error messages
4. Review the paths (use forward slashes)

Happy signing! 🔐

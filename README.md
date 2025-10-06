# C2PA Image Signer - ComfyUI Custom Node

## What is This?

This is a tool that lets you **digitally sign your images** to prove you created them. Think of it like putting an invisible, tamper-proof seal on your artwork that says "I made this."

When you sign an image with C2PA:
- ✅ People can verify **you** created it (authenticity)
- ✅ People can see **when** it was created (timestamp)
- ✅ The signature breaks if someone **modifies** the image (integrity)
- ✅ You can add information about **how** it was made (metadata)

This is especially useful for AI-generated art, photography, and any digital content where proving authorship matters.

---

## 🚀 Quick Start

**New to all this?** Don't worry! Start with these guides in order:

1. **📖 [QUICK_START.md](QUICK_START.md)** - Get it working in 5 minutes (step-by-step)
2. **📚 [SETUP_GUIDE.md](SETUP_GUIDE.md)** - Understand what you're doing (beginner-friendly)
3. **💡 [EXAMPLES.md](EXAMPLES.md)** - See real-world examples

---

## What This Tool Does

### Simple Version
You put an image into this node in ComfyUI, and it comes out with an invisible digital signature embedded in the file. Anyone can check this signature to verify you created it.

### The Features
- ✅ Signs images with **C2PA certificates** (industry standard for digital content)
- ✅ Works directly in your **ComfyUI** workflows
- ✅ Add custom information (who made it, what tools were used, etc.)
- ✅ Includes **test certificates** so you can start immediately
- ✅ Automatically saves signed images (no extra steps needed)

---

## What's Included

When you downloaded this custom node, you got everything you need to start testing:

### Test Certificates (Ready to Use!)

Think of certificates like a digital ID card. The node comes with **official test certificates** from the c2patool project:

- **📄 Private Key:** `keys/es256_private.key`
  - This is like your password - keep it secret!
  - Used to create the signature
  - Never share this file

- **📄 Certificate:** `keys/es256_certs.pem`
  - This is like your public ID - it's safe to share
  - Contains your "public key" that others use to verify your signature
  - Gets embedded in signed images

**⚠️ Important:** These test certificates are **perfect for learning and testing**, but if you're releasing images publicly or professionally, you'll want to get a "real" certificate from a trusted organization (more on that later).

### Why Two Files?

Think of it like this:
- **Private key** = Your pen (only you can sign with it)
- **Certificate** = Your signature sample (others compare to verify it's really yours)

Someone can have your signature sample (certificate) and verify your autograph, but they can't forge your signature without your actual pen (private key).

---

## What You Need First

### Installing c2patool

This is a helper program that does the actual signing. Think of it like installing a printer driver before you can print.

**For Windows (Easiest Way):**

1. **Download the tool:**
   - Go to: https://github.com/contentauth/c2pa-rs/releases
   - Find the latest version
   - Download the file that says "windows" in the name (like `c2patool-v0.23.4-x86_64-pc-windows-msvc.zip`)

2. **Extract it:**
   - Right-click the downloaded ZIP → Extract All
   - Put it somewhere you'll remember (like `C:\Tools\c2patool`)

3. **Make it accessible:**
   - This part lets Windows find the tool from anywhere
   - See the [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions
   - Basically: Add the folder to your "PATH" (Windows settings)

4. **Test it worked:**
   - Open Command Prompt (search for "cmd" in Windows)
   - Type: `c2patool --version`
   - If you see a version number, you're good! ✅

**📖 Need more help?** Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step instructions with screenshots.

---

## How to Use It

This custom node package includes **two nodes**:
1. **C2PA Image Signer** - Signs images with C2PA manifests
2. **C2PA Verifier** - Reads and displays C2PA manifests from signed images

### Signing Images: The Simple Workflow

In ComfyUI, your workflow looks like this:

```
[Load Image] → [C2PA Image Signer]
```

That's it! The C2PA Image Signer automatically saves the signed image for you.

**Important:** Don't add a "Save Image" node after the C2PA Signer. If you do, the signature will be stripped out because ComfyUI re-processes the image. The signer already saves the file for you.

### What to Put in the Node

The node needs these settings:

1. **image** (connect to it)
   - This is your image from Load Image or any other node

2. **private_key_path** (type it in)
   - The full path to your private key
   - Example: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key`
   - ⚠️ Use forward slashes `/` not backslashes `\`

3. **cert_path** (type it in)
   - The full path to your certificate
   - Example: `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem`
   - ⚠️ Use forward slashes `/` not backslashes `\`

4. **filename_prefix** (optional)
   - What to name your signed images
   - Default: "C2PA_signed"
   - Result: `C2PA_signed_20251006_094628.png`

5. **manifest_json** (optional, advanced)
   - Extra information to embed in the signature
   - Start with just `{}` (empty)
   - See examples below for what you can add

### Where Do Signed Images Go?

After you run the workflow, check:
```
<ComfyUI_path>/output/
```

Look for files named like: `C2PA_signed_20251006_094628.png`

The signature is **invisible** - the image looks the same, but the file is slightly larger because it contains the signature data.

---

### Verifying Signed Images: Using the C2PA Verifier

The **C2PA Verifier** node lets you read and display C2PA manifests from signed images directly in ComfyUI.

**Important:** C2PA signatures are stored in the **file's metadata**, not in the image pixels. When images flow through ComfyUI as tensors, they lose this metadata. Therefore, to verify a signed image, you need to provide the **file path** to the actual signed file on disk.

#### How to Use the C2PA Verifier

Your verification workflow looks like this:

```
[Load Image] → [C2PA Verifier] → [Preview Any or Show Text]
```

**The Node Inputs:**

1. **image** (required, connect from Load Image)
   - This is for ComfyUI workflow compatibility
   - The verifier needs a tensor input, but won't use it for verification

2. **file_path** (optional, but required for actual verification)
   - The **full path** to a signed image file on disk
   - Example: `C:/Users/YourName/Documents/ComfyUI/output/C2PA_signed_20251006_094628.png`
   - ⚠️ Use forward slashes `/` not backslashes `\`

**The Node Outputs:**

- **manifest_json** - Full C2PA manifest as JSON (technical details)
- **summary** - Human-readable summary showing:
  - ✅ Whether a manifest was found
  - 🔒 Signature validation status
  - 👤 Issuer/creator information
  - 📋 List of assertions (metadata)
- **image** - Passthrough of input image for workflow chaining

#### Example Workflow: Sign and Verify

1. **Sign an image:**
   ```
   [Load Image] → [C2PA Image Signer]
   ```
   Run this workflow and note the output path shown in the console

2. **Verify the signed image:**
   ```
   [Load Image] → [C2PA Verifier] → [Preview Any]
   ```
   - In the C2PA Verifier node, paste the full file path to your signed image
   - Connect the output to Preview Any or Show Text to see the verification results
   - You should see "✅ C2PA Manifest Found" with signature details

#### What You'll See

**If verification succeeds:**
```
✅ C2PA Manifest Found
🔒 Signature: Valid
👤 Issuer: C2PA Test Signing Cert
🔐 Algorithm: es256
📋 Assertions: 1
  • stds.schema-org.CreativeWork
```

**If you forget to enter the file_path:**
```
❌ No C2PA manifest found

This is expected! Image tensors don't include file metadata.

📝 To verify a signed image:
1. Sign an image (check the output folder for the saved file)
2. Enter the full path to that file in the 'file_path' field above

Example: C:/Users/YourName/Documents/ComfyUI/output/C2PA_signed_20251006_094628.png
```

**Why can't the verifier read from the tensor?**

C2PA signatures are stored in the image **file's metadata**, not in the pixel data. When an image flows through ComfyUI, only the pixel values (the tensor) are passed along - the file metadata is left behind. This is why you need to provide the file path to the actual signed file on disk.

---

## Adding Information to Your Signatures (Optional)

You can embed extra information in your signatures using the `manifest_json` field. This is optional but powerful!

### Example 1: Add Your Name

Paste this into the **manifest_json** field:

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
            "name": "Your Name Here"
          }
        ]
      }
    }
  ]
}
```

This embeds your name as the creator. Anyone who verifies the signature will see this.

### Example 2: Add AI Generation Info

If you're making AI art, add this info:

```json
{
  "assertions": [
    {
      "label": "com.example.ai-art",
      "data": {
        "model": "Stable Diffusion",
        "prompt": "A beautiful sunset over mountains",
        "workflow": "ComfyUI",
        "created_date": "2025-10-06"
      }
    }
  ]
}
```

### What Are "Assertions"?

Assertions are just pieces of information you're "asserting" (claiming) about the image. Think of them like adding tags or notes that get sealed with your signature.

Common things to include:
- Who created it (your name)
- When it was created
- What tools/software were used
- If it's AI-generated or photographed
- Copyright information
- Licensing details

---

## Checking If It Worked

After signing an image, you can verify it contains a signature in two ways:

### Option 1: Using the C2PA Verifier Node (Easiest!)

Use the **C2PA Verifier** node in ComfyUI:
1. Add the C2PA Verifier node to your workflow
2. Paste the full path to your signed image in the `file_path` field
3. Connect to Preview Any or Show Text
4. Run the workflow
5. You should see "✅ C2PA Manifest Found" with signature details

See the [Verifying Signed Images](#verifying-signed-images-using-the-c2pa-verifier) section above for detailed instructions.

### Option 2: Using Command Line

1. Open Command Prompt
2. Type:
   ```bash
   c2patool "<ComfyUI_path>/output/C2PA_signed_20251006_094628.png"
   ```
   (Use your actual filename)

3. You should see a bunch of information about the signature, including:
   - ✅ `"validation_state": "Valid"` (the signature is good!)
   - Your certificate information
   - Any assertions you added

If you see `"validation_state": "Valid"`, congratulations! Your image is signed and verified! 🎉

---

## Common Questions & Problems

### "c2patool not found"

**What it means:** Windows can't find the c2patool program.

**How to fix:**
1. Make sure you extracted c2patool to a folder
2. Make sure you added that folder to your Windows PATH
3. Restart ComfyUI after changing PATH
4. Test by typing `c2patool --version` in Command Prompt

### "Invalid manifest JSON"

**What it means:** There's a typo in your manifest_json field.

**How to fix:**
- Check for missing commas or brackets
- Use a JSON checker: https://jsonlint.com/
- Start simple with just `{}` and add things one at a time

### "Failed to read private key" or "Failed to read certificate"

**What it means:** The file paths are wrong.

**How to fix:**
- Make sure you use **forward slashes**: `C:/Users/...`
- Don't use backslashes: `C:\Users\...` (this won't work)
- Copy-paste the full path to avoid typos
- Make sure the files actually exist in that location

### Why can't I use SaveImage after the C2PA Signer?

**The Problem:** When you run an image through SaveImage, ComfyUI re-processes it and strips out the C2PA signature.

**Why:** SaveImage converts the image back to pixels and re-saves it, which loses all the extra signature data.

**The Solution:** The C2PA Signer already saves the file for you! You don't need SaveImage.

### The image looks the same - did it work?

**Yes!** The signature is **invisible**. The image looks identical to humans.

The signature is stored in the file's metadata (invisible data), not in the pixels you see. The file will be slightly larger (a few KB) because of this extra data.

To verify it worked, use: `c2patool your-image.png`

---

## What "Test Certificates" Mean

The certificates included with this node are **official test certificates** from the c2patool project. Here's what that means:

**For Testing/Learning:**
- ✅ Perfect for experimenting
- ✅ Works completely
- ✅ Signatures verify as valid
- ✅ Free to use

**Limitations:**
- ⚠️ Everyone has these same certificates
- ⚠️ Not unique to you
- ⚠️ Won't prove YOU specifically made something
- ⚠️ Not accepted for professional/commercial use

Think of it like using a practice signature vs. your real signature on legal documents.

### When Do I Need "Real" Certificates?

You need real certificates if:
- You're releasing images publicly
- You want to prove YOU made them (not just "someone")
- You're doing commercial or professional work
- You need legal authenticity

**How to get them:** You'd get a certificate from a "Certificate Authority" (an organization that verifies identities). This is beyond the scope of testing, but when you're ready, look into:
- Professional certificate providers
- Industry-specific certificate authorities
- Enterprise solutions from C2PA members

For now, the test certificates are perfect for learning!

---

## Learn More

Want to understand C2PA better? Check out:

- **C2PA Official Site:** https://c2pa.org/
- **c2patool Documentation:** https://github.com/contentauth/c2pa-rs/tree/main/cli
- **Technical Specification:** https://c2pa.org/specifications/ (if you're curious!)

---

## Need Help?

1. Read [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed explanations
2. Check [EXAMPLES.md](EXAMPLES.md) for workflow examples
3. Review the troubleshooting section above

---

## License

This custom node is free to use. The c2patool program is created by the Content Authenticity Initiative and is licensed under Apache License 2.0 / MIT.

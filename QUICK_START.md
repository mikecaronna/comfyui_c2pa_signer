# C2PA Image Signer - Quick Start Guide

## Welcome! 👋

This guide will get you signing images in about 5 minutes. Don't worry if you're new to this - we'll walk through everything step by step.

**What you'll do:**
1. Install a helper program (c2patool)
2. Add the C2PA node to a ComfyUI workflow
3. Sign your first image!

Let's go! 🚀

---

## Before You Start

### What You Already Have ✅

Good news! Most of the work is already done:

- ✅ **ComfyUI** - You have this installed
- ✅ **C2PA Custom Node** - Already in your ComfyUI (you're reading this!)
- ✅ **Test Certificates** - Already included (in the `keys` folder)

### What You Need to Install ⏳

Just one thing: **c2patool** (a helper program that does the signing)

Think of it like this: The custom node is like a steering wheel, and c2patool is the engine. You need both to make it work.

---

## Step 1: Install c2patool

### Why do I need this?

c2patool is the actual program that adds the digital signature to your images. Our ComfyUI node is just a user-friendly interface that tells c2patool what to do.

### How to install it (Windows):

**1. Download c2patool**

- Go to: **https://github.com/contentauth/c2pa-rs/releases**
- Look for the latest version (the top one)
- Download the ZIP file with "windows" in the name
  - Example: `c2patool-v0.23.4-x86_64-pc-windows-msvc.zip`

**2. Extract the files**

- Find your downloaded ZIP file (probably in your Downloads folder)
- Right-click it → **Extract All...**
- Pick a place you'll remember, like: `C:\Tools\c2patool\`
- Click **Extract**

**3. Add it to your Windows PATH**

This step makes Windows able to find c2patool from anywhere. Think of it like adding c2patool's phone number to your contacts.

1. Press the **Windows key** and search for: **"environment variables"**
2. Click on **"Edit the system environment variables"**
3. Click the **"Environment Variables..."** button at the bottom
4. In the top section (User variables), find and click on **"Path"**
5. Click **"Edit..."**
6. Click **"New"**
7. Type or paste the folder where you extracted c2patool
   - Example: `C:\Tools\c2patool\c2patool`
   - Make sure this is the folder that contains `c2patool.exe`
8. Click **OK** on all the windows

**4. Test it worked**

- **Important:** Close any open Command Prompts or PowerShell windows
- Open a **new** Command Prompt (search for "cmd" in Windows)
- Type: `c2patool --version`
- Press Enter

**What you should see:**
```
c2patool 0.23.4 (or similar)
```

**If it says "command not found":**
- Double-check you added the right folder to PATH
- Make sure you opened a NEW command prompt after changing PATH
- Restart your computer if it still doesn't work

✅ **Once you see a version number, you're done with this step!**

---

## Step 2: Set Up ComfyUI

### Find Your Certificate Paths

You'll need to type these into the node, so let's get them ready:

```
Private Key:
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key

Certificate:
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem
```

**💡 Pro tip:** Copy these to a Notepad file so you can easily copy-paste them later!

**⚠️ Notice:** We use forward slashes `/` not backslashes `\`. This is important!

---

## Step 3: Create Your Workflow

### Start ComfyUI

1. **Restart ComfyUI** if it's already running
   - This makes sure it loads the C2PA custom node

2. **Start fresh**
   - Open ComfyUI in your browser
   - Clear any existing workflow (or start a new one)

### Add the Nodes

**1. Add a Load Image node**
   - Right-click on the canvas
   - Go to: **image** → **Load Image**
   - Load any image you want to test with

**2. Add the C2PA Image Signer node**
   - Right-click on the canvas
   - Go to: **image** → **postprocessing** → **C2PA Image Signer**

**3. Connect them**
   - Connect the **IMAGE** output from Load Image
   - To the **image** input on C2PA Image Signer

Your workflow should look like:
```
[Load Image] → [C2PA Image Signer]
```

**That's it!** Don't add a Save Image node. The C2PA Signer saves the file automatically.

---

## Step 4: Configure the Node

Click on the C2PA Image Signer node and fill in these fields:

### Required Fields:

**private_key_path:**
```
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key
```
- Copy-paste this exactly
- Use forward slashes `/`

**cert_path:**
```
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem
```
- Copy-paste this exactly
- Use forward slashes `/`

### Optional Fields:

**filename_prefix:** (Leave as default or change if you want)
- Default: `C2PA_signed`
- This is what your saved files will be named

**manifest_json:** (Leave this empty for now)
- Type: `{}`
- This is for advanced features (we'll skip it for now)

---

## Step 5: Run It!

1. Click **"Queue Prompt"** (top right in ComfyUI)
2. Wait a few seconds
3. Check the console for any errors

**What should happen:**
- You won't see much! No preview image or anything.
- That's normal! The node saves the file behind the scenes.

**Where's my signed image?**

Check this folder:
```
<ComfyUI_path>/output/
```

Look for a file like:
```
C2PA_signed_20251006_094628.png
```

The number is the date and time it was created.

---

## Step 6: Verify It Worked!

Let's check that the image actually has a signature embedded in it.

### Use c2patool to verify:

1. **Open Command Prompt**
2. **Type this command** (update the filename to match yours):
   ```
   c2patool "<ComfyUI_path>/output/C2PA_signed_20251006_094628.png"
   ```
3. **Press Enter**

### What you should see:

A bunch of JSON data! Look for this line:
```json
"validation_state": "Valid"
```

**If you see "Valid":** 🎉 Success! Your image is signed!

**If you see an error or "No claim found":**
- Make sure you're checking the right file
- Make sure you didn't add a SaveImage node after the C2PA Signer
- Try running the workflow again

---

## 🎉 You Did It!

Congratulations! You just signed your first image with C2PA.

**What you learned:**
- ✅ How to install c2patool
- ✅ How to set up the C2PA node in ComfyUI
- ✅ How to sign an image
- ✅ How to verify the signature

---

## What's Next?

### Add More Information (Optional)

Want to add your name or other info to the signature? Try pasting this into the **manifest_json** field:

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

Replace "Your Name Here" with your actual name, then run the workflow again.

When you verify the new signed image, you'll see your name in the signature data!

### For AI-Generated Images

If you're making AI art, you can add generation details:

```json
{
  "assertions": [
    {
      "label": "com.example.ai-metadata",
      "data": {
        "model": "Stable Diffusion",
        "prompt": "your prompt here",
        "tool": "ComfyUI",
        "created_by": "Your Name"
      }
    }
  ]
}
```

This tells anyone who verifies the image exactly how it was made!

---

## Common Issues

### ❌ "c2patool not found"

**Problem:** Windows can't find c2patool.

**Fix:**
1. Did you add c2patool to your PATH? (Step 1.3)
2. Did you open a **new** Command Prompt after changing PATH?
3. Try restarting ComfyUI
4. Try restarting your computer

### ❌ "Invalid manifest JSON"

**Problem:** There's a typo in the JSON you pasted.

**Fix:**
- Just put `{}` in the manifest_json field to start
- If you added custom JSON, check for missing commas or brackets
- Use https://jsonlint.com/ to validate your JSON

### ❌ "Failed to read private key" or "Failed to read certificate"

**Problem:** The file paths are wrong.

**Fix:**
- Make sure you used forward slashes: `C:/Users/...`
- Don't use backslashes: `C:\Users\...`
- Copy-paste the paths directly from this guide
- Make sure you didn't add extra spaces

### ❌ Node doesn't appear in ComfyUI

**Problem:** ComfyUI hasn't loaded the custom node.

**Fix:**
1. Make sure the files are in: `<ComfyUI_path>/custom_nodes/c2pa_signer/`
2. Restart ComfyUI completely
3. Check the console for errors when ComfyUI starts

### ❌ "No claim found" when verifying

**Problem:** The signature got stripped out.

**Fix:**
- Did you add a SaveImage node after the C2PA Signer? Remove it!
- The C2PA Signer saves automatically - you don't need SaveImage

---

## Learn More

- **📖 [README.md](README.md)** - Detailed explanations of everything
- **📚 [SETUP_GUIDE.md](SETUP_GUIDE.md)** - Deep dive into how C2PA works
- **💡 [EXAMPLES.md](EXAMPLES.md)** - More example workflows and JSON templates

---

## Quick Reference

### File Paths (Copy these!)

```
Private Key:
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_private.key

Certificate:
<ComfyUI_path>/custom_nodes/c2pa_signer/keys/es256_certs.pem

Output Folder:
<ComfyUI_path>/output/
```

### Useful Commands

```bash
# Check if c2patool is installed
c2patool --version

# Verify a signed image
c2patool "path/to/your/image.png"

# List files in your output folder
ls <ComfyUI_path>/output/
```

---

## Need Help?

If you're stuck:
1. Read through the troubleshooting section above
2. Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for more detailed explanations
3. Make sure c2patool is properly installed (`c2patool --version`)
4. Double-check your file paths (forward slashes!)

**Remember:** The test certificates work perfectly for learning. When you're ready to release images professionally, you can look into getting your own unique certificates.

Happy signing! 🔐

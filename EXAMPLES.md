# C2PA Image Signer - Workflow Examples

This document provides practical examples for using the C2PA Image Signer node in ComfyUI.

---

## Table of Contents

1. [Basic Examples](#basic-examples)
2. [Attestation Examples](#attestation-examples)
3. [Real-World Scenarios](#real-world-scenarios)
4. [Advanced Configurations](#advanced-configurations)

---

## Basic Examples

### Example 1: Sign Any Image

**Workflow:**
```
[Load Image] → [C2PA Image Signer] → [Save Image]
```

**Node Configuration:**
- **private_key_path:** `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/private.key`
- **cert_path:** `<ComfyUI_path>/custom_nodes/c2pa_signer/keys/cert.pem`
- **manifest_json:** `{}`

**What it does:**
Creates a basic C2PA signature on any loaded image.

---

### Example 2: Sign AI-Generated Images

**Workflow:**
```
[CLIP Text Encode] → [KSampler] → [VAE Decode] → [C2PA Image Signer] → [Save Image]
```

**Node Configuration:**
- Same paths as Example 1
- **manifest_json:** Empty or add generation info (see below)

**What it does:**
Signs images right after generation, preserving AI creation metadata.

---

### Example 3: Sign After Post-Processing

**Workflow:**
```
[Load Image] → [Upscale] → [Color Correction] → [C2PA Image Signer] → [Save Image]
```

**Node Configuration:**
- Same paths as Example 1
- Add workflow metadata in manifest_json (see below)

**What it does:**
Signs images after enhancement, documenting the processing steps.

---

## Attestation Examples

### Example 1: Basic Author Attribution

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
            "name": "Mike C",
            "identifier": "https://yourwebsite.com"
          }
        ],
        "dateCreated": "2025-10-06"
      }
    }
  ]
}
```

**Use case:** Claim authorship of your work

---

### Example 2: AI Generation Metadata

```json
{
  "title": "AI Generated Artwork",
  "assertions": [
    {
      "label": "com.example.ai.generation",
      "data": {
        "model": "Stable Diffusion XL",
        "model_version": "1.0",
        "prompt": "A serene landscape with mountains at sunset",
        "negative_prompt": "blurry, distorted",
        "seed": 12345,
        "steps": 30,
        "cfg_scale": 7.5,
        "sampler": "DPM++ 2M Karras",
        "generation_tool": "ComfyUI"
      }
    },
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "author": [{"@type": "Person", "name": "Mike C"}],
        "creator": [{"@type": "Organization", "name": "My Studio"}],
        "keywords": ["AI art", "landscape", "digital art"]
      }
    }
  ]
}
```

**Use case:** Document AI generation parameters for transparency

---

### Example 3: Photo Editing Workflow

```json
{
  "title": "Portrait Enhancement Workflow",
  "assertions": [
    {
      "label": "com.example.editing.workflow",
      "data": {
        "original_source": "Canon EOS R5",
        "editing_steps": [
          "Noise reduction",
          "Skin retouching",
          "Color grading",
          "Sharpening"
        ],
        "software": "ComfyUI",
        "editor": "Mike C",
        "date_edited": "2025-10-06"
      }
    },
    {
      "label": "stds.schema-org.Photograph",
      "data": {
        "@context": "https://schema.org",
        "@type": "Photograph",
        "creator": [{"@type": "Person", "name": "Mike C"}],
        "copyrightHolder": [{"@type": "Person", "name": "Mike C"}],
        "copyrightYear": 2025
      }
    }
  ]
}
```

**Use case:** Track editing workflow for professional photography

---

### Example 4: Licensing Information

```json
{
  "assertions": [
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "author": [{"@type": "Person", "name": "Mike C"}],
        "license": "https://creativecommons.org/licenses/by-nc/4.0/",
        "copyrightHolder": [{"@type": "Person", "name": "Mike C"}],
        "copyrightYear": 2025,
        "creditText": "Photo by Mike C - CC BY-NC 4.0"
      }
    }
  ]
}
```

**Use case:** Embed licensing terms directly in the image

---

### Example 5: Multi-Layer Attestations

```json
{
  "title": "Professional AI Artwork",
  "assertions": [
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "CreativeWork",
        "author": [{"@type": "Person", "name": "Mike C"}],
        "dateCreated": "2025-10-06",
        "license": "https://creativecommons.org/licenses/by-nc-nd/4.0/"
      }
    },
    {
      "label": "com.mycompany.ai.metadata",
      "data": {
        "generation_model": "SDXL",
        "prompt": "cyberpunk city at night, neon lights",
        "style": "digital art"
      }
    },
    {
      "label": "com.mycompany.project",
      "data": {
        "project_name": "Cyberpunk Series",
        "project_id": "CP-2025-001",
        "client": "Example Corp",
        "usage_rights": "Exclusive commercial use"
      }
    },
    {
      "label": "com.mycompany.technical",
      "data": {
        "output_resolution": "4096x4096",
        "color_space": "sRGB",
        "bit_depth": 8
      }
    }
  ]
}
```

**Use case:** Comprehensive metadata for professional/commercial work

---

## Real-World Scenarios

### Scenario 1: AI Art Portfolio

**Goal:** Build a portfolio of AI-generated art with proper attribution

**Workflow:**
```
[Text to Image] → [Upscale] → [C2PA Image Signer] → [Save Image]
```

**Manifest JSON Template:**
```json
{
  "title": "{{artwork_title}}",
  "assertions": [
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "author": [{"@type": "Person", "name": "Your Name"}],
        "dateCreated": "{{date}}",
        "keywords": ["AI art", "{{style}}", "{{theme}}"]
      }
    },
    {
      "label": "org.aiart.generation",
      "data": {
        "model": "{{model_name}}",
        "prompt": "{{your_prompt}}",
        "is_ai_generated": true
      }
    }
  ]
}
```

**Benefits:**
- Proves you created the work
- Shows it's AI-generated (transparency)
- Timestamps creation date
- Includes generation details

---

### Scenario 2: Photo Restoration Service

**Goal:** Sign restored/enhanced photos with provenance

**Workflow:**
```
[Load Image] → [Denoise] → [Enhance Details] → [C2PA Image Signer] → [Save Image]
```

**Manifest JSON:**
```json
{
  "title": "Photo Restoration",
  "assertions": [
    {
      "label": "com.restoration.service",
      "data": {
        "original_condition": "faded, scratched",
        "restoration_date": "2025-10-06",
        "restorer": "Mike C",
        "techniques_used": [
          "Scratch removal",
          "Color restoration",
          "Contrast enhancement"
        ],
        "authenticity": "Original photo from 1985, digitally restored"
      }
    },
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "Photograph",
        "creator": [{"@type": "Person", "name": "Original Photographer"}],
        "contributor": [{"@type": "Person", "name": "Mike C"}],
        "dateModified": "2025-10-06"
      }
    }
  ]
}
```

---

### Scenario 3: Product Photography

**Goal:** Sign product images with studio/client info

**Workflow:**
```
[Load Image] → [Background Removal] → [Lighting Adjust] → [C2PA Image Signer] → [Save Image]
```

**Manifest JSON:**
```json
{
  "assertions": [
    {
      "label": "com.studio.product-photo",
      "data": {
        "client": "Example Corp",
        "product_id": "PROD-12345",
        "shoot_date": "2025-10-06",
        "photographer": "Mike C",
        "studio": "MC Photography",
        "usage_license": "Web and print, 12 months"
      }
    },
    {
      "label": "stds.schema-org.Photograph",
      "data": {
        "@context": "https://schema.org",
        "@type": "Photograph",
        "creator": [{"@type": "Person", "name": "Mike C"}],
        "copyrightHolder": [{"@type": "Organization", "name": "MC Photography"}]
      }
    }
  ]
}
```

---

### Scenario 4: NFT Creation with Provenance

**Goal:** Create NFTs with verifiable creation chain

**Workflow:**
```
[AI Generation] → [Style Transfer] → [C2PA Image Signer] → [Save Image] → [Mint NFT]
```

**Manifest JSON:**
```json
{
  "title": "NFT Artwork #001",
  "assertions": [
    {
      "label": "com.nft.metadata",
      "data": {
        "collection": "My NFT Collection",
        "edition": "1 of 100",
        "rarity": "rare",
        "traits": {
          "background": "cosmic",
          "style": "surreal",
          "colors": "vibrant"
        }
      }
    },
    {
      "label": "stds.schema-org.CreativeWork",
      "data": {
        "@context": "https://schema.org",
        "@type": "VisualArtwork",
        "author": [{"@type": "Person", "name": "Mike C"}],
        "dateCreated": "2025-10-06",
        "creator": [{"@type": "Person", "name": "Mike C"}]
      }
    },
    {
      "label": "org.blockchain.nft",
      "data": {
        "intended_blockchain": "Ethereum",
        "wallet_address": "0x...",
        "creation_tool": "ComfyUI + C2PA"
      }
    }
  ]
}
```

---

## Advanced Configurations

### Using Different Signing Algorithms

By default, the node uses `es256` (ECDSA with SHA-256). You can change this:

```json
{
  "alg": "es384",
  "assertions": [...]
}
```

**Available algorithms:**
- `es256` - ECDSA with SHA-256 (default, recommended)
- `es384` - ECDSA with SHA-384
- `es512` - ECDSA with SHA-512
- `ps256` - RSA PSS with SHA-256
- `ps384` - RSA PSS with SHA-384
- `ps512` - RSA PSS with SHA-512
- `ed25519` - EdDSA with Curve25519

**Note:** You must use a compatible key for each algorithm.

---

### Adding Trusted Timestamps

Include a timestamp from a Time Authority:

```json
{
  "ta_url": "http://timestamp.digicert.com",
  "assertions": [...]
}
```

**Popular Time Authority URLs:**
- DigiCert: `http://timestamp.digicert.com`
- Sectigo: `http://timestamp.sectigo.com`
- GlobalSign: `http://timestamp.globalsign.com`

---

### Custom Claim Generator

Add information about your signing tool:

```json
{
  "claim_generator": "ComfyUI C2PA Signer v1.0",
  "claim_generator_info": [
    {
      "name": "ComfyUI C2PA Signer",
      "version": "1.0.0"
    }
  ],
  "assertions": [...]
}
```

---

## Verification Examples

### Command Line Verification

After signing, verify your images:

```bash
# Basic info
c2patool signed_image.png

# Detailed manifest
c2patool signed_image.png --detailed

# Export manifest to JSON
c2patool signed_image.png --output manifest.json

# Verify multiple images
c2patool *.png
```

### Expected Output

```
C2PA Manifest found in: signed_image.png

Title: AI Generated Artwork
Claim Generator: ComfyUI C2PA Signer v1.0

Signature Info:
  Algorithm: es256
  Certificate: CN=C2PA Test Certificate
  Validation: Valid (Self-Signed)

Assertions:
  stds.schema-org.CreativeWork:
    Author: Mike C
    Date Created: 2025-10-06

  com.example.ai.generation:
    Model: Stable Diffusion XL
    Prompt: A serene landscape...
```

---

## Tips and Best Practices

### 1. Consistent Labeling
Use consistent assertion labels across your projects:
- `com.yourcompany.ai.metadata` for AI generation
- `com.yourcompany.project` for project info
- `stds.schema-org.CreativeWork` for standard metadata

### 2. Version Your Schemas
Include version info in custom attestations:
```json
{
  "label": "com.example.metadata",
  "data": {
    "schema_version": "1.0",
    ...
  }
}
```

### 3. Document Your Workflow
Create templates for different workflows and save them for reuse.

### 4. Test Before Production
Always test with your self-signed certificate before using production certificates.

### 5. Keep Metadata Concise
Don't include sensitive information in public attestations.

---

## Need More Examples?

- See `SETUP_GUIDE.md` for detailed explanations
- Visit: https://github.com/contentauth/c2pa-rs/blob/main/cli/docs/manifest.md
- Check Schema.org vocabulary: https://schema.org/

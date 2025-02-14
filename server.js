// Load environment variables
require("dotenv").config();

// Import required modules
const express = require("express");
const cors = require("cors");
const multer = require("multer");
const axios = require("axios");

// Initialize Express app
const app = express();
app.use(cors()); // Enable CORS for cross-origin requests
app.use(express.json()); // Allow JSON request bodies

// Multer setup for handling image uploads
const storage = multer.memoryStorage(); // Store uploaded images in memory
const upload = multer({ storage });

// Route to Upload Character Image
app.post("/upload-character", upload.single("image"), (req, res) => {
  if (!req.file) {
    return res.status(400).json({ error: "No file uploaded" });
  }

  // Convert uploaded image to base64 format
  const imageUrl = `data:image/png;base64,${req.file.buffer.toString(
    "base64"
  )}`;

  // Send image URL in response
  res.json({ image_url: imageUrl });
});

// Route to Generate AI Image using OpenAI's DALL·E
app.post("/generate-image", async (req, res) => {
  const { prompt, image_url } = req.body;

  try {
    // Call OpenAI API for image generation
    const response = await axios.post(
      "https://api.openai.com/v1/images/generations",
      {
        prompt: prompt,
        size: "1024x1024", // Image resolution
        model: "dall-e-3", // AI model to use
        user: "custom-user-id",
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${process.env.OPENAI_API_KEY}`, // Secure API Key
        },
      }
    );

    // Send the generated image URL in response
    res.json({ image_url: response.data.data[0].url });
  } catch (error) {
    console.error("Error generating image:", error);
    res.status(500).json({ error: "Failed to generate image" });
  }
});

// Start the server on port 5000
app.listen(5000, () => console.log("✅ Server running on port 5000"));

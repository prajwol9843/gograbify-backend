const express = require("express");
const cors = require("cors");
const ytdl = require("ytdl-core-discord");

const app = express();
app.use(cors());

app.get("/", (req, res) => {
  res.send("✅ GoGrabify Backend is Running");
});

app.get("/download", async (req, res) => {
  const videoURL = req.query.url;

  if (!videoURL || !ytdl.validateURL(videoURL)) {
    return res.status(400).json({ error: "Invalid YouTube URL" });
  }

  try {
    const info = await ytdl.getInfo(videoURL);
    const title = info.videoDetails.title.replace(/[^\w\s]/gi, "");

    res.setHeader(
      "Content-Disposition",
      `attachment; filename="${title}.mp4"`
    );
    const stream = await ytdl(videoURL, { format: "mp4" });
    stream.pipe(res);
  } catch (err) {
    res.status(500).json({
      error: "Download failed",
      detail: err.message || "Unknown error",
    });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});

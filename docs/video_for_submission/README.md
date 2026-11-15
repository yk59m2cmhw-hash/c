# Demo video for the submitted version (branch `claude/keen-bohr-rsb2xk`)

`smog_tomorrow_demo.mp4` is a 110-second screen recording of that branch's `demo.html` (commit `076d4df`) with English captions and no voice-over.

To record it again after `demo.html` changes (Playwright and ffmpeg are needed):

```bash
node record.js /path/to/folder-with-demo.html "$(pwd)"
ffmpeg -y -i page@*.webm -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -r 25 -movflags +faststart -an smog_tomorrow_demo.mp4
```

The captions quote numbers shown on the page (41, 54, 98, 12.2, 17.0, 22, 40, 16, 19) and the end card quotes the write-up. If any of them changes, edit `record.js` and `end.html` first.

The older `docs/demo_video.mp4` shows a different variant of the project (this branch's own demo) and is not the one to upload.

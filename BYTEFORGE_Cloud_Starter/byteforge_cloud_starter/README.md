# BYTEFORGE — fictional story video factory

Generates one vertical, original fictional story video per scheduled run (two runs each day), using AI narration, captions and muted Minecraft parkour gameplay.

## Gameplay rights and source
Candidate gameplay source: OrbitalNCG, https://www.youtube.com/watch?v=u7kdVe8q5zs. The video description supplied by the channel says reuse and monetisation are allowed with credit, and prohibits re-uploading the raw footage as standalone no-copyright gameplay. Retain evidence of the terms and verify they still apply before publishing.

This workflow does **not** scrape YouTube watch pages. For a gameplay library, place authorised clips named `parkour_000.mp4`, `parkour_001.mp4`, etc. in `assets/gameplay/`. The renderer randomly selects one clip for each story. Alternatively, place one file at `assets/minecraft_parkour.mp4` or set `BACKGROUND_URL` to a direct authorised MP4/WebM/MOV URL. The original gameplay audio is discarded; only generated narration is included.

## Output
- One original, fictional 9:16 MP4 story per scheduled run (two scheduled runs per day).
- AI narration via Edge TTS (no paid AI API key).
- Burned-in captions and metadata.
- Video and metadata artifacts retained for 14 days.
- Every story is labelled fictional and requires human review.

## Run
Enable GitHub Actions, add the authorised gameplay assets, then run **BYTEFORGE story factory** manually once. Scheduled runs happen twice daily at 10:17 and 17:17 UTC (GitHub schedule is best effort).

## Limitations
Generates downloadable artifacts; it does not automatically post to social platforms. No guaranteed views, income, or monetisation. Do not upload raw gameplay as a standalone video.

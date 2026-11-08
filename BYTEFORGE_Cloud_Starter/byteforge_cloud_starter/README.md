# BYTEFORGE Cloud Starter

A low-cost starter pipeline for creating original vertical tech videos on a cloud schedule.

## What it does
- Runs on GitHub Actions (cloud; your PC can be off).
- Twice daily, selects the next original script from `scripts/topics.json`.
- Creates a 1080x1920 MP4 with animated typography, captions, and an optional generated voice.
- Saves the MP4 and metadata as a downloadable GitHub Actions artifact.
- Uses a human review step before anything is published.

## Honest limitations
This starter **does not publish automatically**. YouTube API upload needs a Google Cloud project, OAuth consent and secure token setup. TikTok Direct Post requires an approved app, `video.publish` authorization and audit for public visibility. TikTok unaudited clients are restricted to private posts. The safe first milestone is generating reviewed videos in the cloud.

GitHub scheduled jobs are best-effort and can be delayed. This is not a guaranteed-to-the-minute scheduler.

## Setup
1. Create a GitHub repository named `byteforge-cloud`.
2. Upload all files from this folder to the repository's default branch.
3. Open **Actions** and enable workflows.
4. Run **BYTEFORGE video factory** manually once using **Run workflow**.
5. Download the `byteforge-videos` artifact from the completed run.
6. Review each video for factual accuracy, audio, rights and platform rules before posting.

## Schedule
The workflow runs at 10:17 and 17:17 UTC daily (11:17 and 18:17 in UK winter; 11:17 and 18:17 in UK summer after daylight saving changes are not automatically accounted for by this UTC schedule). Change the cron in `.github/workflows/video-factory.yml` if needed.

## Voice
The workflow attempts a free Edge TTS voice. If network access or the voice service fails, it still renders a silent-caption video. No API key is required.

## Change topics
Edit `scripts/topics.json`. Use original wording and verify claims. Do not use unlicensed clips, music, logos or copied scripts.

## Costs
GitHub Actions has usage limits and free allowances that depend on account/repository settings. The pipeline is designed to use no paid AI API. Rendering is intentionally template-based; more advanced generative visuals or premium voices may cost money.

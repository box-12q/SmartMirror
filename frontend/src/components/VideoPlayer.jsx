/**
 * Camera preview placeholder: centered, translucent camera icon with a
 * caption, plus a hand-detection toggle pinned to the bottom-right
 * corner. Real video frames will replace the placeholder later.
 * Loaded by index.html before App.jsx, exposed on `window`.
 *
 * .video-player fills the whole content area and is position: relative,
 * which is the anchoring box for DetectionToggle's absolute positioning.
 */
function VideoPlayer() {
  return (
    <div className="video-player">
      {/* \uFE0E forces monochrome (text) presentation so the glyph
          takes our purple color instead of the emoji palette */}
      <span className="video-player__icon">{'\u{1F4F7}\uFE0E'}</span>
      <span className="video-player__label">Camera preview</span>

      <DetectionToggle />
    </div>
  );
}

window.VideoPlayer = VideoPlayer;

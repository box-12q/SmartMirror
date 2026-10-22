/**
 * Camera preview placeholder: centered, translucent camera icon with a
 * caption. Real video frames will replace this later (Electron IPC or
 * <video> fed by a local stream).
 * Loaded by index.html before App.jsx, exposed on `window`.
 */
function VideoPlayer() {
  return (
    <div className="video-player">
      {/* \uFE0E forces monochrome (text) presentation so the glyph
          takes our purple color instead of the emoji palette */}
      <span className="video-player__icon">{'\u{1F4F7}\uFE0E'}</span>
      <span className="video-player__label">Camera preview</span>
    </div>
  );
}

window.VideoPlayer = VideoPlayer;

/**
 * Hand-detection on/off switch rendered in the bottom-right corner of
 * the camera preview. Uses useState (React global from the UMD build —
 * Babel standalone does not process ES module imports).
 *
 * Visual design: a single dark-purple capsule split by a thin vertical
 * seam. Both halves show concentric ring outlines; the ACTIVE half also
 * has a filled white dot in the centre. The active half follows the
 * React state; wiring to the Python detection pipeline will go through
 * the preload API later.
 */
const { useState } = React;

function DetectionToggle() {
  const [enabled, setEnabled] = useState(true);

  return (
    <div className="detection-toggle">
      {/* Detection ON */}
      <button
        type="button"
        className="detection-toggle__half"
        aria-label="Enable hand detection"
        aria-pressed={enabled}
        onClick={() => setEnabled(true)}
      >
        {/* Concentric rings + (when active) a filled centre dot */}
        <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">
          <circle cx="11" cy="11" r="9" fill="none" stroke="currentColor" strokeWidth="1.25" />
          <circle cx="11" cy="11" r="4.5" fill="none" stroke="currentColor" strokeWidth="1.25" />
          {enabled && <circle cx="11" cy="11" r="2" fill="currentColor" />}
        </svg>
      </button>

      {/* Detection OFF */}
      <button
        type="button"
        className="detection-toggle__half"
        aria-label="Disable hand detection"
        aria-pressed={!enabled}
        onClick={() => setEnabled(false)}
      >
        {/* Same rings; the centre dot appears here when this side is selected */}
        <svg width="22" height="22" viewBox="0 0 22 22" aria-hidden="true">
          <circle cx="11" cy="11" r="9" fill="none" stroke="currentColor" strokeWidth="1.25" />
          <circle cx="11" cy="11" r="4.5" fill="none" stroke="currentColor" strokeWidth="1.25" />
          {!enabled && <circle cx="11" cy="11" r="2" fill="currentColor" />}
        </svg>
      </button>
    </div>
  );
}

window.DetectionToggle = DetectionToggle;

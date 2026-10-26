/**
 * Hand-detection on/off switch rendered in the bottom-right corner of
 * the camera preview. Uses useState (React global from the UMD build —
 * Babel standalone does not process ES module imports).
 *
 * Visual design: one capsule with two halves. The ACTIVE half is filled
 * with the signature purple, the INACTIVE half gets a soft translucent
 * gray. Each half shows a single clean ring; the active one also has a
 * filled white centre dot. Wiring to the Python detection pipeline will
 * go through the preload API later.
 */
const { useState } = React;

function DetectionToggle() {
  const [enabled, setEnabled] = useState(true);

  return (
    <div className="detection-toggle">
      {/* Detection ON */}
      <button
        type="button"
        className={'detection-toggle__half ' + (enabled ? 'detection-toggle__half--active' : 'detection-toggle__half--idle')}
        aria-label="Enable hand detection"
        aria-pressed={enabled}
        onClick={() => setEnabled(true)}
      >
        {/* One ring + (when selected) a filled centre dot */}
        <svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">
          <circle cx="13" cy="13" r="9.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
          {enabled && <circle cx="13" cy="13" r="3.2" fill="currentColor" />}
        </svg>
      </button>

      {/* Detection OFF */}
      <button
        type="button"
        className={'detection-toggle__half ' + (!enabled ? 'detection-toggle__half--active' : 'detection-toggle__half--idle')}
        aria-label="Disable hand detection"
        aria-pressed={!enabled}
        onClick={() => setEnabled(false)}
      >
        <svg width="26" height="26" viewBox="0 0 26 26" aria-hidden="true">
          <circle cx="13" cy="13" r="9.5" fill="none" stroke="currentColor" strokeWidth="1.5" />
          {!enabled && <circle cx="13" cy="13" r="3.2" fill="currentColor" />}
        </svg>
      </button>
    </div>
  );
}

window.DetectionToggle = DetectionToggle;

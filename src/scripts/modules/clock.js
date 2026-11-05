/**
 * Live clock for the "ID, INA" header label (Asia/Jakarta time).
 * Wraps the center colon (:) in `.clock-colon` so it flashes in time with the seconds.
 * @param {HTMLElement | null} el
 */
export function initClock(el) {
  if (!el) return;

  const formatter = (() => {
    try {
      return new Intl.DateTimeFormat('en-US', {
        timeZone: 'Asia/Jakarta',
        hour: '2-digit',
        minute: '2-digit',
        hour12: true,
      });
    } catch {
      return null;
    }
  })();

  // Build persistent DOM nodes so the colon animation is never interrupted on tick
  el.textContent = '';
  const hourNode = document.createElement('span');
  const colonNode = document.createElement('span');
  colonNode.className = 'clock-colon';
  colonNode.textContent = ':';
  // Phase-lock the 1s blink animation to the system clock's current millisecond offset
  colonNode.style.animationDelay = `-${Date.now() % 1000}ms`;
  const restNode = document.createElement('span');

  el.append(hourNode, colonNode, restNode);

  const formatTimeString = (date) => {
    if (formatter) {
      return formatter.format(date);
    }
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const ampm = date.getHours() >= 12 ? 'PM' : 'AM';
    const hours = date.getHours() % 12 || 12;
    return `${String(hours).padStart(2, '0')}:${minutes} ${ampm}`;
  };

  const tick = () => {
    const formatted = formatTimeString(new Date());
    const colonIdx = formatted.indexOf(':');
    if (colonIdx !== -1) {
      const hr = formatted.slice(0, colonIdx);
      const rest = formatted.slice(colonIdx + 1);
      if (hourNode.textContent !== hr) hourNode.textContent = hr;
      if (restNode.textContent !== rest) restNode.textContent = rest;
    } else {
      hourNode.textContent = formatted;
      restNode.textContent = '';
    }
  };

  tick();
  setInterval(tick, 1000);
}

export async function onRequestGet({ request }) {
  const url = new URL(request.url);
  const summary = url.searchParams.get('summary') || 'Double Mood';
  const description = url.searchParams.get('description') || '';
  const dtstart = url.searchParams.get('dtstart') || '';
  const dtend = url.searchParams.get('dtend') || '';
  const uid = url.searchParams.get('uid') || Date.now().toString();

  function escapeIcs(s) {
    return (s || '').replace(/\\/g, '\\\\').replace(/;/g, '\\;').replace(/,/g, '\\,').replace(/\n/g, '\\n');
  }

  const ics = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//Double Mood//EN',
    'CALSCALE:GREGORIAN',
    'BEGIN:VEVENT',
    'UID:' + escapeIcs(uid),
    'DTSTAMP:' + dtstart,
    'DTSTART:' + dtstart,
    'DTEND:' + dtend,
    'SUMMARY:' + escapeIcs(summary),
    'DESCRIPTION:' + escapeIcs(description),
    'END:VEVENT',
    'END:VCALENDAR'
  ].join('\r\n');

  return new Response(ics, {
    headers: {
      'Content-Type': 'text/calendar; charset=utf-8',
      'Content-Disposition': 'attachment; filename="double-mood.ics"',
      'Cache-Control': 'no-cache'
    }
  });
}

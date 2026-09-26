// Run: node tests/test_voice.js [path/to/deck.html]
const fs = require('fs');
const file = process.argv[2] || __dirname + '/../skills/slide-deck/template/deck.html';
const src = fs.readFileSync(file, 'utf8');
const code = src.split('/* VOICE-PARSER:BEGIN */')[1].split('/* VOICE-PARSER:END */')[0];
const parseVoice = new Function(code + '; return parseVoice;')();

const index = [
  { title: 'Title', hay: 'title start beginning home example director of analytics'.split(' ') },
  { title: 'Summary', hay: 'summary executive overview key numbers the short version'.split(' ') },
  { title: 'Follow-up', hay: 'follow up retention follow up finding one finding 1'.split(' ') },
  { title: 'Recommendations', hay: 'recommendations actions next steps what to do plan what we should do'.split(' ') },
  { title: 'Appendix', hay: 'appendix method data quality caveats'.split(' ') },
];
const cases = [
  ['go back to the first slide', 'goto:0'], ['first slide', 'goto:0'], ['back to the beginning', 'home'], ['start over', 'home'],
  ['go to the last slide', 'end'], ['next', 'next'], ['next slide', 'next'], ['go to the next slide', 'next'], ['next one please', 'next'],
  ['back', 'prev'], ['go back', 'prev'], ['previous slide', 'prev'], ['go back one', 'prev'],
  ['more', 'right'], ['show me more', 'right'], ['show me the breakdown', 'right'], ['dig deeper', 'right'],
  ['back out', 'left'], ['go left', 'left'],
  ['go to recommendations', 'goto:3'], ['take me to the recommendations', 'goto:3'], ['recommendations', 'goto:3'],
  ['go back to the summary', 'goto:1'], ['show the appendix', 'goto:4'], ['go to data quality', 'goto:4'],
  ['slide 3', 'goto:2'], ['slide three', 'goto:2'], ['go to slide number four', 'goto:3'], ['third slide', 'goto:2'],
  ['go to the retention slide', 'goto:2'], ['finding one', 'goto:2'], ['go to next steps', 'goto:3'],
  ['show notes', 'notes'], ['open the menu', 'menu'], ['stop listening', 'voiceoff'],
  ['um', 'null'], ['the weather is nice', 'null'],
];
const dash = [{ field: 'plan', label: 'Plan', values: ['Basic', 'Plus', 'Premium'] }, { field: 'channel', label: 'Channel', values: ['Search', 'Social', 'Referral'] }];
const dashCases = [
  ['filter premium', 'filter:plan=Premium'], ['just the referral channel', 'filter:channel=Referral'], ['show me premium members', 'filter:plan=Premium'],
  ['premium', 'filter:plan=Premium'], ['clear filters', 'filter:clear'], ['reset the filters', 'filter:clear'], ['show all', 'filter:clear'],
  ['next', 'next'], ['go to recommendations', 'goto:3'], ['go back to the first slide', 'goto:0'],
];
let fail = 0;
for (const [say, want] of cases) {
  const r = parseVoice(say, index);
  const got = r ? (r.act === 'goto' ? 'goto:' + r.n : r.act) : 'null';
  const ok = got === want; if (!ok) fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  "${say}" → ${got}${ok ? '' : '   (want ' + want + ')'}`);
}
for (const [say, want] of dashCases) {
  const r = parseVoice(say, index, dash);
  const got = !r ? 'null' : r.act === 'goto' ? 'goto:' + r.n : r.act === 'filter' ? (r.clear ? 'filter:clear' : `filter:${r.field}=${r.value}`) : r.act;
  const ok = got === want; if (!ok) fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  [dashboard] "${say}" → ${got}${ok ? '' : '   (want ' + want + ')'}`);
}
const ctx = { filters: dash, charts: ['New members by month', '90-day retention by channel', 'Revenue by plan'], zoomed: false };
const zoomCases = [
  ['zoom in on the retention chart', false, 'zoom:1'], ['zoom in on revenue', false, 'zoom:2'], ['make chart 3 bigger', false, 'zoom:2'],
  ['zoom in on the second chart', false, 'zoom:1'], ['zoom in', false, 'zoom:0'], ['focus on new members', false, 'zoom:0'],
  ['zoom out', true, 'unzoom'], ['close that', true, 'unzoom'], ['go back', true, 'unzoom'],
  ['zoom out', false, 'left'], ['next', false, 'next'], ['filter premium', false, 'filter:plan=Premium'],
];
for (const [say, zoomed, want] of zoomCases) {
  const r = parseVoice(say, index, { ...ctx, zoomed });
  const got = !r ? 'null' : r.act === 'zoom' ? 'zoom:' + r.n : r.act === 'filter' ? `filter:${r.field}=${r.value}` : r.act;
  const ok = got === want; if (!ok) fail++;
  console.log(`${ok ? 'PASS' : 'FAIL'}  [zoom${zoomed ? ', zoomed' : ''}] "${say}" → ${got}${ok ? '' : '   (want ' + want + ')'}`);
}
const total = cases.length + dashCases.length + zoomCases.length;
console.log(`\n${total - fail}/${total} passed`);
process.exit(fail ? 1 : 0);

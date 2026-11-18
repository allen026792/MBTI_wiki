const slides = [...document.querySelectorAll('.stage')];
const prev = document.querySelector('#prev');
const next = document.querySelector('#next');
const count = document.querySelector('#counter');
const chapterLinks = [...document.querySelectorAll('.lesson-nav a')];
const progress = document.querySelector('.deck-progress');
let current = 0;
function show(focus = false) {
  current = Math.max(0, slides.findIndex(slide => '#' + slide.id === location.hash));
  slides.forEach((slide, i) => slide.hidden = i !== current);
  count.textContent = `${current + 1} / ${slides.length}`;
  chapterLinks.forEach((link, i) => {
    if (i === current) link.setAttribute('aria-current', 'step');
    else link.removeAttribute('aria-current');
  });
  progress.max = slides.length;
  progress.value = current + 1;
  prev.disabled = current === 0;
  next.disabled = current === slides.length - 1;
  if (focus) slides[current].querySelector('h1').focus();
}
function move(step) {
  const slide = slides[current + step];
  if (slide) location.hash = slide.id;
}
prev.onclick = () => move(-1);
next.onclick = () => move(1);
window.addEventListener('hashchange', () => show(true));
document.addEventListener('keydown', event => {
  if (event.target.matches('input') || event.ctrlKey || event.altKey || event.metaKey) return;
  if (event.key === 'ArrowRight') move(1);
  if (event.key === 'ArrowLeft') move(-1);
});
for (const quiz of document.querySelectorAll('.quiz')) {
  const choices = quiz.querySelectorAll('button');
  for (const choice of choices) {
    choice.onclick = () => {
      for (const button of choices) button.setAttribute('aria-pressed', String(button === choice));
      quiz.querySelector('.feedback').textContent = choice.dataset.feedback;
    };
  }
}
const score = document.querySelector('#score');
function update() {
  const value = Number(score.value);
  const label = value >= 50 ? 'E' : 'I';
  document.querySelector('#value').textContent = value;
  document.querySelector('#outcome').textContent = `第一次：49 分 → I。第二次：${value} 分 → ${label}。兩次相差 ${Math.abs(value - 49)} 分。`;
}
if (score) {
  score.oninput = update;
  update();
}
show();

const preferenceNames = {
  E: '注意力較朝外', I: '注意力較朝內',
  S: '偏重具體資訊', N: '偏重模式與可能性',
  T: '判斷時偏重原則', F: '判斷時偏重價值與人的影響',
  J: '外在生活偏向先安排', P: '外在生活偏向保留彈性'
};
const typeButtons = [...document.querySelectorAll('.type-code')];
for (const button of typeButtons) {
  button.addEventListener('click', () => {
    for (const option of typeButtons) option.setAttribute('aria-pressed', String(option === button));
    const code = button.dataset.type;
    document.querySelector('#type-result').textContent = [...code].map(letter => `${letter} · ${preferenceNames[letter]}`).join(' ｜ ');
  });
}

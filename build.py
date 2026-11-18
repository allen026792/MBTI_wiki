from pathlib import Path

dist = Path('dist')
notes = Path('wiki/sources')
dist.mkdir(exist_ok=True)
notes.mkdir(parents=True,exist_ok=True)
sources = [
('四組偏好','Myers & Briggs Foundation · The Preferences','https://www.myersbriggs.org/my-mbti-personality-type/the-mbti-preferences/','四組偏好各描述不同面向。E／I 談注意力與能量取向，S／N 談接收資訊，T／F 談做決定時的著重點，J／P 談面對外在生活的方式。偏好不等於能力。','官方框架說明'),
('結果回饋','Myers & Briggs Foundation · Verification of Best-Fit Type','https://www.myersbriggs.org/unique-features-of-myers-briggs/best-fit-type/','官方的 best-fit type 解讀過程包含了解各類型和檢視結果。回饋有助於比對四字母與自己的經驗。','官方解讀流程'),
('分數信度','Capraro & Capraro (2002) · Score Reliability Across Studies','https://eric.ed.gov/?id=EJ662114','綜合分析指出，所研究的 MBTI 量尺分數通常具良好的內部一致性與重測信度。分數信度的估計與四字母完全一致的比例是不同指標。','摘要，分數信度與研究間變異'),
('類型與維度','McCrae & Costa (1989) · Reinterpreting the MBTI','https://pubmed.ncbi.nlm.nih.gov/2709300/','這項研究未找到支持偏好天然二分的證據，研究者以四個相對獨立的維度解讀結果，並發現它們與大五的部分面向相關。','摘要，二分假設與相關結果'),
('大五人格','Soto & John (2017) · The Next Big Five Inventory','https://pubmed.ncbi.nlm.nih.gov/27055049/','BFI-2 用五個連續領域和十五個較細的面向描述人格。可以呈現某一特質的程度，和四字母的呈現方式不同。','摘要，五領域與十五面向')
]
def page(title, body,script=''):
    layout = 'deck-page' if script else 'catalog-page'
    return f'<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><link rel="stylesheet" href="style.css"><body class="{layout}"><header><a class="brand" href="index.html"><span>✦</span> 人格觀察簿</a><nav><a href="index.html#catalog">講義庫</a><a href="wiki.html">Wiki</a><a href="workflow.html">製作紀錄</a></nav></header><main>{body}</main>{script}</body></html>'
def write(name,title,body,script=''):
    (dist/name).write_text(page(title,body,script))
def refs(ids):
    return '<aside class="refs"><span>本頁依據</span>'+''.join(f'<a href="wiki.html#S{i:02}">{sources[i-1][0]}</a>' for i in ids)+'</aside>'
def quiz(prompt,opts):
    return '<div class="quiz"><h2>'+prompt+'</h2><div class="choices">'+''.join(f'<button type="button" data-feedback="{answer}" aria-pressed="false">{label}</button>' for label,answer in opts)+'</div><p class="feedback" role="status"></p></div>'
cards = []
index = ['# 人格觀察簿 LLM Wiki','']
for i,(name,title,url,summary,location) in enumerate(sources,1):
    key=f'S{i:02}'
    cards.append(f'<article id="{key}" class="sheet"><small>{key} · {location}</small><h2>{name}</h2><p>{summary}</p><a href="{url}">{title} ↗</a></article>')
    (notes/f'{key}.md').write_text(f'# {key} {name}\n\n[{title}]({url})\n\n查閱位置：{location}\n\n{summary}\n')
    index.append(f'- [{key} {name}](sources/{key}.md)')
Path('wiki/index.md').write_text('\n'.join(index)+'\n')
prefs = ''.join(f'<details class="sheet"><summary><b>{pair}</b> {label}</summary><p>{copy}</p></details>' for pair,label,copy in [
('E／I','注意力放在哪裡？','E 偏向外在的人與活動，I 偏向內在的想法與反思。兩者都可能喜歡和朋友相處。'),
('S／N','怎麼接收資訊？','S 偏重眼前的具體資訊與細節，N 偏重模式、連結與可能性。'),
('T／F','怎麼做判斷？','T 傾向先看一致的原則和邏輯，F 傾向先考量價值及對人的影響。'),
('J／P','怎麼面對外在生活？','J 偏向在外在生活中先做安排，P 偏向保留彈性與選項。')])
slides = [
('開場','同一個人，為什麼會測出兩種 MBTI？','<p>小安上次得到 <b>INFP</b>，這次卻拿到 <b>ENFP</b>。只看這兩個結果，你能判斷小安變外向了嗎？</p>'+quiz('先猜一次',[('一定變外向了','還需要看分數、測量條件和使用的工具。'),('光看字母還不夠','答對了。下一頁先看看每個字母在描述什麼。')]),[1,2]),
('四組偏好','四個字母在說什麼？','<p>每組選取一個字母，四組組合起來有 16 種代碼。點開卡片看每組的問題。</p><div class="grid prefs">'+prefs+'</div>',[1]),
('分類實驗','只差兩分，字母卻不同？','<p>這是二分類教學模型。虛構分數 ≥ 50 分記為 E，低於 50 分記為 I。第一次固定在 49 分。拉動第二次分數，比較標籤。</p><div class="sheet lab"><label for="score">第二次分數 <output id="value" for="score">51</output></label><input id="score" type="range" min="40" max="60" value="51"><div class="scale"><span>40 · 偏 I</span><span>50 · 分界</span><span>60 · 偏 E</span></div><p id="outcome" role="status"></p><small>本頁分數與門檻是示意，官方量表使用自己的計分及解讀程序。</small></div>',[2,4]),
('心理計量','信度與效度，各在問什麼？','<div class="grid"><article class="sheet"><h2>信度</h2><p>同樣條件下，分數是否一致？分數的重測相關和四字母完全相同的比例是兩件事。</p></article><article class="sheet"><h2>效度</h2><p>你想從分數做出某種解讀時，有多少證據支持這個解讀？用途不同，需要的證據也不同。</p></article></div>'+quiz('一把尺每次都多量 2 公分，能說明什麼？',[('一致就代表讀值準確','想想每次都多出來的 2 公分。'),('讀值很一致，但會有偏差','答對了。一致只是其中一部分，還要檢查讀值能否支持你要的判斷。')]),[3,4]),
('人格模型','從類型代碼到連續特質','<p>四字母把結果整理成一個類型。大五人格則分別描述外向性、親和性、盡責性、負向情緒性與開放性。兩套模型的維度不能逐一換算。</p><div class="sheet"><h2>同一個例子，兩種描述</h2><p><b>類型代碼</b>會顯示 INFP 或 ENFP。<br><b>連續描述</b>可以保留小安在某個特質上接近中間的資訊。</p></div>',[4,5]),
('回到開場','看到四個字母改變，先問什麼？','<ol><li>兩次用的是同一套工具嗎？</li><li>分數差距和兩次作答條件是什麼？</li><li>這些結果能支持我想做的判斷嗎？</li></ol><p>如果手上只有兩組字母，可以先把它當成反思的起點，再用具體生活例子檢視。</p><a class="cta" href="wiki.html">查看原始資料 →</a>',[1,2,3,4,5])]
def compare(left, right):
    return '<div class="grid contrasts">'+''.join(f'<article class="sheet"><h2>{title}</h2><p>{text}</p></article>' for title,text in (left,right))+'</div>'

expansion = [
('E／I','做完報告，你想先聊聊還是先整理？',
 '<p>同一場小組報告，可用兩種方式回想自己平常如何整理經驗。</p>'+compare(
 ('E｜透過交流整理','小安想找組員聊聊剛剛發生什麼，邊說邊整理自己的看法。'),
 ('I｜透過反思整理','小安想先自己寫下重點，想清楚後再跟組員說。'))+
 '<p><strong>判讀提醒：</strong>一次開會表現無法決定偏好。觀察多個情境中的習慣，比看一次發言次數有用。</p>',[1]),
('S／N','收到一份作業，你會先看什麼？',
 '<p>兩位同學看到同一份作業說明，首先注意的資訊可能不同。</p>'+compare(
 ('S｜先抓具體線索','先讀繳交格式、期限和範例，再規劃完成順序。'),
 ('N｜先找模式與可能性','先猜老師想訓練的能力，再想有哪些題目可以延伸。'))+
 quiz('先找跨章節的共同規律，在這個例子較接近哪個著重點？',[('S','S 的示例較著重可直接觀察的細節。'),('N','答對了，這裡著重資訊之間的連結。')]),[1]),
('T／F','同學遲交，小組怎麼決定？',
 '<p>假設小組要討論是否延期，兩位同學都在認真做判斷，只是先問的問題不同。</p>'+compare(
 ('T｜原則與一致性','先問原本規則是什麼，以及這個例外能否一致地適用於其他人。'),
 ('F｜價值與影響','先問有哪些人的需要應被納入，以及團隊最重視哪個價值。'))+
 '<p>同一個決策可以同時考量原則與人的處境。這裡示範的是先把注意力放在哪裡。</p>',[1]),
('J／P','週末旅行，你會怎麼準備？',
 '<p>兩人都想玩得開心，一位傾向先定好安排，另一位希望保留探索空間。</p>'+compare(
 ('J｜先做安排','先確定集合時間、交通和主要景點，讓行程容易協調。'),
 ('P｜保留選項','先確認必要的交通資訊，其他安排依天氣和現場狀況調整。'))+
 '<p>這組偏好描述面對外在生活的方式。準時、整潔等單一行為還受工作要求與習慣影響。</p>',[1]),
]
from itertools import product
codes=list(map(''.join,product('IE','SN','TF','JP')))
code_grid='<div class="codes" aria-label="十六種代碼">'+''.join(f'<button type="button" class="type-code" data-type="{code}" aria-pressed="false">{code}</button>' for code in codes)+'</div>'
types=('組合練習','四組偏好，怎麼組成 16 種代碼？',
 '<p>每一組有兩個字母，所以共有 <strong>2 × 2 × 2 × 2 = 16</strong> 種組合。點一個代碼，拆開看每個位置。</p>'+code_grid+
 '<p class="sheet" id="type-result" role="status">試著選 INFP，再選 ENFP，看看差在哪一個位置。</p>',[1])
near=('讀懂變動','先查三件事，再解釋重測',
 '<ol class="checklist"><li><strong>工具。</strong>兩次是同一份量表、版本與計分方式嗎？網路測驗即使也顯示四字母，來源仍要確認。</li><li><strong>作答情境。</strong>這次是想像平常的自己，還是剛好想到工作或社團中的自己？</li><li><strong>證據。</strong>目前只看得到代碼，還是也掌握其他分數、回饋與跨情境的例子？</li></ol><p>這些是要查的方向。小安案例只提供兩個代碼，因此原因還待確認。</p>',[2,3,4])
retest=('重測信度','兩種「穩定」為什麼不同？',
 '<p>假設三個人的示意分數都增加兩分。分數順序完全一樣，卻有人跨過 50 分的分類線。</p><div class="scroll"><table><thead><tr><th>人物</th><th>第一次</th><th>第二次</th><th>代碼有變？</th></tr></thead><tbody><tr><td>甲</td><td>40 · I</td><td>42 · I</td><td>否</td></tr><tr><td>乙</td><td>49 · I</td><td>51 · E</td><td>有</td></tr><tr><td>丙</td><td>56 · E</td><td>58 · E</td><td>否</td></tr></tbody></table></div><p>這組假想資料的分數相關為 1，這一個字母的一致率卻是 2／3。兩個指標在回答不同問題。</p>',[3,4])
practice=('課後練習','把測量概念用在新情境',
 quiz('某份測驗重做後分數很一致。能直接拿來決定誰適合當組長嗎？',[
 ('可以，一致就代表適用','一致性提供的是信度資訊。判斷組長適任性，還要有支持這個用途的效度證據。'),
 ('還需要適任性的證據','答對了。決策用途要另外檢驗，例如分數是否能支持對實際帶隊表現的推論。')])+
 quiz('兩人都得到 E，能判定他們在連續尺度上位置相同嗎？',[
 ('可以，相同字母代表同分','同一分類可以涵蓋不同分數。回到分類實驗，試試 51 和 59。'),
 ('不能，只知道同一類','答對了。分類保留類別，分數才能呈現位置差異。')]),[3,4,5])
code_intro = ('讀懂代碼','看到 INFP，先從哪裡讀？',
    '<p>四個位置各有固定的問題。第一格看注意力取向，第二格看接收資訊，第三格看判斷，第四格看如何面對外在生活。下一頁可以自己拆開任何代碼。</p>',[1])
code_compare = ('代碼練習','INFP 和 ENFP 差在哪裡？',
    quiz('只看字母，這兩個代碼差在哪一組偏好？',[('接收資訊 S／N','兩組代碼的第二格都是 N。'),('注意力取向 E／I','答對了，唯一不同的是第一格。')])+'<p>接著如果想理解同一人的字母為何可能改變，可以讀<a href="retest.html">重測與測量</a>。</p>',[1,2])
decks = [
    ('preferences.html','MBTI 入門與四組偏好','從小組報告、旅行和作業，理解四組偏好在描述什麼。',[slides[0],slides[1],*expansion]),
    ('types.html','16 種人格代碼','點選任一代碼，拆解四個字母並練習比較。',[code_intro,types,code_compare]),
    ('retest.html','重測、信度與效度','操作分數滑桿，理解標籤變動和測量證據。',[slides[2],near,slides[3],retest,practice]),
    ('big-five.html','大五人格與結果判讀','比較連續特質與類型，回到日常情境判讀結果。',[slides[4],slides[5]])
]
catalog = '<h2 id="catalog">分類講義</h2><div class="grid menu">'+''.join(
    f'<a class="sheet" href="{file}"><small>{len(items)} 頁</small><h3>{title}</h3><p>{description}</p><span>開啟講義 →</span></a>'
    for file,title,description,items in decks)+'</div>'
hero = '<section class="hero"><div><h1>人格<mark>觀察簿</mark></h1><p>從 MBTI 四個字母出發，探索偏好、人格分類和測量。</p><a class="cta" href="#catalog">挑一份講義 →</a></div><div class="illustration" aria-hidden="true"><b>INFP</b><b>ENFP</b></div></section>'
write('index.html','人格觀察簿｜分類講義庫',hero+catalog)
write('lesson.html','人格觀察簿｜分類講義庫',hero+catalog)
footer = '<footer class="deck-controls"><output id="counter" aria-live="polite"></output><button id="prev" aria-label="上一頁">←</button><button id="next" aria-label="下一頁">→</button></footer>'
cover_art = {
    'preferences.html': '<div class="tiles"><b>E</b><b>I</b><b>S</b><b>N</b><b>T</b><b>F</b><b>J</b><b>P</b></div>',
    'types.html': '<div class="type-ticket"><b>INFP</b><b>ENFP</b></div>',
    'retest.html': '<div class="threshold-art"><b>49</b><i></i><b>51</b><span>I</span><span>E</span></div>',
    'big-five.html': '<div class="trait-art"><i></i><i></i><i></i><i></i><i></i></div>',
}
def render_slide(file, i, item):
    tag, heading, body, ids = item
    art = f'<div class="concept-art" aria-hidden="true">{cover_art[file]}</div>' if i == 1 else ''
    hidden = ' hidden' if i != 1 else ''
    mode = ' stage-cover' if art else ''
    return f'<section class="stage{mode}" id="p{i}"{hidden}><div class="slide-inner"><div class="slide-copy"><small>{tag}</small><h1 tabindex="-1">{heading}</h1>{body}</div>{art}</div>{refs(ids)}</section>'

mappings=[]
for file,title,description,items in decks:
    chapter_nav = '<nav class="lesson-nav" aria-label="本講義章節">' + ''.join(f'<a href="#p{i}">{i} · {tag}</a>' for i,(tag,_,_,_) in enumerate(items,1)) + '</nav>'
    sections = ''.join(render_slide(file,i,item) for i,item in enumerate(items,1))
    write(file,title,'<progress class="deck-progress" aria-label="講義進度"></progress>'+f'<p class="breadcrumb"><a href="index.html#catalog">← 分類講義</a> / <strong>{title}</strong></p><details class="deck-outline"><summary>本講義目錄</summary>{chapter_nav}</details><div class="slide-area">{sections}</div>'+footer,'<script src="lesson.js"></script>')
    mappings.append(f'<h3>{title}</h3><ul>'+''.join(f'<li><a href="{file}#p{i}">{tag}</a> · '+', '.join(f'S{n:02}' for n in ids)+'</li>' for i,(tag,_,_,ids) in enumerate(items,1))+'</ul>')
assert {i for _,_,_,items in decks for _,_,_,ids in items for i in ids} == set(range(1,6))
write('wiki.html','人格觀察簿 Wiki','<h1>五份資料，五張來源卡</h1>'+''.join(cards)+'<h2>講義對照</h2>'+''.join(mappings))
cases=[
('四字母一致率與分數信度相同','一致率','分數信度','分數信度','S03'),
('49／51 是官方 MBTI 計分','官方','示意','示意','S02、S04'),
('大五提供連續特質描述','連續特質','連續特質','連續特質','S05')]
rows=[]
for claim,draft,expected,revised,source in cases:
    assert revised==expected
    rows.append((claim,source,'通過' if draft==expected else '退回',revised))
    print(*rows[-1],sep=' | ')
flow='界定問題 → 收集五份資料 → 整理來源卡 → 逐頁查 Wiki → 核對主張與測量指標 → 生成逐頁講義 → 驗證連結與互動。'
reflection='本輪三個刻意設計的檢查案例中，兩個被退回。兩個都在「將來源轉成教學例句」時混淆了證據範圍。我把檢查前移到主張草擬之後、生成 HTML 之前。發現分類錯誤就回到來源卡，修正欄位和句子後重跑。新增來源時也會重新做原文定位與摘要。程式核對人工標記的概念類別，語句及來源意義另外逐筆審閱。'
table='<div class="scroll"><table><thead><tr><th>待審主張</th><th>依據</th><th>初檢</th><th>修正後類別</th></tr></thead><tbody>'+''.join('<tr>'+''.join(f'<td>{v}</td>' for v in row)+'</tr>' for row in rows)+'</tbody></table></div>'
write('workflow.html','製作紀錄','<h1>製作流程與檢查紀錄</h1><article class="sheet"><h2>Loop</h2><p>'+flow+'</p></article><article class="sheet"><h2>實際執行與反思</h2><p>'+reflection+'</p>'+table+'</article>')
Path('SUBMISSION.md').write_text('# 人格觀察簿｜同一個人，為什麼會測出兩種 MBTI？\n\n## 主題\n\n從四組偏好切入，介紹分類門檻、信度與效度、大五人格。先討論受眾和互動，再整理來源並製作。\n\n## 成果\n\n- [五篇來源 Wiki](dist/wiki.html)與[Markdown 索引](wiki/index.md)\n- [分類講義庫與四份獨立講義](dist/index.html)\n- [製作紀錄](dist/workflow.html)\n\n## Loop\n\n'+flow+'\n\n## 實際結果與反思\n\n'+reflection+'\n\n| 待審主張 | 依據 | 初檢 | 修正後類別 |\n|---|---|---|---|\n'+'\n'.join('| '+' | '.join(r)+' |' for r in rows)+'\n')

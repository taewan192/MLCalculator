import {useState} from 'react';
import {BookOpen, Castle, ChevronDown, Percent, Split, Swords, Users} from 'lucide-react';
import {Button} from '@/components/ui/button';
import skillTree from './assets/skill-tree-example.png?url';

type Translate = (key: string) => string;
type GuideField = [label: string, example: string, description: string];

function IllustratedSteps({title, fields, t}: {title: string; fields: GuideField[]; t: Translate}) {
 return (
  <div className="guide-steps">
   <div className="guide-diagram" role="img" aria-label={`${t(title)}. ${fields.map(([label, example], i) => `${i + 1}. ${t(label)}: ${example}`).join('. ')}`}>
    <strong>{t(title)}</strong>
    <div className="guide-diagram-fields">
     {fields.map(([label, example], index) => (
      <div className="guide-field" key={label}>
       <span className="guide-marker">{index + 1}</span>
       <span>{t(label)}<b>{example}</b></span>
      </div>
     ))}
    </div>
   </div>
   <ol className="guide-instructions">
    {fields.map(([label, , description], index) => (
     <li key={label}>
      <span className="guide-marker" aria-hidden="true">{index + 1}</span>
      <div><strong>{t(label)}</strong><p>{t(description)}</p></div>
     </li>
    ))}
   </ol>
  </div>
 );
}

const playerFields: GuideField[] = [
 ['장비 공격력 (%)', '171', 'guide.equipment'],
 ['레벨', '91', 'guide.playerLevel'],
 ['병력', '269G', 'guide.troops'],
];

export function UsageGuide({t}: {t: Translate}) {
 const [open, setOpen] = useState(false);
 return (
  <>
   <Button className="guide-toggle" variant="outline" type="button" aria-expanded={open} aria-controls="usage-guide" onClick={() => setOpen(previous => !previous)}>
    <BookOpen size={20}/><span>{t('guide.title')}</span><ChevronDown size={18}/>
   </Button>
   <div id="usage-guide" hidden={!open}>
    {open && <>
     <section className="card guide-card">
      <div className="card-heading"><span className="icon-box"><Swords size={20}/></span><h2>{t('Player Stats')}</h2></div>
      <p>{t('guide.playerIntro')}</p>
      <IllustratedSteps t={t} title="장비 + 레벨 + 병력" fields={playerFields}/>
      <p>{t('guide.playerResult')}</p>
      <h3><Split size={18}/>{t('skill.toggle')}</h3>
      <p>{t('guide.skillIntro')}</p>
      <figure className="guide-photo">
       <div className="guide-photo-frame">
        <img src={skillTree} alt={t('guide.skillPhoto')} width={620} height={352}/>
        <span className="guide-photo-highlight" aria-hidden="true"/>
       </div>
       <figcaption>{t('guide.skillPhoto')}</figcaption>
      </figure>
      <IllustratedSteps t={t} title="skill.heading" fields={[playerFields[0], ['skill.points', '184', 'guide.skillPoints'], playerFields[2]]}/>
      <p className="guide-example">{t('guide.skillExample')}</p>
     </section>
     <section className="card guide-card">
      <div className="card-heading"><span className="icon-box"><Castle size={20}/></span><h2>{t('도시 계산기')}</h2></div>
      <p>{t('guide.cityIntro')}</p>
      <IllustratedSteps t={t} title="목표 레벨 비용" fields={[
       ['도시 수', '1', 'guide.cityCount'], ['현재 도시 레벨', '1', 'guide.cityCurrent'], ['목표 도시 레벨', '130', 'guide.cityTarget'],
      ]}/>
      <p>{t('guide.cityResult')}</p>
      <IllustratedSteps t={t} title="보유 골드로 업그레이드" fields={[
       ['도시 수', '1', 'guide.cityCount'], ['현재 도시 레벨', '1', 'guide.cityCurrent'], ['보유 골드', '100 G', 'guide.cityGold'],
      ]}/>
     </section>
     <section className="card guide-card">
      <div className="card-heading"><span className="icon-box"><Users size={20}/></span><h2>{t('예상 모집')}</h2></div>
      <p>{t('guide.recruitIntro')}</p>
      <IllustratedSteps t={t} title="모집 정보" fields={[
       ['부대 생산량', '3G', 'guide.recruitProduction'], ['장비 모집 (%)', '360', 'guide.recruitGear'], ['레벨', '110', 'guide.recruitLevel'],
      ]}/>
      <p className="guide-example">{t('guide.recruitExample')}</p>
     </section>
     <section className="card guide-card">
      <div className="card-heading"><span className="icon-box"><Percent size={20}/></span><h2>{t('percentile.title')}</h2></div>
      <p>{t('guide.percentIntro')}</p>
      <IllustratedSteps t={t} title="percentile.title" fields={[
       ['percentile.rank', '250', 'guide.percentRank'], ['percentile.percent', '6.25', 'guide.percentInput'],
      ]}/>
      <p className="guide-example">{t('guide.percentExample')}</p>
      <p>{t('percentile.note')}</p>
     </section>
    </>}
   </div>
  </>
 );
}

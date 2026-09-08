import data from './calculator-data.json';
export const units:Record<string,number>={U:1,K:1e3,M:1e6,G:1e9,T:1e12,P:1e15};
export function power(s:string){const m=s.replaceAll(',','').trim().match(/^(\d+(?:\.\d+)?)\s*([mMgGtTpPㅁㄱㅎㅌㅍ])$/);if(!m)throw Error('공격력 또는 병력은 예: 55G, 42.2T, 1.5P 처럼 입력하세요.');const aliases:Record<string,string>={'ㅁ':'M','ㄱ':'G','ㅎ':'G','ㅌ':'T','ㅍ':'P'};const n=Number(m[1])*units[aliases[m[2]]||m[2].toUpperCase()];if(!Number.isFinite(n))throw Error('유효한 숫자를 입력하세요.');return n;}
export function number(s:string,min=0,integer=false){if(!s.trim())throw Error('유효한 숫자를 입력하세요.');const n=Number(s.replaceAll(',','').replace('%',''));if(!Number.isFinite(n)||n<min||(integer&&!Number.isInteger(n)))throw Error('유효한 숫자를 입력하세요.');return n;}
export function target(p:number){let level:number|null=null;for(const [l,s] of data.levels){if(p>=power(String(s)))level=Number(l);else break;}return level;}
export function formatUnit(n:number){n=Math.floor(n);let suffix='',v=n;for(const u of ['T','G','M','K'])if(n>=units[u]){suffix=u;v=n/units[u];break;}v=v>=100?Math.round(v):v>=10?Math.round(v*10)/10:Math.round(v*100)/100;return String(v)+suffix;}
export function city(c:number,start:number,targetLevel:number,gold?:number){const wall=70*1.2**(targetLevel-1),cost=c*(50*(1.2**(targetLevel-1)-1.2**(start-1))),vp=20*1.115**(targetLevel-1),won=c*(20*1.115**(targetLevel-1)-20*1.115**(start-1));if(![wall,cost,vp,won].every(Number.isFinite)||cost<0||gold!==undefined&&gold-cost<0)throw Error('입력값으로 계산할 수 없습니다. 레벨과 골드를 확인하세요.');return {'도달 도시 레벨':String(targetLevel),'총 필요 골드 / 사용 골드':formatUnit(cost),'남은 골드':gold===undefined?'—':formatUnit(gold-cost),'도시당 성벽':formatUnit(wall),'도시당 승점':formatUnit(vp),'총 획득 승점':formatUnit(won)};}
export function upgrade(c:number,start:number,gold:number){const level=Math.floor(Math.log(gold/(c*10/0.2)+1.2**(start-1))/Math.log(1.2)+1);return city(c,start,level,gold);}

export function attack(troops:number,equipment:number,level:number,league:string){
 return checked(troops*(100+equipment+(level-1)*(league==='platinum'?2:4))/100);
}
function checked(n:number){if(!Number.isFinite(n)||n<0)throw Error('유효한 숫자를 입력하세요.');return n;}
export function recruitment(production:number,equipment:number,level:number,league:string){
 const percent=equipment+(level-1)*(league==='platinum'?3:6);
 return {percent:checked(percent),amount:checked(production*percent/100)};
}
export function formatAmount(n:number,decimals=2){
 checked(n);const unit=['P','T','G','M','K'].find(u=>n>=units[u]);
 return String(Number((unit?n/units[unit]:n).toFixed(decimals)))+(unit||'');
}

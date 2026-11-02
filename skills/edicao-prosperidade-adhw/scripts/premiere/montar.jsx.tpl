var P=__PLANO__;var seq=null;
for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==P.seq)seq=app.project.sequences[i];
if(!seq)return {erro:"seq"};app.project.activeSequence=seq;
var cache={};
function achar(bin,nm){var key=bin+"|"+nm;if(cache[key])return cache[key];var r=app.project.rootItem;var p=bin.split('/');for(var i=0;i<p.length;i++){var f=null;for(var j=0;j<r.children.numItems;j++)if(String(r.children[j].name)==p[i]){f=r.children[j];break;}if(!f)return null;r=f;}
for(var j=0;j<r.children.numItems;j++)if(String(r.children[j].name)==nm){cache[key]=r.children[j];return r.children[j];}return null;}
function comp(clip,mn){for(var i=0;i<clip.components.numItems;i++)if(String(clip.components[i].matchName)==mn)return clip.components[i];return null;}
var log=[],ok=0;
function por(lista,video){
 for(var n=0;n<lista.length;n++){var x=lista[n];var it=achar(x.bin,x.nm);if(!it){log.push("SEM ITEM "+x.nm);continue;}
  it.setInPoint(x["in"],4);it.setOutPoint(x["in"]+x.dur,4);
  var t=new Time();t.seconds=x.t;var tr=video?seq.videoTracks[x.tr]:seq.audioTracks[x.tr];
  tr.overwriteClip(it,t);it.clearInPoint(4);it.clearOutPoint(4);
  tr=video?seq.videoTracks[x.tr]:seq.audioTracks[x.tr];var c=null;
  for(var j=0;j<tr.clips.numItems;j++){if(Math.abs(tr.clips[j].start.seconds-x.t)<0.05){c=tr.clips[j];}}
  if(!c){log.push("NAO ACHEI "+x.nm+" @"+x.t);continue;}
  if(video&&x["in"]>1&&x.nm.indexOf("AVATAR")>=0){var fr=Math.round(x["in"]*25);var ti=new Time();ti.ticks=String(fr*10160640000);c.inPoint=ti;var te=new Time();te.ticks=String((Math.round(x.t*25)+Math.round(x.dur*25))*10160640000);c.end=te;}
  if(video){var mo=comp(c,"AE.ADBE Motion");
   if(mo){var sc=mo.properties[1];
    if(x.kb){sc.setTimeVarying(true);var k0=new Time();k0.seconds=c.inPoint.seconds;var k1=new Time();k1.seconds=c.inPoint.seconds+x.dur;sc.addKey(k0);sc.setValueAtKey(k0,x.kb[0],true);sc.addKey(k1);sc.setValueAtKey(k1,x.kb[1],true);}
    else if(x.sc){sc.setValue(x.sc,true);}
    if(x.pop){sc.setTimeVarying(true);var b0=c.inPoint.seconds;var ts=[b0,b0+0.16,b0+0.28];for(var q=0;q<3;q++){var kt=new Time();kt.seconds=ts[q];sc.addKey(kt);sc.setValueAtKey(kt,x.pop[q],true);}}
    if(x.pos)mo.properties[0].setValue(x.pos,true);}
   if(x.blend){var op=comp(c,"AE.ADBE Opacity");if(op)op.properties[1].setValue(x.blend,true);}}
  ok++;}
}
if(__FASE__=="V")por(P.V,true);else por(P.A,false);
return {seq:P.seq,fase:__FASE__,ok:ok,log:log.slice(0,15),v2:seq.videoTracks[1].clips.numItems,v3:seq.videoTracks[2].clips.numItems,a3:seq.audioTracks[2].clips.numItems,a4:seq.audioTracks[3].clips.numItems,a2:seq.audioTracks[1].clips.numItems,v1:seq.videoTracks[0].clips.numItems};

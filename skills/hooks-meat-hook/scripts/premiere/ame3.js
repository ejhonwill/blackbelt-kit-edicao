var p=app.project, E="/Users/jhonwill/Movies/128PG_EXPORT", PRESET="/Applications/Adobe Media Encoder 2026/Adobe Media Encoder 2026.app/Contents/MediaIO/systempresets/4E49434B_48323634/01 - Match Source - High bitrate.epr";
var DONE={"128_PG AD01 HK1":1,"128_PG AD01 HK2":1,"128_PG AD01 HK3":1,"128_PG AD01 HK4":1,"128_PG AD01 HK5":1,"128_PG AD01 HK10":1};
app.encoder.launchEncoder();
var names=[]; for(var i=0;i<p.sequences.numSequences;i++){ var nm=p.sequences[i].name; if(nm.match(/^128_PG AD\d\d HK\d+$/) && !DONE[nm]) names.push(nm); }
names.sort(); var q=[];
for(var n=0;n<names.length;n++){ var s=null; for(var i=0;i<p.sequences.numSequences;i++) if(p.sequences[i].name==names[n]) s=p.sequences[i];
  var m=s.name.match(/^128_PG (AD\d\d) HK(\d+)$/);
  app.encoder.encodeSequence(s, E+"/"+m[1]+"/[230926][OT] 128_PG "+m[1]+" HK"+m[2]+" [CardioFlush] [Squad].mp4", PRESET, 0, 1); q.push(names[n]); }
app.encoder.startBatch();
return q.length+" na fila: "+q.join(", ");

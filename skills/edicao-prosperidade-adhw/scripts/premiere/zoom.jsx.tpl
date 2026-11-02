var N=__SEQ__,Z=__Z__;var seq=null;for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==N)seq=app.project.sequences[i];
app.project.activeSequence=seq;var c=seq.videoTracks[0].clips[0];var mo=null;
for(var i=0;i<c.components.numItems;i++)if(String(c.components[i].matchName)=="AE.ADBE Motion")mo=c.components[i];
var sc=mo.properties[1];sc.setTimeVarying(false);sc.setValue(100,true);sc.setTimeVarying(true);var n=0;
for(var i=0;i<Z.length;i++){var a=new Time();a.seconds=Z[i][0]+0.02;var b=new Time();b.seconds=Z[i][1]-0.02;sc.addKey(a);sc.setValueAtKey(a,Z[i][2],true);sc.addKey(b);sc.setValueAtKey(b,Z[i][3],true);n+=2;}
return {seq:N,keys:sc.getKeys().length,esperado:n};

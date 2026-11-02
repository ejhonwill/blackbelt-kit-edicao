var N=__SEQ__;var seq=null;for(var i=0;i<app.project.sequences.numSequences;i++)if(String(app.project.sequences[i].name)==N)seq=app.project.sequences[i];
if(!seq)return {erro:"seq"};app.project.activeSequence=seq;
var vt=[1],at=[2,3];for(var a=0;a<vt.length;a++){var tr=seq.videoTracks[vt[a]];for(var c=tr.clips.numItems-1;c>=0;c--)tr.clips[c].remove(false,false);}
for(var a=0;a<at.length;a++){var tr=seq.audioTracks[at[a]];for(var c=tr.clips.numItems-1;c>=0;c--)tr.clips[c].remove(false,false);}
return {seq:N,v1:seq.videoTracks[0].clips.numItems,v2:seq.videoTracks[1].clips.numItems,v3:seq.videoTracks[2].clips.numItems,a2:seq.audioTracks[1].clips.numItems,a3:seq.audioTracks[2].clips.numItems,a4:seq.audioTracks[3].clips.numItems};

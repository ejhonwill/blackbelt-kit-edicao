var seq=app.project.activeSequence;var tr=seq.videoTracks[1];var n=0,log=[];
for(var j=0;j<tr.clips.numItems-1;j++){var a=tr.clips[j],b=tr.clips[j+1];var g=b.start.seconds-a.end.seconds;
 if(g>0.001&&g<0.6){var e=new Time();e.ticks=String(b.start.ticks);a.end=e;n++;log.push(Math.round(a.start.seconds*100)/100);}}
var tr2=seq.videoTracks[1];var rest=[];for(var j=0;j<tr2.clips.numItems-1;j++){var g=tr2.clips[j+1].start.seconds-tr2.clips[j].end.seconds;if(g>0.001&&g<0.6)rest.push(g);}
return {seq:String(seq.name),fechados:n,em:log,restantes:rest.length};

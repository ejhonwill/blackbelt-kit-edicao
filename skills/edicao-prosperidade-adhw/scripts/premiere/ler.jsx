var seq=app.project.activeSequence;var o={seq:String(seq.name),v2:[],v3:[]};
function comp(clip,mn){for(var i=0;i<clip.components.numItems;i++)if(String(clip.components[i].matchName)==mn)return clip.components[i];return null;}
for(var t=1;t<3;t++){var tr=seq.videoTracks[t];for(var j=0;j<tr.clips.numItems;j++){var c=tr.clips[j];var mo=comp(c,"AE.ADBE Motion");var sc=mo.properties[1];var kv=null;
 if(sc.isTimeVarying()){var ks=sc.getKeys();kv=[];for(var q=0;q<ks.length;q++)kv.push([Math.round(ks[q].seconds*100)/100,Math.round(sc.getValueAtKey(ks[q])*10)/10]);}
 var op=comp(c,"AE.ADBE Opacity");
 o[t==1?"v2":"v3"].push([String(c.name).substr(0,18),Math.round(c.start.seconds*100)/100,Math.round(c.end.seconds*100)/100,Math.round(c.inPoint.seconds*100)/100,kv?kv:Math.round(sc.getValue()*10)/10,op?op.properties[1].getValue():null]);}}
return o;

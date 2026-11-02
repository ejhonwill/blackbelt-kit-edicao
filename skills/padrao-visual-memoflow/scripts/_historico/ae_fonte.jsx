(function(){
 var out=[]; var p=app.project;
 for(var i=1;i<=p.numItems;i++){
   var x=p.item(i);
   if(!(x instanceof FootageItem)) continue;
   if(x.name.indexOf("DR 0")!==0) continue;
   var s=x.name+" | dur="+x.duration.toFixed(3)+" | fps="+(x.frameRate||0).toFixed(3);
   try{ s+=" | conform="+x.mainSource.conformFrameRate; }catch(e){}
   try{ s+=" | arquivo="+x.mainSource.file.fsName; }catch(e){ s+=" | sem arquivo"; }
   out.push(s);
 }
 // audio na comp?
 function comp(n){for(var j=1;j<=p.numItems;j++){var z=p.item(j);if(z instanceof CompItem&&z.name===n)return z;}return null;}
 var C=comp("DR 01 ABERTURA");
 for(var k=1;k<=C.numLayers;k++){
   var Lz=C.layer(k);
   if(Lz.name!=="VIDEO") continue;
   out.push("VIDEO: start="+Lz.startTime.toFixed(3)+" in="+Lz.inPoint.toFixed(3)+" out="+Lz.outPoint.toFixed(3)+" audio="+Lz.audioEnabled);
   try{ out.push("  esticamento="+Lz.stretch); }catch(e){}
 }
 out.push("comp fps="+C.frameRate+" dur="+C.duration.toFixed(3));
 var f=new File("/tmp/ae_fonte.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();

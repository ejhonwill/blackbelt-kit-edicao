(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var M=[["02_DEPOIMENTO_MARK_LIPSYNC.mp4","DEP 02 MARK"],["03_DEPOIMENTO_ELAINE_LIPSYNC.mp4","DEP 03 ELAINE"],
         ["04_DEPOIMENTO_ROBERT_LIPSYNC.mp4","DEP 04 ROBERT"],["06_DEPOIMENTO_MARGARET_LIPSYNC.mp4","DEP 06 MARGARET"],
         ["09_DEPOIMENTO_NANCY_LIPSYNC.mp4","DEP 09 NANCY"],["10_DEPOIMENTO_GEORGE_LIPSYNC.mp4","DEP 10 GEORGE"]];
  for(var k=0;k<M.length;k++){
    var it=null;
    for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof FootageItem && x.name===M[k][0]) it=x; }
    if(!it){ out.push(M[k][0]+": fonte nao achada"); continue; }
    var antes=it.duration; it.mainSource.reload();
    var C=comp(M[k][1]); if(!C){ out.push(M[k][1]+": comp nao achada"); continue; }
    C.duration=it.duration;
    for(var l=1;l<=C.numLayers;l++){ var L=C.layer(l); if(L.name==="VIDEO"){ L.outPoint=it.duration; } }
    out.push(M[k][1]+": "+antes.toFixed(2)+" -> "+it.duration.toFixed(2)+"s");
  }
  app.project.save();
  var f=new File("/tmp/ae_depreload.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_depreload.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();

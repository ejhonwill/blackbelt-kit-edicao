(function(){
 try{
  var out=[]; var p=app.project;
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  // o Whisper grudou "Hello," no zero e esticou a frase ate 4,74;
  // no audio ela vai de 0,67 a 4,71. Remapeia a primeira frase para o tempo medido.
  var A0=0.00, A1=4.74, M0=0.67, M1=4.71;
  var k=(M1-M0)/(A1-A0);
  function mapa(t){ return M0 + t*k; }
  var n=0, det=[];
  for(var i=1;i<=C.numLayers;i++){
    var L=C.layer(i), nm=L.name;
    if(nm.indexOf("LEG ")!==0 && nm.indexOf("PIL ")!==0) continue;
    var ii=L.inPoint, oo=L.outPoint;
    if(oo>A1+0.10) continue;                       // so a primeira frase
    var ni=mapa(ii), no=mapa(oo);
    L.startTime=L.startTime+(ni-ii);
    L.inPoint=ni; L.outPoint=no;
    n++;
    if(nm.indexOf("LEG ")===0) det.push(nm+" "+ii.toFixed(2)+"->"+ni.toFixed(2));
  }
  // "Before" comeca em 5,13 no audio, nao 5,22
  for(var j=1;j<=C.numLayers;j++){
    var L2=C.layer(j), n2=L2.name;
    if(n2.indexOf("LEG ")!==0 && n2.indexOf("PIL ")!==0) continue;
    if(Math.abs(L2.inPoint-5.22)<0.03){ L2.startTime=L2.startTime-0.09; L2.inPoint=5.13; }
  }
  out.push("legendas da primeira frase reposicionadas="+n+" (fator "+k.toFixed(3)+", deslocamento inicial +0,67s)");
  out.push(det.join(" | "));
  app.project.save();
  var f=new File("/tmp/ae_lsync.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_lsync.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();

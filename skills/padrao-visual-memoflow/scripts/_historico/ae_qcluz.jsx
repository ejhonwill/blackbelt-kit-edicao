(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var C=comp("DR 01 ABERTURA");
  var T=[4.80,5.60,22.20,22.36,22.52,29.20,29.40,30.60,31.85,51.40,51.70,52.60];
  for(var i=0;i<T.length;i++) C.saveFrameToPng(T[i], new File("/tmp/lz_"+(100+i)+".png"));
  var f=new File("/tmp/ae_qcl.txt"); f.open("w"); f.write("ok "+T.length+" motionBlur="+C.motionBlur+" camadas="+C.numLayers); f.close();
 }catch(e){ var g=new File("/tmp/ae_qcl.txt"); g.open("w"); g.write("ERRO "+e.toString()); g.close(); }
})();

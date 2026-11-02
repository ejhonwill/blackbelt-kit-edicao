(function(){
  var p=app.project; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  var T=[2.0, 11.0, 17.5, 21.3, 23.2, 26.5, 28.5, 30.2, 34.0, 36.0, 40.2, 43.0, 46.5, 49.3, 52.0, 54.0, 58.0, 60.2, 63.5, 65.2, 67.3, 70.5, 72.5];
  var out=[];
  for(var k=0;k<T.length;k++){
    try{ C.saveFrameToPng(T[k], new File("/tmp/ab_"+(k<10?"0":"")+k+".png")); out.push(T[k]); }
    catch(e){ out.push("x"+T[k]); }
  }
  var f=new File("/tmp/ae_ab.txt"); f.open("w"); f.write(out.join(" ")); f.close();
})();

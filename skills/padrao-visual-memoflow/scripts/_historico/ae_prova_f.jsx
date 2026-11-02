(function(){
  var p=app.project; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  if(!C) return;
  var T=[1.5, 6.5, 12.0, 18.0, 20.3, 23.5, 26.8, 30.5, 34.2, 40.3, 46.0, 51.0, 54.5, 58.5, 62.0, 67.5, 71.0, 74.5];
  for(var k=0;k<T.length;k++){ try{ C.saveFrameToPng(T[k], new File("/tmp/f_"+(k<10?"0":"")+k+".png")); }catch(e){} }
  var f=new File("/tmp/ae_pf.txt"); f.open("w"); f.write("ok "+T.length); f.close();
})();

(function(){
  var p=app.project; var out=[]; var C=null;
  for(var i=1;i<=p.numItems;i++){ var x=p.item(i); if(x instanceof CompItem && x.name==="DR 01 ABERTURA") C=x; }
  out.push("antes: "+C.renderer+" | disponiveis: "+C.renderers.join(", "));
  try{ C.renderer="ADBE Standard 3d"; out.push("depois: "+C.renderer); }
  catch(e){ out.push("falhou trocar: "+e.toString()); }
  C.saveFrameToPng(18.2, new File("/tmp/rend_a.png"));
  C.saveFrameToPng(23.5, new File("/tmp/rend_b.png"));
  var f=new File("/tmp/ae_rend.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();

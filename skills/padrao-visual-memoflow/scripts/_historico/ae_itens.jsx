(function(){
 var out=[]; var p=app.project;
 for(var i=1;i<=p.numItems;i++){
   var x=p.item(i);
   var t=(x instanceof CompItem)?"COMP":((x instanceof FolderItem)?"pasta":"midia");
   if(t==="pasta") continue;
   var s=i+" ["+t+"] "+x.name;
   try{ s+=" "+x.width+"x"+x.height; }catch(e){}
   try{ if(x.duration) s+=" dur="+x.duration.toFixed(2); }catch(e){}
   try{ if(x instanceof CompItem) s+=" camadas="+x.numLayers; }catch(e){}
   try{ if(x.parentFolder) s+=" em:"+x.parentFolder.name; }catch(e){}
   out.push(s);
 }
 var f=new File("/tmp/ae_itens.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
})();

(function(){
 try{
  var p=app.project; var out=[]; var n=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c); if(!(cc instanceof CompItem)) continue;
    for(var i=1;i<=cc.numLayers;i++){
      var L=cc.layer(i); if(!(L instanceof CameraLayer)) continue;
      var T=L.property("Transform");
      var z=T.property("Position").value[2];
      try{ T.property("Point of Interest").setValue([cc.width/2, cc.height/2, 0]); }catch(e0){}
      T.property("Position").setValue([cc.width/2, cc.height/2, z]);
      T.property("Anchor Point").setValue([0,0,0]);
      out.push(cc.name+"/"+L.name+" -> pos=["+(cc.width/2)+","+(cc.height/2)+","+z.toFixed(0)+"]");
      n++;
    }
  }
  out.unshift("cameras corrigidas="+n);
  app.project.save();
  var f=new File("/tmp/ae_cam.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_cam.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();

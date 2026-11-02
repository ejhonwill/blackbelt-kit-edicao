(function(){
 try{
  var p=app.project; var out=[]; var n=0;
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c); if(!(cc instanceof CompItem)) continue;
    for(var i=1;i<=cc.numLayers;i++){
      var L=cc.layer(i); if(!(L instanceof CameraLayer)) continue;
      var T=L.property("Transform");
      var z=T.property("Position").value[2];
      // em camera o ponto de ancoragem E o ponto de interesse
      T.property("Anchor Point").setValue([cc.width/2, cc.height/2, 0]);
      T.property("Position").setValue([cc.width/2, cc.height/2, z]);
      T.property("Orientation").setValue([0,0,0]);
      T.property("X Rotation").setValue(0); T.property("Y Rotation").setValue(0); T.property("Rotation").setValue(0);
      out.push(cc.name+" cam POI=["+(cc.width/2)+","+(cc.height/2)+",0] pos=["+(cc.width/2)+","+(cc.height/2)+","+z.toFixed(0)+"]");
      n++;
    }
  }
  out.unshift("cameras="+n);
  app.project.save();
  var f=new File("/tmp/ae_cam2.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_cam2.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();

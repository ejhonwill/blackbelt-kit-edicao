(function(){
  var out=[]; var p=app.project;
  var C=p.items.addComp("PROBE",200,200,1,1,25);
  var s=C.layers.addSolid([0.5,0.5,0.5],"s",200,200,1);
  var tn=s.property("Effects").addProperty("ADBE AIF Perlin Noise 3D");
  out.push("Ruido turbulento: "+tn.numProperties+" props");
  for(var i=1;i<=tn.numProperties;i++){
    var pr=tn.property(i); var tipo=(pr.numProperties!==undefined&&pr.numProperties>0)?"GRUPO":"";
    out.push("  "+i+": "+pr.name+" "+tipo);
    if(tipo==="GRUPO"){ for(var j=1;j<=pr.numProperties;j++) out.push("     "+i+"."+j+": "+pr.property(j).name); }
  }
  var tri=s.property("Effects").addProperty("ADBE Tritone");
  out.push("Tritone: "+tri.numProperties+" props");
  for(var k=1;k<=tri.numProperties;k++) out.push("  "+k+": "+tri.property(k).name);
  var bb=s.property("Effects").addProperty("ADBE Box Blur2");
  out.push("Box blur: "+bb.numProperties+" props");
  for(var b=1;b<=bb.numProperties;b++) out.push("  "+b+": "+bb.property(b).name);
  var rp=s.property("Effects").addProperty("ADBE Ramp");
  out.push("Ramp: "+rp.numProperties+" props");
  for(var r=1;r<=rp.numProperties;r++) out.push("  "+r+": "+rp.property(r).name);
  C.remove();
  var f=new File("/tmp/ae_probe.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();

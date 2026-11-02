(function(){
 try{
  var p=app.project; var out=[];
  var C=p.items.addComp("__glow",1080,540,1,2,25); C.bgColor=[0,0,0];
  C.layers.addSolid([0.02,0.02,0.04],"BG",1080,540,1);
  function txt(s,x,fonte,cor){
    var t=C.layers.addText(s);
    var d=t.property("Source Text").value;
    d.fontSize=76; d.font=fonte; d.applyFill=true; d.fillColor=cor; d.applyStroke=false; d.tracking=-10;
    t.property("Source Text").setValue(d);
    t.property("Transform").property("Position").setValue([x,300]);
    return t;
  }
  // 1: Deep Glow 2
  var a=txt("MEMOFLOW",40,"Montserrat-ExtraBold",[1,0.42,0.16]);
  var dg=a.property("Effects").addProperty("PEDG2");
  try{ dg.property(24).setValue(60); dg.property(25).setValue(1.6); }catch(e){ out.push("dg props: "+e.toString()); }
  // 2: Glo2 empilhado
  var b=txt("MEMOFLOW",560,"Montserrat-ExtraBold",[1,0.42,0.16]);
  var g1=b.property("Effects").addProperty("ADBE Glo2");
  var g2=b.property("Effects").addProperty("ADBE Glo2");
  try{ g1.property(3).setValue(14); g1.property(4).setValue(1.4);
       g2.property(3).setValue(90); g2.property(4).setValue(1.1); }catch(e2){ out.push("glo2: "+e2.toString()); }
  C.saveFrameToPng(1, new File("/tmp/glow.png"));
  out.push("fonte lida: "+a.property("Source Text").value.font);
  C.remove();
  var f=new File("/tmp/ae_glow.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))||"ok"); f.close();
 }catch(err){ var fe=new File("/tmp/ae_glow.txt"); fe.open("w"); fe.write("ERRO "+err.toString()); fe.close(); }
})();

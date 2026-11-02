(function(){
 try{
  var out=[]; var p=app.project;
  var nc=0, nt=0, det=[];
  for(var c=1;c<=p.numItems;c++){
    var cc=p.item(c);
    if(!(cc instanceof CompItem) || cc.name.indexOf("CARD ")!==0) continue;
    var tm=cc.duration-0.05;          // animador ja resolvido: a medida vale
    var linhas={};
    for(var t=1;t<=cc.numLayers;t++){
      var L=cc.layer(t); if(L.name.indexOf("TXT ")!==0) continue;
      var li=L.name.split(" ")[1].split(".")[0];
      var r=L.sourceRectAtTime(tm,false);
      var pos=L.property("Transform").property("Position");
      var v=pos.value;                                  // local, ja pendurado no CTRL
      var e=540+v[0]+r.left, d=e+r.width;
      if(!linhas[li]) linhas[li]={e:e,d:d,ls:[]};
      linhas[li].e=Math.min(linhas[li].e,e); linhas[li].d=Math.max(linhas[li].d,d);
      linhas[li].ls.push(L);
    }
    var pior=0;
    for(var li2 in linhas){
      var ln=linhas[li2], erro=(ln.e+ln.d)/2-540;
      if(Math.abs(erro)>Math.abs(pior)) pior=erro;
      for(var z=0;z<ln.ls.length;z++){
        var P=ln.ls[z].property("Transform").property("Position");
        var vv=P.value; P.setValue([vv[0]-erro, vv[1], vv[2]]);
        nt++;
      }
    }
    det.push(cc.name+" corrigiu "+Math.round(pior)+"px");
    nc++;
  }
  out.push("titulos="+nc+" camadas="+nt);
  out.push(det.join(" | "));
  app.project.save();
  var f=new File("/tmp/ae_ctr2.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_ctr2.txt"); fe.open("w"); fe.write("ERRO "+e.toString()+" linha "+e.line); fe.close(); }
})();

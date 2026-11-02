(function(){
 try{
  var out=[]; var p=app.project; var LIM=980;
  var nomes=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT","DR 05 MECANISMO",
             "DEP 06 MARGARET","DR 07 OFERTA","DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var n=0;
  for(var k=0;k<nomes.length;k++){
    var C=comp(nomes[k]); if(!C) continue;
    for(var i=1;i<=C.numLayers;i++){
      var L=C.layer(i); if(L.name.indexOf("LEG ")!==0) continue;
      var t=L.inPoint+0.05;
      var r=L.sourceRectAtTime(t,false);
      if(r.width+56<=LIM) continue;
      // encolhe so o que nao cabe, ate entrar na margem
      var td=L.property("Source Text").value, corpo=td.fontSize;
      while(corpo>38 && r.width+56>LIM){
        corpo-=2; td=L.property("Source Text").value; td.fontSize=corpo;
        L.property("Source Text").setValue(td);
        r=L.sourceRectAtTime(t,false);
      }
      // a pilula tem de acompanhar o novo corpo
      var num=L.name.split(" ")[1];
      for(var q=1;q<=C.numLayers;q++){
        var P=C.layer(q); if(P.name!=="PIL "+num) continue;
        var g=P.property("Contents").property(1).property("Contents");
        for(var f=1;f<=g.numProperties;f++){
          var pr=g.property(f);
          if(pr.matchName==="ADBE Vector Shape - Rect"){
            pr.property("ADBE Vector Rect Size").setValue([r.width+56, r.height+34]);
            pr.property("ADBE Vector Rect Roundness").setValue((r.height+34)/2);
          }
        }
        P.property("Transform").property("Position").setValue([540, 952-r.height/2-2]);
      }
      out.push("  "+nomes[k]+" "+L.name+": corpo -> "+corpo+"px, largura "+Math.round(r.width+56)+"px");
      n++;
    }
  }
  out.unshift("legendas ajustadas="+n);
  app.project.save();
  var fo=new File("/tmp/ae_fit.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(e){ var fe=new File("/tmp/ae_fit.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();

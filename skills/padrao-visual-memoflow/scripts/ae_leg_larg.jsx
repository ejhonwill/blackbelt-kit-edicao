(function(){
 try{
  var out=[]; var p=app.project; var LIM=980;   // largura util com margem
  var nomes=["DR 01 ABERTURA","DEP 02 MARK","DEP 03 ELAINE","DEP 04 ROBERT","DR 05 MECANISMO",
             "DEP 06 MARGARET","DR 07 OFERTA","DEP 08 FRANK","DEP 09 NANCY","DEP 10 GEORGE"];
  function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var total=0, estouro=0;
  for(var k=0;k<nomes.length;k++){
    var C=comp(nomes[k]); if(!C) continue;
    var n=0;
    for(var i=1;i<=C.numLayers;i++){
      var L=C.layer(i); if(L.name.indexOf("LEG ")!==0) continue;
      total++;
      var r=L.sourceRectAtTime(L.inPoint+0.05,false);
      var larg=r.width+56;                       // pilula = texto + folga
      if(larg>LIM){
        estouro++; n++;
        if(n<=3){ var t=""; try{ t=L.property("Source Text").value.text; }catch(e){}
          out.push("  "+nomes[k]+" "+L.name+"  "+Math.round(larg)+"px  \""+t.substring(0,42)+"\""); }
      }
    }
    if(n>3) out.push("  ... e mais "+(n-3)+" em "+nomes[k]);
  }
  out.unshift("legendas="+total+" | estouram "+LIM+"px: "+estouro);
  var f=new File("/tmp/ae_larg.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))); f.close();
 }catch(e){ var fe=new File("/tmp/ae_larg.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();

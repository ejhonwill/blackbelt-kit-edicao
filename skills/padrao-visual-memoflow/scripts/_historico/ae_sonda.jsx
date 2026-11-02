(function(){
 try{
  var out=[]; var g=[];
  // efeitos de brilho disponiveis
  for(var i=0;i<app.effects.length;i++){
    var e=app.effects[i];
    var n=e.displayName.toLowerCase(), m=e.matchName.toLowerCase();
    if(n.indexOf("glow")>=0||n.indexOf("brilho")>=0||m.indexOf("glow")>=0||m.indexOf("deep")>=0)
      g.push(e.displayName+" = "+e.matchName);
  }
  out.push("BRILHOS:"); out=out.concat(g);
  // fontes pesadas
  var f=[];
  try{
    var lst=app.fonts.allFonts;
    for(var j=0;j<lst.length;j++){
      var pn=lst[j].postScriptName;
      if(/Helvetica|Inter|Montserrat|Poppins|Archivo|Anton|Impact|Roboto/i.test(pn) && /Black|Heavy|Bold|Extra|Impact|Anton/i.test(pn)) f.push(pn);
    }
  }catch(e1){ out.push("fonts api: "+e1.toString()); }
  out.push("FONTES ("+f.length+"): "+f.slice(0,40).join(", "));
  var fo=new File("/tmp/ae_sonda.txt"); fo.open("w"); fo.write(out.join(String.fromCharCode(10))); fo.close();
 }catch(err){ var fe=new File("/tmp/ae_sonda.txt"); fe.open("w"); fe.write("ERRO "+err.toString()); fe.close(); }
})();

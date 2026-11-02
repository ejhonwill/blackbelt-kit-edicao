(function(){
  var out=[]; var fx=app.effects;
  out.push("total de efeitos="+fx.length);
  var alvo=["noise","turb","fractal","ruido","ruído","tritone","tom","blur","desfoque","ramp","degrade","degradê","gradient"];
  for(var i=0;i<fx.length;i++){
    var d=(fx[i].displayName||"").toLowerCase(); var m=fx[i].matchName;
    for(var a=0;a<alvo.length;a++){
      if(d.indexOf(alvo[a])>=0){ out.push(fx[i].displayName+"  ->  "+m); break; }
    }
  }
  var f=new File("/tmp/ae_fx.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();

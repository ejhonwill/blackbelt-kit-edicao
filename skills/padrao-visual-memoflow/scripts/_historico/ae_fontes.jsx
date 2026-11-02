(function(){
  var out=[];
  try{
    var fs=app.fonts; out.push("familias="+fs.families.length);
    var alvo=["Helvetica","Inter","Jost","Arial","Archivo","Montserrat","Poppins","Roboto","SF Pro","Avenir"];
    for(var a=0;a<alvo.length;a++){
      for(var i=0;i<fs.families.length;i++){
        if(fs.families[i].familyName.indexOf(alvo[a])===0){
          var fam=fs.families[i]; var estilos=[];
          for(var j=0;j<fam.fonts.length;j++) estilos.push(fam.fonts[j].postScriptName);
          out.push(fam.familyName+" -> "+estilos.slice(0,6).join(", "));
          break;
        }
      }
    }
  }catch(e){ out.push("app.fonts falhou: "+e.toString()); }
  var f=new File("/tmp/ae_fontes.txt"); f.open("w"); f.write(out.join("\n")); f.close();
})();

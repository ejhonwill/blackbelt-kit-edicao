(function(){
 var p=app.project; var C=null;
 for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name==="DR 01 ABERTURA")C=x;}
 var s=0,b=0,c=0,pr=0,lg=0;
 for(var k=1;k<=C.numLayers;k++){var n=C.layer(k).name;
   if(n.indexOf("SFX ")===0)s++; else if(n.indexOf("BR ")===0)b++;
   else if(n.indexOf("CARD ")===0)c++; else if(n.indexOf("PROD")===0)pr++;
   else if(n.indexOf("LEG ")===0)lg++; }
 p.save();
 var f=new File("/tmp/ae_fim.txt"); f.open("w");
 f.write("sfx="+s+" broll="+b+" cartelas="+c+" produto="+pr+" legendas="+lg+" total="+C.numLayers+" motionBlur="+C.motionBlur+" salvo=ok");
 f.close();
})();

(function(){
 var out=[];
 for(var i=0;i<app.effects.length;i++){
   var e=app.effects[i];
   if(/artlist|\bAB\b|apple/i.test(e.matchName)||/apple/i.test(e.displayName)) out.push(e.displayName+" = "+e.matchName);
 }
 var f=new File("/tmp/ae_ab.txt"); f.open("w"); f.write(out.join(String.fromCharCode(10))||"nenhum"); f.close();
})();

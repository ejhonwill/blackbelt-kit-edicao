(function(){
 try{
  var p=app.project; function comp(n){for(var i=1;i<=p.numItems;i++){var x=p.item(i);if(x instanceof CompItem&&x.name===n)return x;}return null;}
  var D=[["DEP 02 MARK",9.0],["DEP 03 ELAINE",9.0],["DEP 04 ROBERT",11.0],["DEP 06 MARGARET",8.0],
         ["DEP 08 FRANK",11.0],["DEP 09 NANCY",14.0],["DEP 10 GEORGE",16.0]];
  for(var i=0;i<D.length;i++){
    var C=comp(D[i][0]); if(!C) continue;
    C.saveFrameToPng(D[i][1], new File("/tmp/dp_"+(100+i)+".png"));
  }
  var f=new File("/tmp/ae_qcdep.txt"); f.open("w"); f.write("ok "+D.length); f.close();
 }catch(e){ var fe=new File("/tmp/ae_qcdep.txt"); fe.open("w"); fe.write("ERRO "+e.toString()); fe.close(); }
})();

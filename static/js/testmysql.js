/**
 * Created by Administrator on 2016/11/29.
 */
    //创建数据库连接对象
var conn = new ActiveXObject("ADODB.Connection");
//创建数据集对象
var rs = new ActiveXObject("ADODB.Recordset");
//数据库连接串，具体配置请参考：http://www.connectionstrings.com/
//如果不知道如何配置连接串，可以通过配置UDL文件后用文本编辑器打开获得
//conn.open ("DSN=mysqltest")


conn.ConnectionString = "DRIVER={MySQL ODBC 5.3 ANSI Driver};OPTION=3;SERVER=localhost;User ID=root;Password=;Database=test;Port=3306";
//打开连接
conn.open;

//查询语句
var sql = " select color,count(*) ct  from jd where color <>' '  group by color  ";
//打开数据集（即执行查询语句）
rs.open( sql,conn);

//(或者rs=conn.execute(sql);)
//遍历所有记录
var  xdata =new Array();
var ydata=[];
var clorhtml="";
var dhtml="";
while(!rs.EOF)
{ 	   clorhtml=clorhtml+rs.Fields("color")+"\t" ;dhtml=dhtml+rs.Fields("ct")+"\t";rs.moveNext(); 	}
cht=clorhtml.split('\t');
dht=dhtml.split('\t');
for (i=0;i< cht.length;i++){
    xdata.push(cht[i]);
    ydata.push(dht[i]);
    document.write(xdata[i]+'\t'+ydata[i]+'</br>')
}
//关闭记录集
rs.close();
//关闭数据库连接
conn.close();

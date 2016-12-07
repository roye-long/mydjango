/**
 * Created by Administrator on 2016/12/1.
 */
var mysql = require('D:/Program Files/nodejs/node_modules/mysql')


//创建连接
var client = mysql.createConnection({
    user: 'root',
    password: '',
});
client.connect();
console.log('Connecting to MySQL...');

client.query('USE test');     //如果MySQL中没有库表，赶紧建。

http = require("http");

var server = http.createServer(function(request, response) {
    response.writeHeader(200, {"Content-Type": "text/html"});

    client.query('SELECT * FROM jd', function selectCb(err, results, fields) {
        if (err) {
            throw err;
        }

        var data = '';
        for (var i=0; i<results.length; i++) {
            var firstResult = results[i];
            data += 'clor: ' + (firstResult['color'])+'</br>';
        }

        response.write(data);
        response.end();
    });
});

server.listen(8080);

var sys = require("util");
sys.puts("Server running at http://localhost:8080/");

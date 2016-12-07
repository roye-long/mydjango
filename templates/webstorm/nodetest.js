/**
 * Created by Administrator on 2016/11/30.
 */

var mysql = require('D:/Program Files/nodejs/node_modules/mysql');

var TEST_DATABASE = 'test';
var TEST_TABLE = 'jd';

//创建连接
var client = mysql.createConnection({
    user: 'root',
    password: '',
});

client.connect();
client.query("use " + TEST_DATABASE);
var data=[]
client.query(
    'SELECT * FROM '+TEST_TABLE,
    function selectCb(err, results, fields) {
        if (err) {
            throw err;
        }
        if(results)
        {
            for(var i = 0; i < results.length; i++)
            {
                console.log("%s", results[i].color);
                data.push(results[i].color);

            }
            console.log(data);
        }
        client.end();
    }
);

var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendFile(__dirname + '/index.html');
});

const redis = require('redis');


io.on('connection', function(socket){
  socket.on('chat message', function(msg){
    io.emit('chat message', msg);
  });
});


const subscribe = redis.createClient();

subscribe.subscribe('b2c');
subscribe.on("message", function(channel, message) {
    console.log(message);
    console.log('once');
//client.send(message);
	io.emit('chat message', message);
        });

http.listen(3000, function(){
  console.log('listening on *:3000');
});

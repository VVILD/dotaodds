var app = require('express')();
var http = require('http').Server(app);
var io = require('socket.io')(http);

app.get('/', function(req, res){
  res.sendfile('index.html');
});

const redis = require('redis');r.
const client = redis.createClient();


http.listen(3000, function(){
  console.log('listening on *:3000');
});




io.on('connection', function(socket){

 //    listen to messages from channel pubsub

  console.log('a user connected');
  socket.on('disconnect', function(){
    console.log('user disconnected');
  });
});


const subscribe = redis.createClient();
const subscribe2 = redis.createClient();

subscribe.subscribe('b2c');
subscribe.on("message", function(channel, message) {
    console.log(message);
    console.log('once');
//client.send(message);
	io.emit('chat message', message);
        });


subscribe2.subscribe('b2b');
subscribe2.on("message", function(channel, message) {
    console.log(message);
    console.log('once2');
//client.send(message);
	io.emit('chat message2', message);
        });
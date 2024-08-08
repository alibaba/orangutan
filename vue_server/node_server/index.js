const port = 8888;

var WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({ port });

console.log('listening on port:', port);

// 连接池
let clients = {};
const CLIENT_NAME = {
  python: 'python',
  h5: 'h5',
};

wss.on('connection', function(ws) {
  // 将该连接加入连接池
  const { protocol } = ws;
  clients[protocol] = ws;

  // 如果是h5端建立了连接，向python端发送一个建联通知
  if (protocol.startsWith('h5')) {
    sendMessage2Client(protocol, 'python', 'h5_connected');
  }

  ws.on('message', function(message) {
    message = JSON.parse(message);
    const { type, data, to_protocol } = message;
    if (protocol.startsWith('h5')) {
      sendMessage2Client(protocol, 'python', type, data);
    } else if (protocol === 'python') {
      sendMessage2Client('python', to_protocol, type, data);
    }
  });

  ws.on('close', function(ws) {
    // 连接关闭时，将其移出连接池
    delete clients[protocol];
  });
});

function sendMessage2Client(from_protocol, to_protocol, type, data = {}) {
  // console.log(from_protocol, to_protocol, type, data);
  const ws = clients[to_protocol];
  const message = { type, data, from_protocol };
  ws
    ? ws.send(JSON.stringify(message))
    : console.log(`client ${to_protocol} not exists`);
}

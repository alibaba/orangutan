const port = 8888;

var WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({ port });

console.log('listening on port:', port);

let clients = {};
const CLIENT_NAME = {
  python: 'python',
  h5: 'h5',
};

wss.on('connection', function(ws) {
  const { protocol } = ws;
  clients[protocol] = ws;

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
    delete clients[protocol];
  });
});

function sendMessage2Client(from_protocol, to_protocol, type, data = {}) {
  const ws = clients[to_protocol];
  const message = { type, data, from_protocol };
  ws
    ? ws.send(JSON.stringify(message))
    : console.log(`client ${to_protocol} not exists`);
}

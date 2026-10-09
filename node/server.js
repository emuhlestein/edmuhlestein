import { createServer } from "node:http";
import { WebSocketServer } from "ws";

const port = Number(process.env.PORT || 2567);
const rooms = new Map();

function roomFor(id) {
  let room = rooms.get(id);
  if (!room) {
    room = {
      id,
      player: { x: 100, y: 200 },
      input: { left: false, right: false, jump: false },
      sockets: new Set(),
    };
    rooms.set(id, room);
  }
  return room;
}

function broadcast(room) {
  const payload = JSON.stringify({
    status: "running",
    player: room.player,
  });
  for (const socket of room.sockets) {
    if (socket.readyState === socket.OPEN) socket.send(payload);
  }
}

const server = createServer((req, res) => {
  if (req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ status: "ok", rooms: rooms.size }));
    return;
  }
  res.writeHead(404);
  res.end();
});

const wss = new WebSocketServer({ noServer: true });

server.on("upgrade", (req, socket, head) => {
  const match = new URL(req.url, "http://game").pathname.match(/^\/rooms\/([^/]+)$/);
  if (!match) {
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    ws.roomId = decodeURIComponent(match[1]);
    wss.emit("connection", ws, req);
  });
});

wss.on("connection", (ws) => {
  const room = roomFor(ws.roomId);
  room.sockets.add(ws);
  broadcast(room);

  ws.on("message", (data) => {
    try {
      const input = JSON.parse(data.toString());
      if (input.resize) {
        room.width = Number(input.width) || room.width;
        room.height = Number(input.height) || room.height;
        return;
      }
      if (input.reset) {
        room.player.x = room.width/2;
        room.player.y = room.height/2;
        room.player.vy = 0;
        room.input.left = false;
        room.input.right = false;
        room.input.jump = false;
        broadcast(room);
        return;
      }
      room.input.left = !!input.left;
      room.input.right = !!input.right;
      room.input.jump = !!input.jump;
    } catch {
      // ignore malformed input
    }
  });

  ws.on("close", () => {
    room.sockets.delete(ws);
    if (room.sockets.size === 0) rooms.delete(room.id);
  });
});

setInterval(() => {
  for (const room of rooms.values()) {
    if (room.input.left) room.player.x -= 4;
    if (room.input.right) room.player.x += 4;
    if (room.input.jump) room.player.y -= 4;
    broadcast(room);
  }
}, 50);

server.listen(port, "0.0.0.0", () => {
  console.log(`game server listening on ${port}`);
});

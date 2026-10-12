import { createServer } from "node:http";
import { WebSocketServer } from "ws";
import Matter from "matter-js";


const { Engine, Bodies, World } = Matter;

const engine = Engine.create({ gravity: { x: 0, y: 1 } });
const ground = Bodies.rectangle(400, 500, 800, 40, { isStatic: true });
const player = Bodies.rectangle(200, 200, 32, 32);
World.add(engine.world, [ground, player]);
const port = Number(process.env.PORT || 2567);
const rooms = new Map();

function roomFor(id) {
  let room = rooms.get(id);
  if (!room) {
    room = {
      id,
      width: 800,
      height: 600,
      player: { x: 100, y: 200 },
      input: { left: false, right: false, jump: false },
      sockets: new Set(),
    };
    room.engine = Engine.create({ gravity: { x: 0, y: 1 } });
    room.body = Bodies.rectangle(200, 200, 32, 32);
    room.ground = Bodies.rectangle(400, 500, 10000, 40, { isStatic: true });
    World.add(room.engine.world, [room.ground, room.body]);
    rooms.set(id, room);
  }
  return room;
}

function makeGround(room) {
  const width = room.width || 800;
  const height = room.height || 600;
  if (room.ground) {
    World.remove(room.engine.world, room.ground);
  }
  room.ground = Bodies.rectangle(width / 2, height - 20, width, 40, {
    isStatic: true
  });
  World.add(room.engine.world, room.ground);
}

function placeGround(room) {
  const width = room.width || 800;
  const height = room.height || 600;
  Matter.Body.setPosition(room.ground, {
    x: width / 2,
    y: height - 20
  });
}

function broadcast(room) {
  const payload = JSON.stringify({
    status: "running",
    player: room.player,
    ground: room.ground && {
      x: room.ground.position.x,
      y: room.ground.position.y,
      width: room.width,
      height: 40
    }
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
  console.log("upgrade", req.url);
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
  console.log("connection", ws.roomId);
  const room = roomFor(ws.roomId);
  room.sockets.add(ws);
  broadcast(room);

  ws.on("message", (data) => {
    // console.log("message", data.toString());
    try {
      const input = JSON.parse(data.toString());
      if (input.resize) {
        room.width = Number(input.width) || room.width;
        room.height = Number(input.height) || room.height;
        makeGround(room);
        return;
      }
      if (input.reset) {
        const x = (room.width || 800) / 2;
        const y = (room.height || 600) / 2;
        placeGround(room);
        console.log("reset to", x, y, "canvas", room.width, room.height);
        console.log("body before", room.body && room.body.position);
        Matter.Body.setPosition(room.body, { x, y });
        Matter.Body.setVelocity(room.body, { x: 0, y: 0 });
        room.player.x = x;
        room.player.y = y;
        console.log("body after", room.body.position);
        broadcast(room);
        return;
      }
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
  // console.log("tick", rooms.size);
  for (const room of rooms.values()) {
    const body = room.body;
    if (!body) continue;

    if (room.input.jump && body.position.y >= 470) {
      Matter.Body.setVelocity(body, { x: body.velocity.x, y: -10 });
      room.input.jump = false;
    }
    if (room.input.left) {
      Matter.Body.applyForce(body, body.position, { x: -0.002, y: 0 });
    }
    if (room.input.right) {
      Matter.Body.applyForce(body, body.position, { x: 0.002, y: 0 });
    }

    Engine.update(room.engine, 50);
    room.player.x = body.position.x;
    room.player.y = body.position.y;
    broadcast(room);
  }
}, 50);

server.listen(port, "0.0.0.0", () => {
  console.log(`game server listening on ${port}`);
});

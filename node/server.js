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
      player: { x: 16, y: 200 },
      input: { left: false, right: false, jump: false },
      sockets: new Set(),
      segments: [],
    };
    room.engine = Engine.create({ gravity: { x: 0, y: 1 } });
    room.body = Bodies.rectangle(16, 200, 32, 32);
    World.add(room.engine.world, room.body);
    layGround(room);
    rooms.set(id, room);
  }
  return room;
}

function addSegment(room, x, width, y, height, kind) {
  const body = Bodies.rectangle(x + width / 2, y, width, height, { isStatic: true });
  World.add(room.engine.world, body);
  room.segments.push({ body, width, height, kind });
}

function addObstacle(room, x, y) {
  addSegment(room, x - 16, 32, y, 64, "obstacle");
}

function layGround(room) {
  const height = 40;
  const floor = (room.height || 600) - height / 2;
  const target = room.width || 800;
  let x = 0;
  while (x < target) {
    const gap = x > 200 && Math.random() < 0.2;
    if (gap) {
      x += 36;
      continue;
    }
    const width = Math.min(160, target - x);
    addSegment(room, x, width, floor, height, "ground");
    if (x > 200 && Math.random() < 0.3) {
      addObstacle(room, x + width / 2, floor - height / 2 - 32);
    }
    x += width;
  }
  room.end = x;
}

function broadcast(room) {
  const payload = JSON.stringify({
    status: "running",
    player: room.player,
    ground: room.segments.map((s) => ({
      x: s.body.position.x,
      y: s.body.position.y,
      width: s.width,
      height: s.height,
      kind: s.kind
    }))
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
        for (const s of room.segments) World.remove(room.engine.world, s.body);
        room.segments = [];
        layGround(room);
        broadcast(room);
        return;
      }

      if (input.reset) {
        const groundHeight = 80;
        const floor = (room.height || 600) - groundHeight;
        const x = 16;
        const y = floor - 16;
        Matter.Body.setPosition(room.body, { x, y });
        Matter.Body.setVelocity(room.body, { x: 0, y: 0 });
        room.player.x = x;
        room.player.y = y;
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
  // console.log("tick", rooms.size);
  for (const room of rooms.values()) {
    const body = room.body;
    if (!body) continue;

    if (room.input.left) {
      Matter.Body.applyForce(room.body, room.body.position, { x: -0.002, y: 0 });
    }
    if (room.input.right) {
      Matter.Body.applyForce(room.body, room.body.position, { x: 0.002, y: 0 });
    }
    if (room.input.jump && room.body.position.y >= (room.height || 600) - 80) {
      Matter.Body.setVelocity(room.body, { x: room.body.velocity.x, y: -10 });
      room.input.jump = false;
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

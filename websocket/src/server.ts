import * as express from "express"
import * as WebSocket from 'ws';
import * as http from "http";
import {ProgressInfo} from "./progress_obj";

const app = express();
app.use(express.json());
const server = http.createServer(app);
const wss = new WebSocket.Server({ server: server, path: "" });
const port = 3005;

app.post("/progress", async (req,res) =>{
    let progress: ProgressInfo = req.body;
    console.log(progress)
});

server.listen(port, ()=> console.log(`App running at port: ${port}`));
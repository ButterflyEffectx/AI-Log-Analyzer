import express from "express";
import bodyParser from "body-parser";
// import mysql from "mysql2/promise";
import pkg from "pg";
const { Pool } = pkg;
import bcrypt from "bcrypt";
import cors from "cors";

const app = express();
app.use(bodyParser.json());
app.use(cors());

// const db = await mysql.createConnection({
//     host: process.env.DB_HOST || "db",
//     user: process.env.DB_USER || "webuser",
//     password: process.env.DB_PASSWORD || "webpass",
//     database: process.env.DB_NAME || "login_system"
// });

app.set("trust proxy", true);

const pool = new Pool({
    connectionString: process.env.DATABASE_URL,
    ssl: { rejectUnauthorized: false }
});

const blockedIPs = ["111.222.333.444"];

app.post("/login", async (req, res) => {
    const { username, password: inputPassword } = req.body;

    let ip = req.ip.replace("::ffff:", "");
    if (ip === "::1") ip = "127.0.0.1";

    if (blockedIPs.includes(ip)) {
        await pool.query(
            "INSERT INTO login_logs (username, ip_address, status) VALUES ($1, $2, $3)",
            [username, ip, "blocked"]
        );
        return res.status(403).json({ message: "Blocked IP" });
    }

    const result = await pool.query("SELECT * FROM users WHERE username=$1", [username]);
    if (result.rows.length === 0) {
        await pool.query(
            "INSERT INTO login_logs (username, ip_address, status) VALUES ($1, $2, $3)",
            [username, ip, "failed"]
        );
        return res.status(401).json({ message: "Invalid credentials" });
    }

    const user = result.rows[0];
    const match = await bcrypt.compare(inputPassword, user.password_hash);

    if (!match) {
        await pool.query(
            "INSERT INTO login_logs (username, ip_address, status) VALUES ($1, $2, $3)",
            [username, ip, "failed"]
        );
        return res.status(401).json({ message: "Invalid credentials" });
    }

    await pool.query(
        "INSERT INTO login_logs (username, ip_address, status) VALUES ($1, $2, $3)",
        [username, ip, "success"]
    );

    return res.json({ message: "Login success" });
});

app.get("/logs", async (req, res) => {
    const result = await pool.query("SELECT * FROM login_logs ORDER BY timestamp DESC");
    res.json(result.rows);
});

app.listen(3000, () => console.log("Server running on http://localhost:3000"));

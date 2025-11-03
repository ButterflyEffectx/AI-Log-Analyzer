import mysql from "mysql2/promise";
import bcrypt from "bcrypt";

const db = await mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "login_system"
});

const username = "admin1";
const password = "admin1";

const hash = await bcrypt.hash(password, 10);

await db.query(
    "INSERT INTO users (username, password_hash) VALUES (?, ?)",
    [username, hash]
);

console.log("✅ User added!");
